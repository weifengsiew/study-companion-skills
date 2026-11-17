---
name: gaps-extractor
description: Internal extraction support for prepare-for-test. Create immutable gap manifests from completed quiz progress when delegated or explicitly invoked.
---

# Gaps Extractor

Extract already recorded gaps without assessing answers, inferring gaps, or changing progress. An immediate correct retry does not erase an earlier gap.

Before writing an output file or directory, identify every exact planned path. When delegated, return them to the caller, which must inform the learner and obtain explicit approval before extraction; when invoked directly, do this yourself. After creation, return the exact created paths.

## Commands

For one progress file:

```bash
python3 scripts/extract_gaps.py <progress-file> [--output <gaps-file>]
```

Without `--output`, return the printed JSON. Use `--force` to replace an existing output only after explicit approval.

For a completed `prepare-for-test` pass:

```bash
python3 scripts/extract_gap_directory.py <completed-pass-progress-dir> <new-pass-gaps-dir>
```

Directory mode requires a new output directory. It creates ordered, provenance-bearing `<topic>-gaps.json` files only for topics with gaps and an aggregate `_manifest.json`. Never regenerate or replace this directory.

Present extracted data as recorded evidence, not a new diagnosis. Distinguish retained assessments from individual gap statements.
