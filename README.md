# polyp-detect

YOLOv8n / YOLOv11n / YOLOv11s polyp detector on PolypDB — Phase 1 + Cross-Modality

**Dataset:** [PolypDB](https://osf.io/pr7ms/) — 3,934 endoscopy images, 5 modalities (WLI/NBI/BLI/FICE/LCI)  
**Phase 1 scope:** WLI-only training → cross-modality evaluation  
**Architecture:** YOLO family (v8n / v11n / v11s)  
**SOTA reference:** GDCA-Net mAP@50 = 85.9% · Best YOLO in paper (YOLOv6) = 92.5%

---

## Results — WLI Training (100 epochs + HSV augmentation)

| Model | mAP@50 | mAP@50-95 | Precision | Recall |
|---|---|---|---|---|
| YOLOv11s (พี่ฟิล์ม baseline · 50ep · no HSV) | 94.09% | — | — | 84.29% |
| YOLOv8n (100ep + HSV) | 94.6% | 77.4% | 93.6% | 89.3% |
| YOLOv11n (100ep + HSV) | 93.8% | 76.6% | 92.8% | 88.4% |
| **YOLOv11s (100ep + HSV)** | **94.7%** | **77.8%** | **94.5%** | **90.5%** |

Key delta vs baseline: +0.61pp mAP@50, +6.21pp Recall — from 100 epochs + HSV augmentation.  
All models beat GDCA-Net (85.9%) and best YOLO in paper (92.5%).

---

## Results — Cross-Modality Generalization (YOLOv11s · WLI-trained only)

Train on WLI → test on 4 unseen modalities with zero additional training.

| Modality | Seen in training? | Test images | mAP@50 | Precision | Recall |
|---|---|---|---|---|---|
| WLI | ✅ Yes | 358 | 94.7% | 94.5% | 90.5% |
| NBI | ❌ No | 14 | 87.4% | 97.5% | 86.7% |
| BLI | ❌ No | 7 | 96.1% | 99.1% | 88.9% |
| FICE | ❌ No | 7 | 94.5% | 77.8% | 100.0% |
| LCI | ❌ No | 6 | 99.5% | 100.0% | 99.7% |

vs paper (per-modality trained models):

| Modality | Paper best | Ours (WLI-only) | Delta |
|---|---|---|---|
| WLI | 92.5% | **94.7%** | +2.2pp |
| NBI | 68.8% | **87.4%** | +18.6pp |
| BLI | 68.8% | **96.1%** | +27.3pp |
| FICE | 88.7% | **94.5%** | +5.8pp |
| LCI | 99.5% | **99.5%** | 0pp |

Single WLI-trained model outperforms paper's per-modality trained models on NBI and BLI by a large margin.

---

## Quickstart

### 1. Prepare dataset
```bash
python src/prepare_dataset.py --data_root ./data/polypdb --modality WLI
```

### 2. Train
```bash
# YOLOv8n
python src/train.py --model yolov8n.pt --data configs/wli_yolov8n.yaml --epochs 100

# YOLOv11n
python src/train.py --model yolo11n.pt --data configs/wli_yolov11n.yaml --epochs 100 --name yolov11n_wli

# YOLOv11s
python src/train.py --model yolo11s.pt --data configs/wli_yolov11s.yaml --epochs 100 --name yolov11s_wli
```

### 3. Evaluate (mAP + speed + size + ONNX)
```bash
python src/evaluate.py --weights runs/train/yolov11s_wli/weights/best.pt
```

### 4. Cross-modality evaluation
```bash
python src/cross_modality_eval.py \
  --weights runs/train/yolov11s_wli/weights/best.pt \
  --data_root ./data/polypdb
```

### 5. Train on Kaggle (recommended — free T4 GPU)
Upload `notebooks/polypdb_comparison.ipynb` → enable GPU T4 → run all cells.

---

## Project Structure
```
polyp-detect/
├── configs/
│   ├── wli_yolov8n.yaml         # Dataset config — YOLOv8n
│   ├── wli_yolov11n.yaml        # Dataset config — YOLOv11n
│   └── wli_yolov11s.yaml        # Dataset config — YOLOv11s
├── notebooks/
│   ├── polypdb_yolov8n_wli.ipynb    # Phase 1: YOLOv8n baseline (พี่ฟิล์ม)
│   └── polypdb_comparison.ipynb     # Phase 1+: Multi-model + cross-modality
├── src/
│   ├── prepare_dataset.py       # COCO → YOLO conversion, WLI filter
│   ├── train.py                 # Training script
│   ├── evaluate.py              # mAP + speed + ONNX export
│   └── cross_modality_eval.py   # Cross-modality generalization test
└── data/                        # (gitignored) downloaded dataset
```

---

## Pre-trained Weights

Trained model weights available on Google Drive:  
[Download Model Weights (.pt)](https://drive.google.com/drive/folders/11DyxCTp5oOPeZy0iC92uq0J_M_VEpO0V?usp=sharing)

| File | Size | mAP@50 |
|---|---|---|
| DOWNLOAD_YOLOv8n_best.pt | 6.0 MB | 94.6% |
| DOWNLOAD_YOLOv11n_best.pt | 5.2 MB | 93.8% |
| DOWNLOAD_YOLOv11s_best.pt | 18.3 MB | 94.7% |

---

## Dataset Details

| Modality | Images | % of total |
|---|---|---|
| WLI (White Light) | ~3,558 | 90.4% |
| NBI | ~146 | 3.7% |
| BLI | ~60 | 1.5% |
| FICE | ~88 | 2.2% |
| LCI | ~82 | 2.1% |

---

## References
- Paper: [PolypDB arxiv 2409.00045](https://arxiv.org/abs/2409.00045)
- Dataset: [OSF osf.io/pr7ms](https://osf.io/pr7ms/)
- GitHub: [DebeshJha/PolypDB](https://github.com/DebeshJha/PolypDB)
- Ultralytics: [docs.ultralytics.com](https://docs.ultralytics.com)
