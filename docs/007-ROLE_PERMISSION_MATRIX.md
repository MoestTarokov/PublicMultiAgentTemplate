# 007-ROLE_PERMISSION_MATRIX.md
# ロール権限マトリクス（正本）

目的：権限逸脱を防ぎ、責務分離を固定する。

| ロール | 実装編集 | docs一般編集 | BRIDGE編集（AGENTTODO/AGENTOUTPUT/MEMORY） | コミット |
|---|---|---|---|---|
| root | 禁止 | 原則禁止 | 許可 | 許可（bridge管理のみ） |
| explorer | 禁止 | 禁止 | 禁止 | 禁止 |
| researcher | 禁止 | 禁止 | 禁止 | 禁止 |
| worker | 許可 | 許可（担当範囲） | AGENTTODOの担当TIDのみ許可 | 許可 |
| fast_worker | 許可（軽微） | 許可（担当範囲） | AGENTTODOの担当TIDのみ許可 | 許可 |
| reviewer | 禁止 | 禁止 | 禁止 | 禁止 |

root の例外許可（実装禁止は維持）：
- `docs/301-BRIDGE/AGENTTODO.md` の代行更新
- `docs/301-BRIDGE/AGENTOUTPUT.md` の統合追記
- `docs/301-BRIDGE/MEMORY.md` の教訓追記
- 上記3ファイルのみを対象とした bridge 管理コミット

BLOCK 条件：
- 権限外編集/コミット
- root が実装差分を含むコミットを実施