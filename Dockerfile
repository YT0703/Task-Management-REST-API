# Dockerfile

# ベースイメージの指定
FROM python:3.10-slim-buster

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY ./app /app/app

# Alembicの実行
# アプリケーション起動時にDBマイグレーションを実行するためのエントリーポイント
# `alembic upgrade head` は、DBスキーマを最新の状態に更新します
COPY alembic.ini .
COPY alembic /app/alembic
RUN alembic upgrade head

# FastAPIアプリケーションを起動
# ホスト0.0.0.0で公開し、ポート8000でリッスン
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



