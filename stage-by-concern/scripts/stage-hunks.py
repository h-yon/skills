#!/usr/bin/env python3
"""特定の git diff ハンクだけをインデックスにステージする。

git add -p の自動化版。指定したファイルの 0-indexed なハンク番号だけを
パッチとして取り出し、git apply --cached で当てる。

usage:
  python3 stage-hunks.py <file>                       # ハンク一覧を表示
  python3 stage-hunks.py <file> <index> [<index> ...]  # 指定ハンクを stage

base は index（git add -p と同じ）。staged 済みの差分は無視する。
新規ファイルを hunk 単位で扱いたいときは先に `git add -N <file>`。
"""
from __future__ import annotations

import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1

    file_path = sys.argv[1]
    try:
        indices = sorted({int(s) for s in sys.argv[2:]})
    except ValueError:
        print('hunk indices must be integers', file=sys.stderr)
        return 1

    diff = subprocess.check_output(
        ['git', 'diff', '--no-ext-diff', '--', file_path],
        text=True,
    )
    if not diff:
        print(f'no diff for {file_path}', file=sys.stderr)
        return 1

    header: list[str] = []
    hunks: list[list[str]] = []
    current: list[str] | None = None
    for line in diff.split('\n'):
        if line.startswith('@@'):
            if current is not None:
                hunks.append(current)
            current = [line]
        elif current is None:
            header.append(line)
        else:
            current.append(line)
    if current is not None:
        hunks.append(current)

    # 引数なし: 一覧表示して終了
    if not indices:
        print(f'{file_path}: {len(hunks)} hunks total', file=sys.stderr)
        for i, h in enumerate(hunks):
            print(f'  hunk {i}: {h[0]}', file=sys.stderr)
        return 0

    out_of_range = [i for i in indices if i < 0 or i >= len(hunks)]
    if out_of_range:
        print(f'{file_path}: {len(hunks)} hunks total', file=sys.stderr)
        print(f'hunk indices out of range: {out_of_range}', file=sys.stderr)
        return 1

    selected = [hunks[i] for i in indices]
    patch_body = '\n'.join('\n'.join(h) for h in selected)
    patch = '\n'.join(header) + '\n' + patch_body
    if not patch.endswith('\n'):
        patch += '\n'

    proc = subprocess.run(
        ['git', 'apply', '--cached', '-'],
        input=patch.encode(),
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        print('git apply failed:', file=sys.stderr)
        print(proc.stderr.decode(), file=sys.stderr)
        return 1

    print(f'staged hunks {indices} from {file_path}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
