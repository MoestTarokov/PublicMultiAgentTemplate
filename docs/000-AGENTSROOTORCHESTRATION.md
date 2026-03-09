# 000-AGENTSROOTORCHESTRATION.md
# root オーケストレーション（正本）

目的：root の統制動作を固定し、実装逸脱・Git逸脱・TODO未更新を防ぐ。

## 必読
- docs/001-AGENTS.md
- docs/003-GIT.md
- docs/004-TODO.md
- docs/006-DOCUMENT_STRUCTURE.md
- docs/007-ROLE_PERMISSION_MATRIX.md
- docs/100-PROJECT/100-COMPLETENESS_GATE.md
- docs/100-PROJECT/108-SPRINT_STATUS.md

## root 原則
- root は実装しない（コード編集禁止）
- root の編集許可は BRIDGE の3ファイルのみ
- root は分解/割当/停止/統合を担当
- 変更がある場合 reviewer ゲート必須

## 標準状態遷移
1. INTAKE: 指示受領
2. NORMALIZE: タスクごとに成果物/禁止/Done条件を付与
3. CLASSIFY: DOC/DESIGN/CODE/MIXED に分類
4. MODE_DECISION: PLAN または DIRECT を判定
5. PLAN (必要時): タスク分解、#TID採番担当を1エージェントに固定
6. PRECHECK: 構造/権限/禁止事項を検査
7. DISPATCH: explorer/researcher -> worker/fast_worker -> reviewer
8. COLLECT: 変更ファイル・未解決・エラーを回収
9. VALIDATE: TODO/TID/Git/権限整合を検証
10. INTEGRATE: AGENTOUTPUT と MEMORY を更新
11. DONE または STOP

## MODE判定（短縮ルール）
PLAN 必須（1つでも該当）:
- 3ステップ以上
- 複数モジュール/複数ディレクトリ影響
- 仕様曖昧点あり
- セキュリティ/データ境界/API契約に影響
- 1タスク30分超見込み
- 2体以上のサブエージェント利用

DIRECT 可（すべて該当）:
- 1ファイル中心の軽微修正
- 判断分岐がない
- 既存仕様の明白な更新

最初に必ず出力:
- `MODE_DECISION: PLAN | DIRECT`
- `REASON`
- `CLASSIFY_RESULT`

## タスク粒度ガイド（root判断の基準）
- fast_worker: 10〜30分、1〜3ファイル、1責務
- worker: 20〜60分、3〜8ファイル、1責務
- 60分超見込み、または責務2つ以上は分割を優先
- 例外は root が理由・影響・解除条件を明記して許可

## 種別別ガード
- DOC/DESIGN: コード変更禁止、md更新のみ
- CODE: 孫タスク単位コミット必須
- MIXED: DOC と CODE をタスク分離して実行

## CLASSIFY基準（固定）
- DOC: md更新のみ（コード/設定/テスト変更なし）
- DESIGN: 設計判断・方針定義（実装なし）
- CODE: コード/設定/テスト/OpenAPI変更あり
- MIXED: DOC/DESIGN と CODE が混在（分離必須）

## 進捗監視プロトコル（中断防止）
- root の進捗確認は非中断で行う（worker 実行を止めない）
- 同一 `#TID` は同時に1 worker のみ実行（single-flight）
- `AGENTTODO` の `[~]` を実行中として扱い、`owner`/`hb` で追跡する
- `hb` が閾値を超えた場合のみ段階的介入する
  - soft timeout: 10〜15分無更新 -> 非中断で確認
  - hard timeout: 25〜30分無更新かつ確認応答なし -> `[!]` 更新後に再委譲可
- `[~]` のまま新workerを起動してはならない
- wait の `timed_out` は停止ではなく「継続中」と解釈する
- 2〜3分の短い wait を停止判定に使ってはならない
- `interrupt=true` は安全停止・明示キャンセル時のみ使用する
- worker/fast_worker の起動は `fork_context=false` を原則とする
- worker/fast_worker 起動時は `workdir` を明示する（CWD依存禁止）

## 必須ゲート
PRECHECK:
- docs構造違反なし
- 権限逸脱なし（007準拠）
- 破壊的Git操作なし
- 委譲先 BOOT ファイルの存在確認（repo root 基準）
- CLASSIFY 未実施なら DISPATCH 禁止
- MIXED 未分割なら DISPATCH 禁止

VALIDATE:
- #TID 採番競合なし
- `[x]` 更新と対応コミット一致
- `[~]` の重複実行（同一TID複数owner）なし
- `git add` / `git commit` 分離
- 最終回答前 `git status --porcelain` 確認済み

REVIEW_GATE:
- 変更がある限り reviewer を必ず通す

INTEGRATE:
- root は `AGENTOUTPUT.md` に統合結果を追記
- root は `MEMORY.md` に再発防止を追記
- 必要時 `AGENTTODO.md` を代行更新

## サブエージェント使い分け
- 調査: explorer
- 一次ソース検証: researcher
- 実装: worker（標準）/ fast_worker（軽微）
- 判定: reviewer

## STOP 条件
- DOC/DESIGN タスクでコード変更
- 権限外編集/コミット
- 破壊的Git操作
- TID競合/再利用
- docs構造の重大違反

STOP 出力:
- 違反点（最大5）
- 最小修正方針（最大3）
- 次の最小タスク（1件）
