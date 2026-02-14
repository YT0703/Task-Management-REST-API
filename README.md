# 🔐 Auth Task API（JWT認証付きREST APIサンプル）

FastAPI + SQLAlchemy + JWT を用いて開発した  
**実務レベルの認証付きREST APIサーバー実装サンプル** です。

ユーザー登録・ログイン・JWT認証・タスクCRUDを備え、  
実際のバックエンド開発現場を想定した設計・構成で構築しています。

---

## 🚀 主な機能

- ユーザー登録 / ログイン
- JWT認証（ステートレス認証）
- パスワードbcryptハッシュ化
- 認証必須API
- タスクCRUD（自分のデータのみ操作可能）
- Swagger自動APIドキュメント
- pytestによる自動テスト
- Dockerでワンコマンド起動

---

## 🛠 使用技術

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Auth / Security
- JWT（python-jose）
- passlib（bcrypt）

### Database
- SQLite（開発）
- PostgreSQL（本番想定）

### Dev / Test
- pytest
- Docker / docker-compose
- Black / Ruff

---

## 🏗 アーキテクチャ

責務分離を意識したクリーンアーキテクチャ構成。

app/
├─ main.py
├─ routers/
├─ services/
├─ repositories/
├─ models/
├─ schemas/
├─ core/
└─ tests/

### 設計ポイント
- ビジネスロジックをService層へ分離
- DBアクセスをRepository層に集約
- 型ヒント徹底
- テストしやすい構成
- 保守性・拡張性を重視

---

## 🔑 API例

| Method | Endpoint | 説明 |
|--------|-----------|-----------|
| POST | /auth/register | ユーザー登録 |
| POST | /auth/login | ログイン（JWT取得） |
| GET | /tasks | タスク一覧取得（認証必須） |
| POST | /tasks | タスク作成 |
| PUT | /tasks/{id} | タスク更新 |
| DELETE | /tasks/{id} | タスク削除 |
|Swagger |UI

### pytest

- 認証テスト
- CRUDテスト
- 異常系（401/403）テスト

---

## 🎯 工夫した点

- JWTによるステートレス認証実装
- bcryptによる安全なパスワード管理
- ユーザーごとのアクセス制御（認可）
- クリーンアーキテクチャによる責務分離
- pytestによる自動テスト整備
- Dockerによる環境統一
- Cursor（AIエディタ）を活用した設計レビュー・リファクタリング

---

## 📚 このプロジェクトで習得したスキル

- REST API設計
- 認証/認可（JWT）
- DB設計・ORM操作
- テスト駆動開発
- Docker環境構築
- 実務を意識した保守性の高いコード設計

---

## 🔮 今後の改善予定

- Refresh Token対応
- 権限管理（Role）
- PostgreSQL本番運用
- CI/CD導入
- APIテスト自動化

---

## 👤 Author

Pythonバックエンドエンジニア志望  
ポートフォリオとして開発

