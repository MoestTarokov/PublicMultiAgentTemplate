# 001-AGENTS.md
# 実行規範コア

## 優先順
1. `docs/000-AGENTSROOTORCHESTRATION.md`
2. `docs/007-ROLE_PERMISSION_MATRIX.md`
3. `docs/003-GIT.md`
4. `docs/004-TODO.md`

## ロール要約
- root: 分解/割当/統合/停止判断（実装禁止）
- explorer: 調査のみ
- researcher: 一次ソース調査のみ
- worker: 実装主担当
- fast_worker: 小規模実装
- reviewer: APPROVE/REQUEST_CHANGES/BLOCK 判定

## 共通原則
- 日本語・Markdownで出力
- ルール逸脱を検知したら即停止し再計画
- TODO と Git を同期させる
- ユーザー指摘を `docs/301-BRIDGE/MEMORY.md` に反映

## 禁止
- 規範無視の実装
- 合意のない仕様拡張
- 不整合の放置