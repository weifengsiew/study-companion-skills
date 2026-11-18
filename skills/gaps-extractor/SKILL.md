---
name: gaps-extractor
description: Internal extraction support for prepare-for-test. Create immutable gap manifests from completed quiz progress when delegated or explicitly invoked.
---

# Gaps Extractor

Extract already recorded gaps without assessing answers, inferring gaps, or changing progress. An immediate correct retry does not erase an earlier gap.

When delegated by `prepare-for-test`, its approval covers new gap manifests under the approved preparation root; return created paths to the caller without requesting approval again. When invoked directly, show every planned output path and obtain explicit approval before writing. After creation, return the exact created paths.

## Commands

For one progress file:

```bash
python3 scripts/extract_gaps.py <progress-file> [--output <gaps-file>]
```

Without `--output`, return the printed JSON. Use `--force` to replace an existing output only after explicit approval.

Present extracted data as recorded evidence, not a new diagnosis. Distinguish retained assessments from individual gap statements.
