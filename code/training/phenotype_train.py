#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, random
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import DataLoader
from diagnostic_runtime import ClassificationDataset, load_manifest
from phenotype_common import init_model
from matched_residual_model import PHENOTYPE_NAMES, phenotype_loss


def make_loader(rows, args, training, epoch=0):
    generator = torch.Generator().manual_seed(args.seed * 10000 + args.fold * 100 + epoch)
    return DataLoader(ClassificationDataset(rows, args.image_size, training), batch_size=args.batch_size,
        shuffle=training, num_workers=args.workers, pin_memory=True, drop_last=training,
        generator=generator if training else None)


@torch.no_grad()
def predict(model, data_loader, fold, seed):
    model.eval(); records = []
    for batch in data_loader:
        ap, lat = batch["ap"].cuda(non_blocking=True), batch["lat"].cuda(non_blocking=True)
        with torch.autocast("cuda", dtype=torch.float16):
            extracted = model.extract(ap, lat)
            outputs = {mode: model.compose(extracted, mode) for mode in
                       ("identity", "no_biomechanics", "reverse_reliability", "derange_anchors")}
            axes = [model.compose(extracted, "zero_axis", index) for index in range(len(PHENOTYPE_NAMES))]
        for row_index, release_case_id in enumerate(batch["release_case_id"]):
            identity = outputs["identity"]
            row = {"release_case_id": release_case_id, "fold": fold, "seed": seed,
                   "label": int(batch["label"][row_index]),
                   "baseline_probability": float(identity["baseline_logit"][row_index].sigmoid()),
                   "identity_probability": float(identity["logit"][row_index].sigmoid()),
                   "biomechanical_residual": float(identity["biomechanical_residual"][row_index]),
                   "anatomy_gate": float(identity["anatomy_gate"][row_index])}
            for mode in ("no_biomechanics", "reverse_reliability", "derange_anchors"):
                row[f"{mode}_probability"] = float(outputs[mode]["logit"][row_index].sigmoid())
            for index, name in enumerate(PHENOTYPE_NAMES):
                row[name] = float(identity["phenotype"][row_index, index])
                row[f"zero_{name}_probability"] = float(axes[index]["logit"][row_index].sigmoid())
            records.append(row)
    return records


def main():
    parser = argparse.ArgumentParser()
    for name in ("manifest", "normal_checkpoint", "baseline_root", "teacher_root", "calibrator_root", "output"):
        parser.add_argument("--" + name.replace("_", "-"), required=True, type=Path)
    parser.add_argument("--fold", required=True, type=int, choices=range(5)); parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--epochs", type=int, default=30); parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--accumulation", type=int, default=4); parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--lr", type=float, default=2e-4); parser.add_argument("--image-size", type=int, default=384)
    parser.add_argument("--expected-cases", type=int, default=1461)
    args = parser.parse_args()
    if not torch.cuda.is_available(): raise SystemExit("ERROR: CUDA required")
    random.seed(args.seed + args.fold); np.random.seed(args.seed + args.fold); torch.manual_seed(args.seed + args.fold); torch.cuda.manual_seed_all(args.seed + args.fold)
    rows = load_manifest(args.manifest, "internal")
    if len(rows) != args.expected_cases: raise SystemExit(f"ERROR: expected {args.expected_cases} cases, found {len(rows)}")
    args.output.mkdir(parents=True, exist_ok=True)
    if all((args.output / name).is_file() for name in ("COMPLETE", "model.pt", "predictions.csv")):
        print(json.dumps({"status": "SKIP_COMPLETE", "seed": args.seed, "fold": args.fold})); return
    model = init_model(args.normal_checkpoint, args.baseline_root / f"fold_{args.fold}" / "model.pt",
                       args.teacher_root / f"fold_{args.fold}" / "best.pt", args.calibrator_root / f"fold_{args.fold}.pt").cuda()
    parameters = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=args.lr, weight_decay=0.03); scaler = torch.amp.GradScaler("cuda")
    train_rows = [r for r in rows if int(r["fold"]) != args.fold]; test_rows = [r for r in rows if int(r["fold"]) == args.fold]
    last = args.output / "last.pt"; start = 0
    if last.exists():
        state = torch.load(last, map_location="cpu", weights_only=False); model.load_state_dict(state["model"], strict=True); optimizer.load_state_dict(state["optimizer"]); start = state["epoch"] + 1
    for epoch in range(start, args.epochs):
        model.train(); model.baseline.eval(); model.teacher.eval(); model.calibrator.eval(); losses=[]; optimizer.zero_grad(set_to_none=True)
        data_loader = make_loader(train_rows, args, True, epoch)
        for step, batch in enumerate(data_loader, 1):
            with torch.autocast("cuda", dtype=torch.float16):
                output = model(batch["ap"].cuda(non_blocking=True), batch["lat"].cuda(non_blocking=True))
                total, parts = phenotype_loss(output, batch["label"].cuda(non_blocking=True)); loss = total / args.accumulation
            scaler.scale(loss).backward(); losses.append(float(total.detach()))
            if step % args.accumulation == 0 or step == len(data_loader):
                scaler.unscale_(optimizer); torch.nn.utils.clip_grad_norm_(parameters, 3.0); scaler.step(optimizer); scaler.update(); optimizer.zero_grad(set_to_none=True)
        torch.save({"protocol":"MATCHED-RESIDUAL-CHECKPOINT-1.0","model":model.state_dict(),"optimizer":optimizer.state_dict(),"epoch":epoch,"seed":args.seed,"fold":args.fold}, last)
        print(json.dumps({"event":"PHENOTYPE_EPOCH","seed":args.seed,"fold":args.fold,"epoch":epoch,"loss":float(np.mean(losses))}), flush=True)
    records = predict(model, make_loader(test_rows, args, False), args.fold, args.seed)
    with (args.output / "predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer=csv.DictWriter(handle, fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)
    torch.save({"protocol":"MATCHED-RESIDUAL-FINAL-1.0","seed":args.seed,"fold":args.fold,"state_dict":model.state_dict(),"phenotypes":PHENOTYPE_NAMES,
                "claim_guardrail":"standardized radiographic proxy phenotypes; not patient-specific FE"}, args.output / "model.pt")
    (args.output / "COMPLETE").write_text("COMPLETE\n", encoding="ascii")
    print(json.dumps({"status":"PHENOTYPE_FOLD_COMPLETE","seed":args.seed,"fold":args.fold,"n":len(records)}), flush=True)


if __name__ == "__main__": main()
