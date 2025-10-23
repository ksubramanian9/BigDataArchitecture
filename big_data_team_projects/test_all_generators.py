#!/usr/bin/env python3
"""Utility to run the synthetic data generator for every config with a small sample."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List


def discover_configs(config_root: Path) -> List[Path]:
    """Return a sorted list of JSON config files under ``config_root``."""
    if not config_root.exists():
        raise FileNotFoundError(f"Config directory not found: {config_root}")
    return sorted(config_root.rglob("*.json"))


def load_format(config_path: Path) -> str:
    with config_path.open("r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    return cfg.get("output", {}).get("format", "csv")


def run_generator(
    generator: Path,
    config: Path,
    output: Path,
    records: int,
    python_executable: str,
) -> subprocess.CompletedProcess:
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        python_executable,
        str(generator),
        "--config",
        str(config),
        "--out",
        str(output),
        "--n",
        str(records),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base_dir = Path(__file__).resolve().parent
    parser.add_argument(
        "--generator",
        type=Path,
        default=base_dir / "generator_template.py",
        help="Path to generator_template.py",
    )
    parser.add_argument(
        "--config-root",
        type=Path,
        default=base_dir / "synth_configs",
        help="Root directory containing JSON configuration files",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=base_dir / "test_outputs",
        help="Directory where sample files will be written",
    )
    parser.add_argument(
        "--records",
        type=int,
        default=100,
        help="Number of records to generate for each config",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python interpreter to use when invoking the generator",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    configs = discover_configs(args.config_root)
    if not configs:
        print(f"No configuration files found under {args.config_root}")
        return 1

    successes = 0
    failures = 0

    for config_path in configs:
        format_hint = load_format(config_path)
        try:
            relative_config = config_path.relative_to(args.config_root)
        except ValueError:
            relative_config = Path(config_path.name)
        output_suffix = ".jsonl" if format_hint == "jsonl" else ".csv"
        output_path = (args.output_root / relative_config).with_suffix(output_suffix)

        print(
            f"Running generator for {relative_config} -> "
            f"{output_path.relative_to(args.output_root)}"
        )
        result = run_generator(args.generator, config_path, output_path, args.records, args.python)

        if result.returncode == 0:
            successes += 1
            if result.stdout:
                print(result.stdout.strip())
        else:
            failures += 1
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)

    print()
    print(f"Completed runs: {successes} succeeded, {failures} failed")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
