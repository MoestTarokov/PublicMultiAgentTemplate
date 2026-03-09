# 553-AGENT_WORKER_BOOT.md
# worker 起動カード

## 必読
- docs/001-AGENTS.md
- docs/003-GIT.md
- docs/004-TODO.md
- docs/007-ROLE_PERMISSION_MATRIX.md

## 開始ゲート
1. `git status --porcelain`
2. AGENTTODO に TID 登録
3. 対象孫タスクを `[~]` に更新
4. `[~]` 行に `owner` と初回 `hb` を記載

## 実施
- 実装/修正/テストを最小差分で実行
- 長時間作業時は 10分目安で `hb` を更新
- ブロック時は `[!]` に更新し `note` を記載
- root からの進捗確認には、作業を中断せず `hb` 更新で応答する（明示キャンセル時を除く）

## 完了ゲート
1. 対象孫タスクを `[x]` に更新
2. `git add` -> `commit_linter` -> `git commit`
3. `git status --porcelain` 確認
4. reviewer へ提出
