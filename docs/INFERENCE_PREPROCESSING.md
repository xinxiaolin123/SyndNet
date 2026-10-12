# Input preprocessing

Provide correctly oriented, exported AP and lateral images. AP is the first model input and lateral is the second. The adapter applies deterministic grayscale conversion, border cropping, black square padding, resizing to the configured input size and ImageNet normalization. The implementation is in `code/utils/diagnostic_runtime.py`.

No DICOM windowing, automatic view detection, EXIF transpose or orientation canonicalization is performed. Input preparation must be consistent with the intended paired-image use. Alternative image conversions are not validated by this example.
