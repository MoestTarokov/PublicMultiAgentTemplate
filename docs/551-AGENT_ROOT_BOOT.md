## 9. AGENTOUTPUT 固定手順（必須）
1. `python tools/append_agentoutput.py --tid ... --reviewer ... --file ... --summary ... --next-action ...`
2. `python tools/lint_agentoutput.py`
3. lint 成功後にのみ `AGENTOUTPUT.md` を保持する
4. 全履歴の棚卸しが必要なときだけ `python tools/lint_agentoutput.py --all` を使う

必須ルール:
- タイムスタンプはスクリプト実行時刻を自動採用し、推定や手打ち補完を禁止する
- 追記形式は `docs/301-BRIDGE/AGENTOUTPUT.md` 冒頭テンプレに厳密準拠する
- 追記は append のみ。全文置換や既存履歴の整形をしない
- reviewer 判定は `APPROVE | REQUEST_CHANGES | BLOCK` を正とし、補足が必要な場合も canonical 判定を先頭に置く