# Minimal metric-interface example

`demo_metrics.csv` contains four invented nonclinical observations, not patient data or study results. It demonstrates the existing metric interface with recorded toy decisions and probabilities. It does not demonstrate trained-model imaging inference, MRMC fitting, or full retraining.

From the repository root, after installing the numerical environment:

```bash
python examples/demo_metrics.py
```

The example has perfect label ranking and classification by construction. Its output must not be used as evidence of study performance.
