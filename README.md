# sato_AIkaihatuouyouKadai3

# 映画レコメンデーション Web アプリ  
Flask とレコメンドアルゴリズムを用いて、ユーザーが選択した映画に類似した作品をおすすめ表示する Web アプリです。  
映画を選択せず送信した場合は、全体の平均評価が高い映画を自動的に表示します。

---

## 📌 使用技術

- Python 3.x
- Flask
- Pandas
- Scikit-learn（cosine_similarity）
- HTML（Jinja2 Template）

---

## 📁 ディレクトリ構成

project_root/
├─ app.py # Flask アプリ本体
├─ movies_100k.csv # 映画データ
├─ ratings_100k.csv # 評価データ
└─ templates/
├─ index.html # トップページ（映画選択）
└─ result.html # おすすめ表示ページ

yaml
コードをコピーする

---

## 📊 使用データ

### 🎬 movies_100k.csv  
MovieLens データセットを元にした映画リスト。  
区切り文字：`|`  
主な列：

| 列名 | 内容 |
|------|------|
| movie_id | 映画ID |
| movie_title | 映画タイトル |
| release_date | 公開日 |
| IMDb URL | IMDbページ |
| （以降）ジャンルフラグ | Action / Adventure / ... |

本アプリでは `movie_id` と `movie_title` を使用します。

---

### ⭐ ratings_100k.csv  
区切り文字：`,`  
主な列：

| 列名 | 内容 |
|-------|------|
| userId | ユーザーID |
| movieId | 映画ID |
| rating | 評価（1〜5） |

本アプリではピボットテーブルに使用します。

---

## 🧠 アルゴリズム概要

映画同士の類似度を求めるため、次のステップで計算します。

### ① ピボットテーブル生成  
rows = ユーザー
columns = 映画ID
values = rating

yaml
コードをコピーする

### ② 類似度計算  
`cosine_similarity` により映画同士の類似度を算出します。

### ③ 推薦結果生成
- ユーザーが選択した映画の類似スコアを合算  
- 自分で選んだ映画は除外  
- 上位 5 件をおすすめとして表示  

### ④ 未選択時
- 評価の平均値が高い映画 Top5 を表示

---

## ▶ 実行方法

### 1. 必要ライブラリのインストール

pip install flask pandas scikit-learn

shell
コードをコピーする

### 2. Flask アプリの起動

python app.py

shell
コードをコピーする

### 3. ブラウザでアクセス  
http://127.0.0.1:5000

yaml
コードをコピーする

---

## 💻 画面説明

### 🏠 index.html  
- 映画タイトルの一覧  
- 複数選択可能なチェックボックス  
- 「おすすめを表示」ボタン

### 🎬 result.html  
- 選択した映画に基づくおすすめ映画を 5 件表示  
- 未選択の場合は「総合評価の高い映画」を表示  
- 戻るボタンでトップへ

---

## 🛠 トラブルシューティング

### ❗ TemplateNotFound: result.html  
`templates` フォルダの場所が間違っています。  
必ず以下の構造にしてください：

app.py
templates/
├ index.html
└ result.html

yaml
コードをコピーする

---

### ❗ 類似度計算でエラーが出る  
- ratings_100k.csv が空または列名が異なる  
- movie_id が int になっていない  
- movies_100k.csv の区切り文字が違う

---

## 📄 ライセンス

MovieLens データセット（各 CSV）は  
GroupLens（https://grouplens.org/datasets/movielens/）  
のライセンスに従い使用しています。

---

## 📘 補足・拡張案

- ジャンルをタグ表示  
- 作品のポスター画像を TMDb API で取得  
- おすすめ結果の説明追加  
- ソート機能（人気順 / 評価順）  
- 機械学習モデルの追加（SVD, kNNなど）  

---

## 👨‍🏫 作成者

授業課題・演習用のサンプルとして作成。  
アプリの改善・機能追加もサポートできます！
