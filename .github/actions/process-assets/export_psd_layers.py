"""Export each visible layer of every PSD file as an individual PNG.

Usage:
    python export_psd_layers.py <target_dir>

Each visible top-level layer is saved as <sanitized_layer_name>.png in the
same directory as the source PSD.  Hidden layers are skipped.  The original
PSD file is removed after successful export.
"""

import os
import pathlib
import re
import sys

from psd_tools import PSDImage


def sanitize(name: str) -> str:
    """Replace spaces with underscores and strip non-alphanumeric chars."""
    name = name.strip()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w\-.]", "", name)
    return name or "layer"


def export_psd(psd_path: pathlib.Path) -> None:
    """Export all visible layers of a single PSD file as PNGs."""
    print(f"Verarbeite PSD: {psd_path}")
    psd = PSDImage.open(psd_path)
    out_dir = psd_path.parent
    used_names: dict[str, int] = {}

    for layer in psd:
        if not layer.is_visible():
            print(f"  Überspringe versteckte Ebene: {layer.name}")
            continue

        base = sanitize(layer.name)

        # Handle name collisions
        if base in used_names:
            used_names[base] += 1
            filename = f"{base}_{used_names[base]}.png"
        else:
            used_names[base] = 0
            filename = f"{base}.png"

        out_path = out_dir / filename
        layer_image = layer.composite()
        layer_image.save(out_path)
        print(f"  Exportiert: {out_path}")

    os.remove(psd_path)
    print(f"  PSD entfernt: {psd_path}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python export_psd_layers.py <target_dir>", file=sys.stderr)
        sys.exit(1)

    target_dir = sys.argv[1]
    psd_files = list(pathlib.Path(target_dir).rglob("*.psd"))

    if not psd_files:
        print("Keine PSD-Dateien gefunden — überspringe.")
        return

    for psd_path in psd_files:
        export_psd(psd_path)


if __name__ == "__main__":
    main()
