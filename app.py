from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

MOVIES_CSV = "movies_100k.csv"
RATINGS_CSV = "ratings_100k.csv"

# ---------------------------
# 1. 映画データ読み込み
# ---------------------------
movies_df = pd.read_csv(
    MOVIES_CSV,
    sep="|"
)

# movie_id を int 型に揃える
movies_df.rename(columns={"movie_id": "movie_id"}, inplace=True)
movies_df["movie_id"] = movies_df["movie_id"].astype(int)

# タイトル列
movies_df["title"] = movies_df["movie_title"]

# ---------------------------
# 2. 評価データ読み込み
# ---------------------------
ratings_df = pd.read_csv(
    RATINGS_CSV,
    sep=","
)

ratings_df = ratings_df.rename(
    columns={"userId": "user_id", "movieId": "movie_id"}
)

ratings_df["movie_id"] = ratings_df["movie_id"].astype(int)

# ---------------------------
# 3. ピボットテーブル
# ---------------------------
ratings_pivot = ratings_df.pivot_table(
    index="user_id",
    columns="movie_id",
    values="rating"
)

# ---------------------------
# 4. 類似度行列（映画同士）
# ---------------------------
similarity_matrix = cosine_similarity(ratings_pivot.T.fillna(0))
similarity_df = pd.DataFrame(
    similarity_matrix,
    index=ratings_pivot.columns,
    columns=ratings_pivot.columns
)

# ---------------------------
# 5. 全体の平均評価（未選択時）
# ---------------------------
top_general_movies = (
    ratings_df.groupby("movie_id")["rating"].mean()
    .sort_values(ascending=False)
    .head(5)
    .index.tolist()
)

# ---------------------------
# 6. トップページ
# ---------------------------
@app.route("/")
def index():
    movie_list = movies_df[["movie_id", "title"]].head(500).to_dict(orient="records")
    return render_template("index.html", movies=movie_list)

# ---------------------------
# 7. おすすめ処理
# ---------------------------
@app.route("/recommend", methods=["POST"])
def recommend():
    selected = request.form.getlist("movies")

    if len(selected) == 0:
        # 未選択時
        recommended_ids = top_general_movies
        message = "（選択がありませんでした — 総合評価の高い映画を表示しています）"
    else:
        selected = list(map(int, selected))

        # 類似度スコア合計
        sim_scores = np.sum(similarity_df[selected], axis=1)

        # 選択映画を除外
        for sid in selected:
            sim_scores[sid] = -1

        recommended_ids = sim_scores.sort_values(ascending=False).head(5).index.tolist()
        message = "（あなたの選んだ映画に基づいておすすめを表示しています）"

    # 映画情報取得（空対策）
    recommended_movies = movies_df[movies_df["movie_id"].isin(recommended_ids)]

    return render_template(
        "result.html",
        movies=recommended_movies.to_dict(orient="records"),
        message=message
    )

# ---------------------------
# 8. Flask 起動
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
