Polis 生データ（仙台 音楽ホール等複合施設 試験運用）
会話ID 6sphpcbrdc / レポートID r9tycfbapkdbhwks7dixn
取得日時: 2026-11-01 JST（Polisのレポート出力APIから取得）
運営: 音楽堂ホールを考える会・畠山紳悟
ライセンス: CC BY 4.0（出典を書けば転載・加工は自由）

個人情報の扱い:
- 参加者は匿名。メールアドレス・氏名・アカウント名は含まれない。
- voter-id / author-id / participant は Polis が振った連番で、個人は特定できない。
- 自由記述（意見の本文）は、参加者が投稿した文面そのまま。

ファイル:
- votes.csv              投票の全記録（timestamp, comment-id, voter-id, vote）。vote: 1=賛成, -1=反対, 0=わからない。同じ人が同じ意見に複数回投票した場合は全て残っている（集計では最後の1票を使った）
- comments.csv           全意見（moderated: 1=表示中, -1=運営者が非表示にした, 0=未処理）
- participant-votes.csv  参加者ごとの全投票の一覧（行列形式）とグループ番号
- comment-groups.csv     意見ごとの、グループ別の賛成・反対・わからない数
- summary.csv            会話全体の概要
- daily_progress.csv     日別の参加者数の推移（votes.csv から作成）
- statements_all_72.csv  全72本の意見（本文・状態・提出者区分・投票数）。提出者区分の「運営者」は author-id 0 と 7（運営者の2つの投稿枠）

注意: 意見の取り下げ・追加は 2026-10-13 に行った。意見番号は取り下げ後も欠番にならず残る。
