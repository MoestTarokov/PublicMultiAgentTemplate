# 556-AGENT_REVIEWER_BOOT.md
# reviewer 起動カード

## 必読
- docs/001-AGENTS.md
- docs/003-GIT.md
- docs/004-TODO.md
- docs/006-DOCUMENT_STRUCTURE.md
- docs/007-ROLE_PERMISSION_MATRIX.md
- docs/100-PROJECT/100-COMPLETENESS_GATE.md

## 判定順
1. タスク種別整合
2. docs構造違反
3. 権限逸脱（007）
4. TID運用整合
5. Git規約
6. セキュリティ境界（該当時）

## 出力
- 判定: APPROVE / REQUEST_CHANGES / BLOCK
- Blocking
- Non-blocking
- 追加確認