---
name: stage-by-concern
description: 作業ツリーの変更を関心ごとに分割して staging するスキル。対話型の `git add -p` をエージェントが代行する。ユーザーが「git add -p」「選択的に stage したい」「コミットを分けたい」「このリファクタとバグ修正を別コミットにしたい」「split into commits」などと言ったとき、または diff が複数の関心事を含んでいてそのまま一括コミットすべきでないと判断したときに必ず使う。実装の途中で「ここまでをまずコミットしたい」と言われたときにも使う。
---

# stage-by-concern

## スコープ

このスキルは **verified な staging area** で終わる。commit は別タスク。

merge / rebase / cherry-pick 進行中は使わない。`git status` で判定し、解消してから再開する。

## ワークフロー

### 1. 作業ツリーを把握する

```bash
git status --short
git diff
```

### 2. グループ分けの計画を立てる

diff を読み、意味論的にまとめる。次の形でユーザーに提示する:

```
Group 1: <一文で書ける説明>
  - path/to/a.ts （ファイル全体）
  - path/to/b.ts hunks 1, 3

Group 2: <一文で書ける説明>
  - path/to/c.py hunk 2
```

一文で説明できないグループはたいてい 2 つに分けるべき。

### 3. 各グループを stage する

- **ファイル全体**: `git add <path>`
- **hunk 単位**: `python3 scripts/stage-hunks.py <file> <index> [<index> ...]`（後述）

### 4. Verify

```bash
git diff --cached --stat
git diff --stat
```

意図とずれていれば `git reset HEAD <path>` で巻き戻してやり直す。

### 5. 次のグループへ

3〜4 を繰り返す。完了したら grouping を要約して報告する。

## hunk 単位 staging

`scripts/stage-hunks.py` を使う。

```
python3 scripts/stage-hunks.py <file>                    # hunk 一覧を表示
python3 scripts/stage-hunks.py <file> <index> [<index> ...]   # 0 始まり、指定 hunk を stage
```

例:

```
$ python3 scripts/stage-hunks.py util.py
util.py: 2 hunks total
  hunk 0: @@ -2,7 +2,7 @@
  hunk 1: @@ -14,6 +14,8 @@ def chunks(seq, size):

$ python3 scripts/stage-hunks.py util.py 0
staged hunks [0] from util.py
```

新規ファイルを hunk 単位で扱いたいときは先に `git add -N <path>` で intent-to-add を入れる。

### スクリプトが落ちたとき

- `no diff for <file>`: 既に全部 stage 済みか変更なし
- `hunk indices out of range`: 一覧と index がずれている。引数なしで再確認
- `git apply failed`: 直前の stage と重なっている、または hunk 内に意味の違う変更が同居していて分離不可能。grouping を見直す

hunk 内分割は本スクリプトの守備範囲外。必要なら手で patch を編集して `git apply --cached --check` → `git apply --cached` するが、事故率が高いので grouping 変更を優先する。

## ファイル単位で stage すべきケース

hunk 構造がない、または意味のある hunk として分けられない変更はファイル単位で扱う:

- 新規ファイル全体・削除ファイル
- rename
- binary ファイル
- mode change のみ
- whitespace / 改行コードのみの変更（独立グループに切り出すと後で `git log -w` で意味のある変更を追える）
- submodule pointer 更新

## グループ分けの原則

**判定基準**: そのグループ単独で revert してリポジトリが意味のある状態に戻るか。

実例:

- bug fix 1 件 = 1 グループ
- refactor 1 件 = 1 グループ。挙動変更を refactor に紛れ込ませない
- formatting のみは単独グループ
- テストの変更は対応するコード変更と同じグループ
- generated file（ロックファイル、ビルド成果物）は単独グループ
