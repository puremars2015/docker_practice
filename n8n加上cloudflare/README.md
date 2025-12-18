# n8n with Cloudflare Tunnel

這個專案使用 Docker Compose 來運行 n8n 工作流程自動化工具，並透過 Cloudflare Tunnel 讓外部可以安全訪問。

## 前置準備

1. **Cloudflare 帳號**：需要有 Cloudflare 帳號和已經添加的域名
2. **Cloudflare Tunnel Token**：需要先在 Cloudflare Zero Trust 中創建 Tunnel

## 設置 Cloudflare Tunnel

### 方法 1: 使用 Cloudflare Dashboard (推薦)

1. 登入 [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. 前往 `Access` > `Tunnels`
3. 點擊 `Create a tunnel`
4. 選擇 `Cloudflared` 類型
5. 輸入 Tunnel 名稱（例如：n8n-tunnel）
6. 複製生成的 **Tunnel Token**
7. 在 `Public Hostname` 設置中添加：
   - **Subdomain**: 你想要的子域名（例如：n8n）
   - **Domain**: 你的域名
   - **Service Type**: HTTP
   - **URL**: `http://n8n:5678`

### 方法 2: 使用命令列

```bash
# 登入 Cloudflare
cloudflared tunnel login

# 創建 tunnel
cloudflared tunnel create n8n-tunnel

# 查看 tunnel 列表和 ID
cloudflared tunnel list

# 設置 DNS 記錄
cloudflared tunnel route dns <TUNNEL-ID> n8n.yourdomain.com

# 獲取 tunnel token
cloudflared tunnel token <TUNNEL-ID>
```

## 配置

1. 編輯 `docker-compose.yml`，替換以下內容：
   - `TUNNEL_TOKEN`: 將 `your_tunnel_token_here` 替換為您的 Cloudflare Tunnel Token
   - `WEBHOOK_URL`: 將 `https://your-domain.com` 替換為您的實際域名

2. （可選）修改 n8n 的環境變數：
   - `GENERIC_TIMEZONE`: 設置時區
   - 可以添加更多 n8n 環境變數，如資料庫連接等

## 啟動服務

```bash
# 啟動所有服務
docker compose up -d

# 查看日誌
docker compose logs -f

# 查看特定服務的日誌
docker compose logs -f n8n
docker compose logs -f cloudflared

# 停止服務
docker compose down

# 停止並刪除 volumes
docker compose down -v
```

## 訪問 n8n

- **外部訪問**：https://n8n.yourdomain.com（或您設置的域名）
- **本地訪問**：http://localhost:5678

## 常用的 n8n 環境變數

可以在 `docker-compose.yml` 中添加更多環境變數：

```yaml
environment:
  # 基本設置
  - N8N_BASIC_AUTH_ACTIVE=true
  - N8N_BASIC_AUTH_USER=your_username
  - N8N_BASIC_AUTH_PASSWORD=your_password
  
  # 執行模式
  - EXECUTIONS_MODE=queue
  
  # 日誌
  - N8N_LOG_LEVEL=info
  
  # 加密密鑰（重要！請設置唯一的密鑰）
  - N8N_ENCRYPTION_KEY=your_encryption_key_here
```

## 安全建議

1. 設置 n8n 的基本認證或使用 Cloudflare Access 來保護您的 n8n 實例
2. 定期備份 n8n_data volume
3. 使用強密碼和加密密鑰
4. 定期更新 Docker 映像檔

## 故障排除

### 檢查服務狀態
```bash
docker compose ps
```

### 查看 Cloudflared 連接狀態
```bash
docker compose logs cloudflared
```

如果看到 "Connection established" 表示 tunnel 連接成功。

### n8n 無法訪問
1. 確認 Cloudflare Tunnel 的 Public Hostname 設置正確
2. 確認 Service URL 設置為 `http://n8n:5678`
3. 檢查 Docker 網絡連接

## 備份與恢復

### 備份
```bash
docker run --rm -v n8n加上cloudflare_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### 恢復
```bash
docker run --rm -v n8n加上cloudflare_n8n_data:/data -v $(pwd):/backup alpine tar xzf /backup/n8n-backup-YYYYMMDD.tar.gz -C /data
```
