# 554-AGENT_FASTWORKER_BOOT.md
# fast_worker 起動カード

## 必読
- docs/001-AGENTS.md
- docs/003-GIT.md
- docs/004-TODO.md
- docs/007-ROLE_PERMISSION_MATRIX.md

## 対象
- 1〜3ファイル程度の軽微変更
- 目安時間は 10〜30分

## 開始/完了ゲート
- worker と同一（TODO状態更新、lint、コミット、reviewer提出）
- `[~]` 行の `owner/hb` 記載と 10分目安の `hb` 更新を行う
- root からの進捗確認には、作業を中断せず `hb` 更新で応答する（明示キャンセル時を除く）

## 禁止
- 大規模リファクタ
- ディレクトリ再編
- 破壊的Git操作
