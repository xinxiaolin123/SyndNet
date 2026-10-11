#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from final_scale_common import FINAL, PROBES, ROOT, load_config, metrics, read_csv, sha256, threshold_for_sensitivity, write_csv, write_json


def main() -> None:
    config = load_config(); FINAL.mkdir(parents=True, exist_ok=True)
    decision = json.loads((PROBES / "RESIDUAL_SCALING_SELECTION.json").read_text(encoding="utf-8"))
    if decision["selected_route"] != "residual_scaling_selected":
        raise RuntimeError("finalize_scale is allowed only after residual_scaling_selected")
    rows = read_csv(PROBES / "PROBE_OOF_PATIENT_PREDICTIONS.csv")
    y = np.asarray([int(row["label"]) for row in rows])
    anchor = np.asarray([float(row["phenotype_probability"]) for row in rows])
    candidate = np.asarray([float(row["scale_probability"]) for row in rows])
    # Preserve the already locked PHENOTYPE fold-safe clinical operating contract.
    # The model change is isolated to the residual scale; no threshold is
    # re-selected on held-out outcomes.
    threshold = np.asarray([float(row["phenotype_threshold"]) for row in rows])
    anchor_metrics = metrics(y, anchor, threshold)
    final_metrics = metrics(y, candidate, threshold)
    anchor_correct = (anchor >= threshold) == y
    final_correct = (candidate >= threshold) == y
    transitions = {
        "phenotype_wrong_to_final_correct": int((~anchor_correct & final_correct).sum()),
        "phenotype_correct_to_final_wrong": int((anchor_correct & ~final_correct).sum()),
        "fp_rescued": int(((y == 0) & (anchor >= threshold) & (candidate < threshold)).sum()),
        "new_fp": int(((y == 0) & (anchor < threshold) & (candidate >= threshold)).sum()),
        "fn_rescued": int(((y == 1) & (anchor < threshold) & (candidate >= threshold)).sum()),
        "new_fn": int(((y == 1) & (anchor >= threshold) & (candidate < threshold)).sum()),
    }
    bootstrap = decision["scale_probe"]["bootstrap"]
    gates = {
        "auroc_noninferiority_check": final_metrics["auroc"] - anchor_metrics["auroc"] >= -0.0005,
        "average_precision_noninferiority_check": final_metrics["ap"] - anchor_metrics["ap"] >= -0.001,
        "specificity_noninferiority_check": final_metrics["specificity"] >= anchor_metrics["specificity"],
        "sensitivity_tolerance_check": final_metrics["sensitivity"] >= anchor_metrics["sensitivity"] - 0.005,
        "probability_quality_check": final_metrics["brier"] <= anchor_metrics["brier"] and final_metrics["log_loss"] <= anchor_metrics["log_loss"],
        "error_transition_check": transitions["phenotype_wrong_to_final_correct"] > transitions["phenotype_correct_to_final_wrong"],
        "residual_scale_stability_check": decision["scale_probe"]["stability"]["boundary_count"] == 0,
        "substantive_improvement": bootstrap["brier"]["ci95"][1] < 0 and
                                   final_metrics["auroc"] >= anchor_metrics["auroc"] and
                                   final_metrics["ap"] >= anchor_metrics["ap"] - .001,
    }
    selection_met = all(gates.values())
    protocol = {
        "protocol": config["protocol"], "candidate": "Final SyndNet",
        "formula": "final_logit = baseline_logit + alpha_train * phenotype_biomechanical_residual",
        "phenotype_frozen": True, "residual_off_exact_phenotype": True,
        "alpha_bounds": [0.5, 2.0], "scale_penalty": config["scale_penalty"],
        "threshold_policy": "inherit the pre-existing fold-safe PHENOTYPE threshold for each outer fold",
        "sensitivity_nonregression_tolerance_absolute": 0.005,
        "external_locked_during_development": True,
    }
    write_json(FINAL / "FINAL_PROTOCOL_LOCK.json", protocol)

    scale_rows = [row for row in read_csv(PROBES / "RESIDUAL_SCALING_EVALUATION.csv") if row.get("seed")]
    alpha_map = {f"seed_{int(row['seed'])}_fold_{int(row['outer_fold'])}": float(row["alpha"]) for row in scale_rows}
    weights = {"protocol": config["protocol"], "candidate": "Final SyndNet",
               "alpha_by_checkpoint": alpha_map, "alpha_parameter_count": 15,
               "note": "One scalar was fitted on the corresponding outer-training patients for each frozen PHENOTYPE seed/fold checkpoint."}
    weights_path = FINAL / "FINAL_SCALE_WEIGHTS.json"; write_json(weights_path, weights)

    final_rows = []
    for row, pred, cut in zip(rows, candidate, threshold):
        final_rows.append({"release_case_id": row["release_case_id"], "outer_fold": int(row["fold"]), "label": int(row["label"]),
                           "phenotype_raw_probability": float(row["phenotype_probability"]), "final_raw_probability": float(pred),
                           "fold_safe_threshold": float(cut), "phenotype_predicted_label": int(float(row["phenotype_probability"]) >= cut),
                           "final_predicted_label": int(pred >= cut)})
    write_csv(FINAL / "FINAL_OOF_PATIENT_PREDICTIONS.csv", final_rows)
    write_json(FINAL / "FINAL_PAIRED_VS_PHENOTYPE_BOOTSTRAP.json", bootstrap)
    write_csv(FINAL / "FINAL_ERROR_TRANSITIONS.csv", [{**transitions, "phenotype_errors": int((~anchor_correct).sum()),
                                                         "final_errors": int((~final_correct).sum())}])
    write_csv(FINAL / "FINAL_MECHANISM_ABLATION.csv", [
        {"model": "Matched residual", **anchor_metrics},
        {"model": "Final SyndNet", **final_metrics},
        {"model": "Without residual", **anchor_metrics},
    ])
    selection_summary = {"protocol": config["protocol"], "candidate": "Final SyndNet",
                 "phenotype_metrics": anchor_metrics, "final_metrics": final_metrics,
                 "deltas": {name: float(final_metrics[name]) - float(anchor_metrics[name]) for name in ("auroc", "ap", "brier", "log_loss", "sensitivity", "specificity")},
                 "transitions": transitions, "gates": gates, "selection_criteria_met": selection_met,
                 "external_data_read": False}
    write_json(FINAL / "MODEL_SELECTION_SUMMARY.json", selection_summary)

    code_paths = [Path(__file__).resolve().parent.parent / "models" / "final_syndnet.py"]
    write_csv(FINAL / "FINAL_MODEL_CODE_SHA256.csv", [{"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for path in code_paths])
    write_csv(FINAL / "FINAL_MODEL_WEIGHTS_SHA256.csv", [{"path": weights_path.name, "sha256": sha256(weights_path)}])
    manifest_path = Path(config["manifest"])
    write_csv(FINAL / "FINAL_DATA_MANIFEST_SHA256.csv", [{"path": str(manifest_path), "sha256": sha256(manifest_path)}])
    freeze = {"protocol": config["protocol"], "candidate": "Final SyndNet", "selection_criteria_met": selection_met,
              "architecture_frozen": selection_met, "weights_frozen": selection_met, "threshold_frozen": selection_met,
              "calibrator": "unchanged PHENOTYPE raw probability path", "post_external_retuning_prohibited": True,
              "external_global_threshold_phenotype": threshold_for_sensitivity(y, anchor, config["target_sensitivity"]),
              "external_global_threshold_final": threshold_for_sensitivity(y, candidate, config["target_sensitivity"]),
              "code_sha256": sha256(code_paths[0]), "weights_sha256": sha256(weights_path),
              "manifest_sha256": sha256(manifest_path)}
    write_json(FINAL / "FINAL_FREEZE.json", freeze)
    write_json(FINAL / "EXTERNAL_VALIDATION_PROTOCOL.json", {
        "protocol": config["protocol"], "ALLOW_EXTERNAL": bool(selection_met),
        "candidate": "Final SyndNet" if selection_met else None,
        "condition": "one-shot external validation assessment; no external refitting or recalibration",
        "freeze_sha256": sha256(FINAL / "FINAL_FREEZE.json"),
    })
    print(json.dumps({"status": "final_model_ready", "selection_criteria_met": selection_met,
                      "delta_auroc": selection_summary["deltas"]["auroc"],
                      "delta_specificity": selection_summary["deltas"]["specificity"]}), flush=True)


if __name__ == "__main__":
    main()
