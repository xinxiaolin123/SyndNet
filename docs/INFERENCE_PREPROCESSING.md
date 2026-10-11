# Locked paired-image preprocessing

The adapter calls `clean_tensor` in the unchanged `code/utils/diagnostic_runtime.py`. The authoritative external predictor calls the equivalent `v62_runtime.ClassificationDataset(..., 384, False)`; this is a deterministic path.

Each AP and lateral input is opened separately by Pillow, converted to 8-bit grayscale `L`, cropped by `dx=max(1,int(width*0.025))` and `dy=max(1,int(height*0.025))` on both opposing borders, and centred on a black grayscale square canvas whose side is the larger cropped dimension. Odd padding differences use integer floor offsets. The canvas is resized to 384 × 384 with Pillow BILINEAR interpolation and converted to RGB by repeating the grayscale channel. `torchvision.transforms.functional.to_tensor` maps uint8 to floating values in [0,1]. Channel means [0.485,0.456,0.406] and standard deviations [0.229,0.224,0.225] define normalization.

AP is passed as the first model argument and lateral as the second. No random crop, affine transform, augmentation or preprocessing flip is enabled. The model itself performs a deterministic horizontal-flip teacher pass for reliability features; this is part of the original mathematics.

No automatic orientation correction, EXIF transpose, laterality standardization, DICOM windowing, view detection or 16-bit calibration is implemented in the submitted path. Provide already exported, correctly oriented AP/lateral images following the study acquisition conventions. This release does not validate alternative projections or arbitrary DICOM conversion. Grayscale conversion follows Pillow semantics rather than adding a new intensity policy. The source has no explicit left/right orientation canonicalization; none is inferred here.
