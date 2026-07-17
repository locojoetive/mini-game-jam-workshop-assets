"""Export each visible layer of every PSD file as an individual PNG.

Usage:
    python export_psd_layers.py <target_dir>

Each visible top-level layer is saved as <psd_name>-<layer_name>.png in the
same directory as the source PSD.  If multiple layers share the same name,
a numeric index is appended: <psd_name>-<layer_name>-<index>.png.
Hidden layers are skipped.  The original PSD file is removed after export.
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
    psd_name = sanitize(psd_path.stem)

    # Collect visible layers and count name occurrences
    visible_layers = []
    name_counts: dict[str, int] = {}
    for layer in psd:
        if not layer.is_visible():
            print(f"  Überspringe versteckte Ebene: {layer.name}")
            continue
        base = sanitize(layer.name)
        visible_layers.append((layer, base))
        name_counts[base] = name_counts.get(base, 0) + 1

    # Export with index suffix only for duplicate names
    name_indices: dict[str, int] = {}
    for layer, base in visible_layers:
        if name_counts[base] > 1:
            idx = name_indices.get(base, 0)
            name_indices[base] = idx + 1
            filename = f"{psd_name}-{base}-{idx}.png"
        else:
            filename = f"{psd_name}-{base}.png"

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
