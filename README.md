# 市民記録アーカイブ / Civic Record Archive

まちの変化（建設現場、公共施設、地域の社会課題など）を、**数年〜数十年後に誰でも使えるよう**高解像度で記録し、公開するプロジェクトです。

- **原本（高解像度）**: Internet Archive に記録ごとに1アイテムで保存（識別子 `civicarchive-<collection>-<YYYYMMDD>-<slug>`）
- **目録（このリポジトリ）**: メタデータ・説明・縮小プレビュー
- **予備**: Google Drive（原本一式のミラー） https://drive.google.com/drive/folders/1RTxsAQsRHVimEnKvqN0dQdSpZwQ1VXj7
- **ライセンス**: 原則 CC BY 4.0（記録ごとの `metadata.json` に提供者とクレジットを記載）

## コレクション
| ID | テーマ | 状態 |
|---|---|---|
| [sendai-music-hall](collections/sendai-music-hall/) | 音楽ホール等複合施設（仙台市） | 記録中 |

新しいテーマは `collections.json` に追加し、`collections/<id>/` を作ります。

## 構成
```
collections.json                  テーマ一覧
schema/metadata.schema.json       記録メタデータの定義
templates/metadata.json           新規記録の雛形
scripts/                          RAW→TIFF変換、Internet Archiveアップロード
collections/<id>/<YYYYMMDD>_<slug>/
    metadata.json  README.md  previews/
```

## 参加したい方へ
写真・資料の提供は歓迎です。[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---
Photos and documents recording civic changes (construction sites, public facilities, social issues), published for long-term public use. Originals on Internet Archive; this repository is the catalog. License: CC BY 4.0 unless noted.
