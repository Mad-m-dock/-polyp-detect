"""
Cross-modality generalization evaluation.

Train on WLI → test on NBI / BLI / FICE / LCI with zero additional training.
Measures how well a single WLI model generalizes across all endoscopy lighting types.

Usage:
    python src/cross_modality_eval.py \
        --weights runs/train/yolov11s_wli/weights/best.pt \
        --data_root ./data/polypdb_wli
"""

import argparse
import shutil
import tempfile
from pathlib import Path

import pandas as pd


MODALITIES = ['WLI', 'NBI', 'BLI', 'FICE', 'LCI']

PAPER_BEST = {
    'WLI':  0.925,
    'NBI':  0.688,
    'BLI':  0.688,
    'FICE': 0.887,
    'LCI':  0.995,
}


def build_modality_split(data_root: Path, modality: str, split: str = 'test') -> Path:
    src_img = data_root / 'images' / split
    src_lbl = data_root / 'labels' / split

    tmp = Path(tempfile.mkdtemp(prefix=f'eval_{modality}_'))
    (tmp / 'images').mkdir()
    (tmp / 'labels').mkdir()

    copied = 0
    for img in src_img.iterdir():
        if not img.name.startswith(modality):
            continue
        lbl = src_lbl / (img.stem + '.txt')
        shutil.copy2(img, tmp / 'images' / img.name)
        if lbl.exists():
            shutil.copy2(lbl, tmp / 'labels' / lbl.name)
        copied += 1

    yaml_path = tmp / 'data.yaml'
    yaml_path.write_text(
        f"path: {tmp}\ntrain: images\nval: images\ntest: images\nnc: 1\nnames: ['polyp']\n"
    )
    return tmp, yaml_path, copied


def evaluate(model, yaml_path: Path):
    m = model.val(data=str(yaml_path), split='test', verbose=False, plots=False)
    return {
        'mAP@50':    round(m.box.map50, 4),
        'Precision': round(m.box.mp, 4),
        'Recall':    round(m.box.mr, 4),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', required=True, help='Path to best.pt')
    parser.add_argument('--data_root', default='data/polypdb_wli', help='YOLO dataset root')
    parser.add_argument('--split', default='test')
    args = parser.parse_args()

    from ultralytics import YOLO
    model = YOLO(args.weights)
    data_root = Path(args.data_root)

    rows = []
    for mod in MODALITIES:
        tmp_dir, yaml_path, n_images = build_modality_split(data_root, mod, args.split)
        if n_images == 0:
            print(f'{mod}: no images found — skipping')
            shutil.rmtree(tmp_dir)
            continue

        metrics = evaluate(model, yaml_path)
        shutil.rmtree(tmp_dir)

        delta = metrics['mAP@50'] - PAPER_BEST.get(mod, 0)
        rows.append({
            'Modality':    mod,
            'Images':      n_images,
            'mAP@50':      f"{metrics['mAP@50']*100:.1f}%",
            'Precision':   f"{metrics['Precision']*100:.1f}%",
            'Recall':      f"{metrics['Recall']*100:.1f}%",
            'Paper best':  f"{PAPER_BEST.get(mod, 0)*100:.1f}%",
            'Delta':       f"{delta*100:+.1f}pp",
        })
        print(f"{mod:5s} ({n_images:3d} imgs): mAP@50={metrics['mAP@50']*100:.1f}%  "
              f"P={metrics['Precision']*100:.1f}%  R={metrics['Recall']*100:.1f}%  "
              f"vs paper {PAPER_BEST.get(mod,0)*100:.1f}% ({delta*100:+.1f}pp)")

    print('\n' + '='*65)
    print('CROSS-MODALITY SUMMARY')
    print('='*65)
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print('='*65)


if __name__ == '__main__':
    main()
