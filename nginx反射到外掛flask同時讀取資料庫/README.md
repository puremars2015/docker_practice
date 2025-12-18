# Flask + Nginx + MySQL 反向代理專案

這個專案展示了如何使用 Docker Compose 建立一個完整的 Web 應用，包含：
- Nginx 反向代理
- Flask 應用程式
- MySQL 資料庫

## 專案結構

```
.
├── docker-compose.yml       # Docker Compose 配置
├── nginx.conf               # Nginx 配置
├── init.sql                 # 資料庫初始化腳本
└── app/
    ├── app.py               # Flask 應用程式
    ├── Dockerfile           # Flask 容器配置
    ├── requirements.txt     # Python 依賴套件
    └── templates/           # HTML 模板
        ├── index.html
        └── about.html
```

## 功能說明

### 資料庫 API 端點

- `GET /api/users` - 獲取所有使用者列表
- `GET /api/users/<id>` - 獲取單一使用者資訊
- `POST /api/users` - 新增使用者
- `PUT /api/users/<id>` - 更新使用者資訊
- `DELETE /api/users/<id>` - 刪除使用者
- `GET /api/db-test` - 測試資料庫連線

### 環境變數

- `DB_HOST`: 資料庫主機 (預設: mysql)
- `DB_PORT`: 資料庫端口 (預設: 3306)
- `DB_USER`: 資料庫使用者 (預設: flask_user)
- `DB_PASSWORD`: 資料庫密碼 (預設: flask_password)
- `DB_NAME`: 資料庫名稱 (預設: flask_db)

## 使用方式

### 啟動服務

```bash
docker-compose up -d
```

### 停止服務

```bash
docker-compose down
```

### 查看日誌

```bash
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f flask
docker-compose logs -f mysql
```

## API 測試範例

### 1. 測試資料庫連線

```bash
curl http://localhost/api/db-test
```

### 2. 獲取所有使用者

```bash
curl http://localhost/api/users
```

### 3. 獲取單一使用者

```bash
curl http://localhost/api/users/1
```

### 4. 新增使用者

```bash
curl -X POST http://localhost/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"陳八","email":"chen@example.com"}'
```

### 5. 更新使用者

```bash
curl -X PUT http://localhost/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"張三改名","email":"zhang_new@example.com"}'
```

### 6. 刪除使用者

```bash
curl -X DELETE http://localhost/api/users/1
```

## 資料庫連線資訊

- 主機: localhost
- 端口: 3306
- 資料庫: flask_db
- 使用者: flask_user
- 密碼: flask_password
- Root 密碼: root_password

## 服務端口

- Nginx (HTTP): 80
- Nginx (備用): 8080
- MySQL: 3306
- Flask (內部): 5050

## 初始資料

資料庫會在首次啟動時自動初始化，並插入 5 筆範例資料：
- 張三 (zhang@example.com)
- 李四 (li@example.com)
- 王五 (wang@example.com)
- 趙六 (zhao@example.com)
- 錢七 (qian@example.com)

## 故障排除

### 重建容器

```bash
docker-compose down -v
docker-compose up -d --build
```

### 查看容器狀態

```bash
docker-compose ps
```

### 進入 MySQL 容器

```bash
docker exec -it mysql mysql -u flask_user -pflask_password flask_db
```

### 查看資料表

```sql
SHOW TABLES;
SELECT * FROM users;
```
