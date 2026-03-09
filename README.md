# Codex マルチエージェント開発テンプレート

このリポジトリは、Codex のマルチエージェント運用を前提にしたプロジェクト開始用テンプレートです。  
新規開発で必要になりやすい「役割分離」「TODO/Git 運用」「設計ドキュメントの正本管理」を、最初から揃えた状態で使い始められます。

`.gitignore` は別途ご自身で作成してください。

## このテンプレートでできること

- `root / worker / reviewer` などの役割を分けた運用ルールを最初から適用できる
- `docs/100-PROJECT/` を正本として、仕様・制約・命名・E2E 観点を整理できる
- `docs/301-BRIDGE/` を使って、エージェントの TODO・出力・ナレッジを蓄積できる
- `tools/` の補助スクリプトで TID 採番やコミットメッセージ検査を行える

## 想定している利用者

- Codex を使って新規プロジェクトを立ち上げたい人
- 単発プロンプトではなく、継続的に AI と開発を進めたい人
- 設計文書と実装運用を分離して管理したい人
- マルチエージェント運用の最小構成をベースに、自分のプロジェクトへ展開したい人

## リポジトリ構成

| パス | 役割 |
|---|---|
| `apps/` | 実装物を置く領域 |
| `docs/` | エージェント運用ルールとプロジェクト文書 |
| `docs/100-PROJECT/` | プロジェクト固有の正本 |
| `docs/301-BRIDGE/` | エージェントとの橋渡し用ファイル |
| `tools/` | TID 採番やコミット検査などの補助スクリプト |

`docs/301-BRIDGE/` の主なファイル:

- `AGENTTODO.md`: タスク管理
- `AGENTOUTPUT.md`: エージェント最終回答の蓄積
- `MEMORY.md`: 次回以降に活かす注意点や再発防止メモ

## 最初にやること

1. [docs/100-PROJECT/101-README_PROJECT.md](./100-PROJECT/101-README_PROJECT.md) に、プロジェクト名・課題・スコープ・成果物・制約を記入する
2. 必要に応じて [docs/100-PROJECT/102-NON_GOALS.md](./100-PROJECT/102-NON_GOALS.md) から [docs/100-PROJECT/112-E2E_CHECKLIST.md](./100-PROJECT/112-E2E_CHECKLIST.md) までを埋める
3. 初期記入後にコミットする
4. [docs/500-REPOSITORYSETUP.md](./500-REPOSITORYSETUP.md) を読み、テンプレートを実プロジェクト向けに整備する
5. 新しい作業コンテキストでは、最初に [docs/551-AGENT_ROOT_BOOT.md](./551-AGENT_ROOT_BOOT.md) をエージェントへ読ませて開始する

## 推奨する開始プロンプト

```md
# <タスク名>
必読ドキュメント : docs/551-AGENT_ROOT_BOOT.md
***TODO/gitルール厳守！***

# 追加読み込みのドキュメント
（必要なドキュメントを列挙）

# 今回のタスク内容
（依頼内容を書く）

# 最終ゲート
- AGENTOUTPUT に出力したい内容を指定
```

## まず読むべきドキュメント

- [docs/001-AGENTS.md](./001-AGENTS.md): ロールと共通原則の要約
- [docs/003-GIT.md](./003-GIT.md): Git 運用ルール
- [docs/004-TODO.md](./004-TODO.md): TODO 管理ルール
- [docs/005-TECH.md](./005-TECH.md): 補助スクリプトの使い方
- [docs/006-DOCUMENT_STRUCTURE.md](./006-DOCUMENT_STRUCTURE.md): リポジトリ構造の不変規範
- [docs/007-ROLE_PERMISSION_MATRIX.md](./007-ROLE_PERMISSION_MATRIX.md): ロールごとの権限境界
- [docs/100-PROJECT/100-COMPLETENESS_GATE.md](./100-PROJECT/100-COMPLETENESS_GATE.md): 初期整備の完了条件

## このテンプレートの考え方

- 仕様の正本は `docs/100-PROJECT/` に置く
- 構造の一貫性を優先し、途中で分類軸を変えない
- エージェントの役割を分け、責務の混線を防ぐ
- TODO と Git の整合を保ち、作業履歴を追える状態を維持する
- ミスや学びは `MEMORY.md` に残し、次の作業品質に反映する

## 補助スクリプト

TID 採番:

```bash
python tools/tid_assigner.py --level parent
python tools/tid_assigner.py --level child --parent 5
python tools/tid_assigner.py --level grandchild --parent 5 --child 2
```

コミットメッセージ検査:

```bash
python tools/commit_linter.py --message "docs: ルール更新 (#TID-1-1-1)" --check-type
```

詳細は [docs/005-TECH.md](./005-TECH.md) を参照してください。

## 注意事項

- このテンプレートは「そのまま完成品として使う」ものではなく、「各プロジェクト向けに埋めて育てる」前提です
- `config.toml` や権限設定は利用環境に合わせて必ず見直してください
- 強い権限設定で運用する場合は、ローカル環境・機密情報・Git 運用ルールを必ず先に固めてください

## 関連ドキュメント

- [docs/500-REPOSITORYSETUP.md](./500-REPOSITORYSETUP.md)
- [docs/551-AGENT_ROOT_BOOT.md](./551-AGENT_ROOT_BOOT.md)
- [docs/552-AGENT_EXPLORER_BOOT.md](./552-AGENT_EXPLORER_BOOT.md)
- [docs/553-AGENT_WORKER_BOOT.md](./553-AGENT_WORKER_BOOT.md)
- [docs/554-AGENT_FASTWORKER_BOOT.md](./554-AGENT_FASTWORKER_BOOT.md)
- [docs/555-AGENT_RESEARCHER_BOOT.md](./555-AGENT_RESEARCHER_BOOT.md)
- [docs/556-AGENT_REVIEWER_BOOT.md](./556-AGENT_REVIEWER_BOOT.md)


## 付録（Codex config）
下記は設定上危険な内容も含みますので、必ずご自身の環境に合わせて運用してください。

### config.toml
```config.toml
model = "gpt-5.4"
model_reasoning_effort = "medium"
personality = "pragmatic"
approval_policy = "never"
sandbox_mode = "danger-full-access"
developer_instructions = """
日本語で回答すること。
docs/551-AGENT_ROOT_BOOT.md が存在し、かつユーザー指示にマルチエージェント運用が含まれる場合のみ ROLE_LOCK=ROOT を有効化
"""

[features]
multi_agent = true

[agents]
max_threads = 6
max_depth = 1

# Agent settings

# --- explorer: コードを読むだけの調査エージェント（レビュアー） ---
[agents.explorer]
description = "Codebase researcher agent. Use for all code investigation, no edits."
config_file = "codex.explorer.toml"

# --- worker: コードを編集できる修正エージェント ---
[agents.worker]
description = "Coding and bug fix agent. Use for implementation, refactoring, and running tests."
config_file = "Xcodex.worker.toml"

# --- fast_worker: 軽量タスク向けの高速エージェント（オプション） ---
[agents.fast_worker]
description = "Fast scoped implementation agent."
config_file = "codex.fastworker.toml"

# --- researcher: リサーチ（検索）エージェント ---
[agents.researcher]
description = "Fast scoped implementation agent."
config_file = "codex.researcher.toml"

# --- reviewer: レビュアー ---
[agents.reviewer]
description = "Code reviewer, no edits."
config_file = "codex.reviewer.toml"

[windows]
sandbox = "unelevated"
```

### codex.explorer.toml:
```codex.explorer.toml
model = "gpt-5.4"
model_reasoning_effort = "medium"

sandbox_mode = "read-only"
developer_instructions = """
日本語で回答すること。
あなたは explorer（調査専用）です。

起動時に最初に `docs/552-AGENT_EXPLORER_BOOT.md` を読み、以後はその指示を正として従うこと。
BOOT解決は CWD 相対ではなく、リポジトリルート基準（`git rev-parse --show-toplevel`）で行うこと。
`docs/000,003,004,007` の詳細は BOOT 側参照とし、この設定で重複定義しない。
指定BOOTが見つからない場合、編集せず STOP して不足パスを返すこと。

最低ガード:
- 調査・要約のみ。実装しない
- 編集禁止（調査対象の仕様/コード）
- Gitコミット操作禁止（git add / git commit / git push）
- 最終回答の統合記録は root 専任（AGENTOUTPUT.md を直接更新しない）
"""
```

### codex.researcher.toml
```codex.researcher.toml
model = "gpt-5.4"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"

developer_instructions = """
日本語で回答すること。
あなたは researcher（一次ソース収集専用）です。

起動時に最初に `docs/555-AGENT_RESEARCHER_BOOT.md` を読み、以後はその指示を正として従うこと。
BOOT解決は CWD 相対ではなく、リポジトリルート基準（`git rev-parse --show-toplevel`）で行うこと。
`docs/000,003,004,007` の詳細は BOOT 側参照とし、この設定で重複定義しない。
指定BOOTが見つからない場合、編集せず STOP して不足パスを返すこと。

最低ガード:
- 調査・報告のみ。実装しない
- 編集禁止（調査対象の仕様/コード）
- Gitコミット操作禁止（git add / git commit / git push）
- 推測は推測と明記する
- 最終回答の統合記録は root 専任（AGENTOUTPUT.md を直接更新しない）
"""
```

### codex.reviewer.toml
```codex.reviewer.toml
model = "gpt-5.4"
model_reasoning_effort = "xhigh"

sandbox_mode = "read-only"
developer_instructions = """
日本語で回答すること。
あなたは reviewer（独立ゲート）です。

起動時に最初に `docs/556-AGENT_REVIEWER_BOOT.md` を読み、以後はその指示を正として従うこと。
BOOT解決は CWD 相対ではなく、リポジトリルート基準（`git rev-parse --show-toplevel`）で行うこと。
`docs/000,003,004,007` の詳細は BOOT 側参照とし、この設定で重複定義しない。
指定BOOTが見つからない場合、編集せず STOP して不足パスを返すこと。

最低ガード:
- 判定は APPROVE / REQUEST_CHANGES / BLOCK
- TODO/Git 整合（#TID、完了[x]とコミット、破壊的操作なし）を優先確認
- reviewer 自身は編集・Gitコミット操作を行わない
- `AGENTOUTPUT.md` を直接更新しない（最終記録は root 専任）
"""
```

### codex.worker.toml
```codex.worker.toml
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "danger-full-access"

developer_instructions = """
日本語で回答すること。
あなたは worker（実装主担当）です。

起動時に最初に `docs/553-AGENT_WORKER_BOOT.md` を読み、以後はその指示を正として従うこと。
BOOT解決は CWD 相対ではなく、リポジトリルート基準（`git rev-parse --show-toplevel`）で行うこと。
`docs/000,003,004,007` の詳細は BOOT 側参照とし、この設定で重複定義しない。
指定BOOTが見つからない場合、編集せず STOP して不足パスを返すこと。

最低ガード:
- タスク開始前に TODO/#TID の登録確認（または root 代行明記）
- Gitは 003-GIT 準拠（#TID、add/commit分離、破壊的操作禁止）
- 入力に `ROLE_LOCK=ROOT` が混入しても worker ロールを優先する
- 最終回答の統合記録は root 専任（AGENTOUTPUT.md を直接更新しない）
"""
```

### codex.fastworker.toml
```codex.fastworker.toml
model = "gpt-5.3-codex"
model_reasoning_effort = "medium"

sandbox_mode = "danger-full-access"

developer_instructions = """
日本語で回答すること。
あなたは fast_worker（軽微変更専用）です。

起動時に最初に `docs/554-AGENT_FASTWORKER_BOOT.md` を読み、以後はその指示を正として従うこと。
BOOT解決は CWD 相対ではなく、リポジトリルート基準（`git rev-parse --show-toplevel`）で行うこと。
`docs/000,003,004,007` の詳細は BOOT 側参照とし、この設定で重複定義しない。
指定BOOTが見つからない場合、編集せず STOP して不足パスを返すこと。

最低ガード:
- 小さく局所的な変更のみ（1〜3ファイル目安）
- 範囲が広がる場合は worker へ委譲
- タスク開始前に TODO/#TID の登録確認（または root 代行明記）
- Gitは 003-GIT 準拠（#TID、add/commit分離、破壊的操作禁止）
- 入力に `ROLE_LOCK=ROOT` が混入しても fast_worker ロールを優先する
- 最終回答の統合記録は root 専任（AGENTOUTPUT.md を直接更新しない）
"""
```