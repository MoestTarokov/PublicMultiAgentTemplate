#!/usr/bin/env python3
"""
TID Assigner
-------------

This script assists with automatic assignment of task IDs (TIDs) for the
AgentCodingTemplateMulti project. It reads the current `AGENTTODO.md` and
archived TODO files to find existing task IDs and then proposes the next
available identifier. Use this tool to avoid manual numbering errors.

Usage examples:

```
# Assign next parent task ID
python tid_assigner.py --level parent

# Assign next child task ID under parent 5
python tid_assigner.py --level child --parent 5

# Assign next grandchild task ID under parent 5, child 3
python tid_assigner.py --level grandchild --parent 5 --child 3

# Specify custom locations if the docs directory differs
python tid_assigner.py --level parent --todo-path docs/301-BRIDGE/AGENTTODO.md --archive-dir docs/301-BRIDGE/ARCHIVE
```

The script assumes that TIDs follow the pattern:

```
#TID-X
#TID-X-Y
#TID-X-Y-Z
```

Where X is the parent ID, Y is the child ID, and Z is the grandchild ID. It ignores
any entries that are not of this form.
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

TID_PATTERN = re.compile(r"#TID-(\d+)(?:-(\d+))?(?:-(\d+))?")


def extract_tids_from_file(path: Path) -> List[Tuple[int, int, int]]:
    """Extract all TID tuples (parent, child, grandchild) from a Markdown file.

    Missing components are represented as None.

    Args:
        path: Path to the Markdown file.

    Returns:
        A list of tuples (parent, child, grandchild). Missing values are None.
    """
    tids: List[Tuple[int, int, int]] = []
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return tids
    for match in TID_PATTERN.finditer(content):
        parent = int(match.group(1))
        child = int(match.group(2)) if match.group(2) is not None else None
        grandchild = int(match.group(3)) if match.group(3) is not None else None
        tids.append((parent, child, grandchild))
    return tids


def collect_all_tids(todo_path: Path, archive_dir: Path) -> List[Tuple[int, int, int]]:
    """Collect TIDs from the main AGENTTODO and all archive files.

    Args:
        todo_path: Path to AGENTTODO.md.
        archive_dir: Directory containing archived AGENTTODO files.

    Returns:
        A combined list of all (parent, child, grandchild) IDs.
    """
    tids: List[Tuple[int, int, int]] = []
    tids.extend(extract_tids_from_file(todo_path))
    if archive_dir.is_dir():
        for file in archive_dir.iterdir():
            if file.is_file() and file.name.startswith("AGENTTODO") and file.suffix == ".md":
                tids.extend(extract_tids_from_file(file))
    return tids


def next_parent_id(tids: List[Tuple[int, int, int]]) -> int:
    """Return the next available parent ID."""
    parents = [tid[0] for tid in tids]
    return max(parents) + 1 if parents else 1


def next_child_id(tids: List[Tuple[int, int, int]], parent: int) -> int:
    """Return the next available child ID under a given parent."""
    children = [tid[1] for tid in tids if tid[0] == parent and tid[1] is not None]
    return max(children) + 1 if children else 1


def next_grandchild_id(tids: List[Tuple[int, int, int]], parent: int, child: int) -> int:
    """Return the next available grandchild ID under a given parent and child."""
    grandchildren = [tid[2] for tid in tids if tid[0] == parent and tid[1] == child and tid[2] is not None]
    return max(grandchildren) + 1 if grandchildren else 1


def main():
    parser = argparse.ArgumentParser(description="Assign next available TID based on existing tasks.")
    parser.add_argument("--level", choices=["parent", "child", "grandchild"], required=True,
                        help="Level of TID to assign (parent, child, grandchild)")
    parser.add_argument("--parent", type=int, help="Parent ID (required for child/grandchild)")
    parser.add_argument("--child", type=int, help="Child ID (required for grandchild)")
    parser.add_argument("--todo-path", type=Path, default=Path("docs/301-BRIDGE/AGENTTODO.md"),
                        help="Path to the main AGENTTODO.md")
    parser.add_argument("--archive-dir", type=Path, default=Path("docs/301-BRIDGE/ARCHIVE"),
                        help="Directory containing archived AGENTTODO files")
    args = parser.parse_args()

    tids = collect_all_tids(args.todo_path, args.archive_dir)
    if args.level == "parent":
        new_id = next_parent_id(tids)
        print(f"#TID-{new_id}")
    elif args.level == "child":
        if args.parent is None:
            raise SystemExit("--parent is required when level=child")
        new_id = next_child_id(tids, args.parent)
        print(f"#TID-{args.parent}-{new_id}")
    elif args.level == "grandchild":
        if args.parent is None or args.child is None:
            raise SystemExit("--parent and --child are required when level=grandchild")
        new_id = next_grandchild_id(tids, args.parent, args.child)
        print(f"#TID-{args.parent}-{args.child}-{new_id}")


if __name__ == "__main__":
    main()