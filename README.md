# Polyp Detection — Cross-Modal Architecture Comparison

**Which YOLO architecture generalizes best across endoscopic imaging modalities?**

> PolypDB · 4-Architecture Comparison · Trained on WLI → Zero-shot tested on NBI / BLI / FICE / LCI

---

## The Research Question

PolypDB contains 5 imaging modalities: WLI, NBI, BLI, FICE, and LCI.  
WLI (White Light Imaging) accounts for 3,588 of 3,934 images (91%).

> **Does architecture choice — independent of augmentation — affect how well a WLI-trained model generalizes to unseen imaging modalities?**

This study trains four architectures under identical conditions (same dataset, epochs, augmentation config) where **only the model architecture varies**.

---

## Four-Architecture Comparison

| Model | Parameters | GFLOPs | Family |
|---|---|---|---|
| **YOLO26s** | 9.47M | 20.5 | Custom (YOLO26) |
| **YOLOv11n** | 2.58M | 6.3 | Ultralytics v11 nano |
| **YOLOv11s** | 9.41M | 21.3 | Ultralytics v11 small |
| **YOLOv8n** | 3.01M | 8.1 | Ultralytics v8 nano |

---

## Cross-Modal Results

### mAP@50 Heatmap

![Cross-Modal Heatmap](cross_modal_heatmap.png)

### Full Results Table

| Model | WLI (train) | LCI | FICE | NBI | BLI | Avg OOD |
|---|---|---|---|---|---|---|
| **YOLO26s** | 0.983 | 0.980 | 0.881 | 0.790 | 0.761 | 0.853 |
| **YOLOv11n** | 0.977 | 0.977 | 0.962 | 0.929 | 0.921 | 0.947 |
| **YOLOv11s** | 0.983 | **0.992** | 0.961 | **0.943** | **0.940** | **0.959** |
| **YOLOv8n** | **0.983** | 0.989 | **0.963** | 0.926 | 0.933 | 0.953 |

> WLI = training modality (val set). LCI / FICE / NBI / BLI = zero-shot (never seen during training).  
> Avg OOD = mean mAP@50 across 4 unseen modalities.

---

## Key Findings

### 1. Larger is not more generalizable

YOLO26s achieves the same WLI performance as others (98.3%) but the worst OOD generalization — dropping to 76.1% on BLI and 79.0% on NBI.

YOLOv11s (similar parameter count) outperforms it on every OOD modality by **6–18 percentage points**.

| Model | WLI → BLI drop | WLI → NBI drop |
|---|---|---|
| YOLO26s | **−22.2%** | **−19.3%** |
| YOLOv11n | −5.6% | −4.8% |
| YOLOv11s | −4.3% | −3.9% |
| YOLOv8n | −5.0% | −5.7% |

YOLO26s has **4–5× larger cross-modal drop** than the v11/v8 architectures.

### 2. YOLOv11s achieves best overall balance

- Best average OOD mAP@50: **95.9%**
- Highest single OOD score: LCI **99.2%**
- Most consistent across all 5 modalities

### 3. YOLOv8n punches above its weight

3.01M parameters vs 9.41M for YOLOv11s — yet achieves **95.3% average OOD**. Strong generalization at 1/3 the model size.

### 4. Cross-modal drop order is consistent across all architectures

**LCI > FICE > NBI > BLI** — this reflects domain shift magnitude, not architecture behavior.

---

## Why the Cross-Modal Gaps Exist

**LCI generalizes best** — Linked Color Imaging preserves the white-light color profile. Closest color statistics to WLI.

**NBI and BLI drop significantly** — Narrow-band imaging uses 415nm / 540nm wavelengths to highlight vascular patterns, producing fundamentally different color distributions.

**FICE sits in between** — Post-processing simulation of narrow-band contrast with partial WLI color overlap.

**Clinical implication:** A WLI-only model is reliable for standard imaging and LCI, but should not be deployed for NBI/BLI without additional adaptation. The gap is not a model failure — it is a real domain boundary.

---

## Training Configuration

| Parameter | Value |
|---|---|
| Training modality | WLI only |
| Dataset split | 70 / 15 / 15 (train / val / test) |
| Epochs | 100 |
| Image size | 640px |
| Augmentation | HSV locked (hsv_h/s/v = 0.0), spatial flips, mixup |
| Hardware | Kaggle T4 GPU |

**HSV lock rationale:** Standard YOLO augmentation applies HSV jitter by default. For medical endoscopy this is incorrect — color carries diagnostic signal (redness = inflammation, pallor = tissue state). Locking HSV preserves the biological markers that enable cross-modal transfer.

---

## Dataset

**PolypDB** — Jha et al. 2024 ([arXiv:2409.00045](https://arxiv.org/abs/2409.00045))  
3,934 colonoscopy images · 5 modalities · 3 hospitals (Norway, Sweden, Vietnam)

| Modality | Full name | Images |
|---|---|---|
| WLI | White Light Imaging | 3,588 |
| NBI | Narrow Band Imaging | 146 |
| BLI | Blue Light Imaging | 70 |
| FICE | Flexible Spectral Imaging Color Enhancement | 70 |
| LCI | Linked Color Imaging | 60 |

---

## Reproduce

```bash
pip install ultralytics==8.4.6

# Evaluate cross-modal generalization
python scripts/evaluate.py --weights <model>.pt --modality NBI
python scripts/evaluate.py --weights <model>.pt --modality BLI
python scripts/evaluate.py --weights <model>.pt --modality FICE
python scripts/evaluate.py --weights <model>.pt --modality LCI

# Generate cross-modal heatmap
python scripts/plot_crossmodal_heatmap.py
```

Full evaluation notebook: `notebooks/polypdb_crossmodal_eval.ipynb`

---

## Related Projects

- [รู้รอบกรุง](https://github.com/Mad-m-dock/ruurobnkrung) — Thai civic RAG assistant · BDI National AI Hackathon 2026
- [Jenna OS](https://github.com/Mad-m-dock) — Production multi-agent AI system

---

*Questions or collaboration: stangykung19@gmail.com*
