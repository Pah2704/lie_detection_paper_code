# Experimental Environment

The author confirmed on 1 November 2026 that the project environment recorded
below was used for the reported experiments. Historical project notes and
installed-package metadata support this record.

| Component | Version |
| --- | --- |
| Python | 3.10.20 |
| GPU | NVIDIA GeForce RTX 3060 12GB |
| PyTorch | 2.5.1+cu121 |
| torchvision | 0.20.1+cu121 |
| torchaudio | 2.5.1+cu121 |
| CUDA build of PyTorch | 12.1 |
| Transformers | 5.5.3 |
| MediaPipe | 0.10.14 |
| OpenCV Python distributions | 4.13.0.92 |
| NumPy | 2.2.6 |
| pandas | 2.3.3 |
| scikit-learn | 1.7.2 |
| SciPy | 1.15.3 |
| Matplotlib | 3.10.9 |
| seaborn | 0.13.2 |
| PyYAML | 6.0.3 |
| tqdm | 4.67.3 |
| openpyxl | 3.1.5 |

Both `opencv-python` and `opencv-contrib-python` are present in the recorded
environment. The installation requirements select only the contrib distribution
to avoid installing two distributions that provide the same `cv2` module.
OpenCV reports the API version as 4.13.0.

`requirements.txt` and `requirements-torch-cu121.txt` pin the project packages
listed above, not every transitive dependency. FFmpeg/FFprobe versions, GPU driver
and cuDNN versions, downloaded-backbone revisions and per-run optimizer states
are not provided as historical records. The cu121 suffix identifies the PyTorch
CUDA build, not the installed GPU driver version.

The implementation sets cuDNN benchmark to true and deterministic to false.
Seeds are set, but bitwise deterministic training is not claimed. Optional W&B
logging is off in the manuscript wrapper; W&B, yt-dlp and Grad-CAM are not claimed
as installed packages in this environment record.

