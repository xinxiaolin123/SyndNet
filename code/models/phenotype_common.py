#!/usr/bin/env python3
from __future__ import annotations
import torch
from diagnostic_model import ConvNeXtTinyEncoder, DIAGNOSTICDualViewModel
from anatomy_model import ConvNeXtAnatomyEncoder, ANATOMYAnatomyTeacher
from reliability_model import ReliabilityCalibrator
from matched_residual_model import PHENOTYPEBiomechanicalPhenotype


def init_model(normal_path, baseline_path, teacher_path, calibrator_path):
    normal=torch.load(normal_path,map_location="cpu",weights_only=False)
    encoder=ConvNeXtTinyEncoder(False); encoder.load_state_dict(normal["encoder"],strict=True)
    baseline=DIAGNOSTICDualViewModel(encoder,normal["prototype_mean"],normal["prototype_scale"])
    state=torch.load(baseline_path,map_location="cpu",weights_only=False); baseline.load_state_dict(state.get("state_dict",state.get("model",state)),strict=True)
    teacher=ANATOMYAnatomyTeacher(ConvNeXtAnatomyEncoder(False)); state=torch.load(teacher_path,map_location="cpu",weights_only=False); teacher.load_state_dict(state["model"],strict=True)
    calibrator=ReliabilityCalibrator(); state=torch.load(calibrator_path,map_location="cpu",weights_only=False); calibrator.load_state_dict(state["model"],strict=True)
    return PHENOTYPEBiomechanicalPhenotype(baseline,teacher,calibrator)
