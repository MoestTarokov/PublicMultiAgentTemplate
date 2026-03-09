# 500-REPOSITORYSETUP.md
# Repository Setup（短縮版）

## 必読
- docs/001-AGENTS.md
- docs/003-GIT.md
- docs/004-TODO.md
- docs/006-DOCUMENT_STRUCTURE.md
- docs/007-ROLE_PERMISSION_MATRIX.md
- docs/100-PROJECT/100-COMPLETENESS_GATE.md
- docs/100-PROJECT/101-README_PROJECT.md

## 手順
1. docs分類軸を `101-README_PROJECT.md` に確定記載
2. `100-PROJECT/102-112` を最低1段落以上で整備
3. GO/NOTGO判定

GO条件:
- docs軸確定
- 101記入済み
- 102-112が空文化でない
- Git/TODO/構造規範と整合

NOTGO条件:
- docs軸未決定
- 必須文書未記入
- 構造矛盾

## 最終ゲート（root）
- `AGENTOUTPUT.md` に統合結果を追記
- `MEMORY.md` に再発防止を追記
- 必要時 `AGENTTODO.md` を代行更新
- bridge 管理コミットを実施