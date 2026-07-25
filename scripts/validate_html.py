"""Small offline validator for the standalone HTML tools."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_MARKERS = ("<!DOCTYPE html>", "<canvas", "<script", "</html>")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker.lower() not in text.lower():
            errors.append(f"{path}: missing marker {marker!r}")
    if "http://" in text or "https://" in text:
        errors.append(f"{path}: external URL found; tool should remain standalone")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: validate_html.py FILE [FILE ...]", file=sys.stderr)
        return 2
    failures: list[str] = []
    for raw in argv[1:]:
        failures.extend(validate(Path(raw)))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Validated {len(argv) - 1} standalone HTML tool(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
