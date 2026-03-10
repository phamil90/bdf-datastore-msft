from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import bdf
from bdf.io import save


@dataclass
class ConversionFailure:
    path: Path
    reason: str


@dataclass
class UnsupportedInput:
    path: Path
    reason: str


def iter_raw_files(root: Path) -> list[Path]:
    raw_files: list[Path] = []
    for raw_dir in sorted(p for p in root.rglob("raw") if p.is_dir()):
        for candidate in sorted(p for p in raw_dir.rglob("*") if p.is_file()):
            raw_files.append(candidate)
    return raw_files


def target_path_for(raw_file: Path) -> Path:
    raw_dir = raw_file.parent
    while raw_dir.name != "raw":
        raw_dir = raw_dir.parent
    relative_under_raw = raw_file.relative_to(raw_dir)
    processed_dir = raw_dir.parent / "processed"
    return (processed_dir / relative_under_raw).with_suffix(".bdf.csv")


def convert_file(raw_file: Path) -> None:
    df = bdf.read(raw_file, validate=True)
    save(df, target_path_for(raw_file), index=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert all files below raw/ folders into sibling processed/*.bdf.csv files."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to scan for raw/ folders.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    raw_files = iter_raw_files(root)
    failures: list[ConversionFailure] = []
    unsupported: list[UnsupportedInput] = []
    converted = 0

    for raw_file in raw_files:
        sniff = bdf.detect(raw_file)
        if sniff.id == "abstract" or sniff.confidence <= 0:
            unsupported.append(
                UnsupportedInput(
                    path=raw_file,
                    reason="unsupported by batterydf auto-detection",
                )
            )
            continue

        try:
            convert_file(raw_file)
            converted += 1
        except Exception as exc:  # noqa: BLE001
            failures.append(ConversionFailure(path=raw_file, reason=str(exc)))

    print(f"Scanned {len(raw_files)} raw files")
    print(f"Converted {converted} files")
    print(f"Skipped unsupported {len(unsupported)} files")
    print(f"Failed {len(failures)} files")

    if unsupported:
        print("\nUnsupported:", file=sys.stderr)
        for item in unsupported:
            rel_path = item.path.relative_to(root)
            print(f"- {rel_path}: {item.reason}", file=sys.stderr)

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            rel_path = failure.path.relative_to(root)
            print(f"- {rel_path}: {failure.reason}", file=sys.stderr)

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
