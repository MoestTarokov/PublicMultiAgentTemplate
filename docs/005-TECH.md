# 005-TECH.md
# 実行手順と補助スクリプト

## 文字コード
- テキストは UTF-8 BOM なし
- 不要な改行コード変更は禁止

## TID採番
```bash
python tools/tid_assigner.py --level parent
python tools/tid_assigner.py --level child --parent 5
python tools/tid_assigner.py --level grandchild --parent 5 --child 2
```

## コミットメッセージ lint
```bash
python tools/commit_linter.py --message "docs: ルール更新 (#TID-1-1-1)" --check-type
```

## 備考
- 詳細手順は `003-GIT.md` と `004-TODO.md` を正とする