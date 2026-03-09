# AGENTTODO.md
# Agent タスク管理（追記・状態更新）

状態:
- `[ ]` 未着手
- `[~]` 進行中
- `[x]` 完了（対応コミット済み）
- `[!]` ブロック中

ルール:
- 新規タスクは末尾追記
- TIDは `tools/tid_assigner.py` で採番
- `[x]` 更新は対応コミットと同時に確定

---

## TODO記載開始位置

- [x] #TID-1 README を docs/README.md に戻して公開前状態を整備
