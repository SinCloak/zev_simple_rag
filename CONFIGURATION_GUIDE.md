# 配置指南

本项目已使用提供的凭证预配置完成。以下是详细的配置信息。

## 凭证摘要

| 服务 | 配置项 | 值 |
|------|--------|-----|
| **Gemini API 密钥** | `gemini_api_key` | `AIzaSyCzRQ3CnG0yK8gE8zqVPYDr3eBYOgf0oCc` |
| **PostgreSQL** | 主机 | `localhost` |
| **PostgreSQL** | 端口 | `5432` |
| **PostgreSQL** | 用户 | `postgres` |
| **PostgreSQL** | 密码 | `6666` |
| **PostgreSQL** | 数据库 | `postgres` |

## 后端配置

### 环境变量

创建 `backend/.env` 文件（可选 - 默认值已设置）：

```env
# 应用
DEBUG=true

# 数据库
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=6666
DATABASE_NAME=postgres

# Gemini API
GEMINI_API_KEY=AIzaSyCzRQ3CnG0yK8gE8zqVPYDr3eBYOgf0oCc
GEMINI_MODEL=gemini-3.5-pro-preview

# Chroma 数据库
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=zev_simple_rag_1_docs

# 知识库
KNOWLEDGE_BASE_PATH=./knowledge_base

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 配置文件

主配置位于 `backend/src/core/config.py`。所有默认值都已预配置。

## 前端配置

创建 `frontend/.env.development` 文件（可选）：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 数据库设置

### PostgreSQL

确保 PostgreSQL 已安装并运行：

```bash
# 检查 PostgreSQL 是否运行（Windows）
# 使用 Services.msc 或 pgAdmin

# 或通过命令行（如果已添加到 PATH）
psql --version
```

### 数据库表

应用会在启动时自动创建以下表：
- `zev_simple_rag_1_sessions` - 聊天会话
- `zev_simple_rag_1_messages` - 聊天消息

无需手动迁移。

## 知识库

### 添加文档

1. 将 Markdown 文档添加到 `backend/knowledge_base/`
2. 系统会在启动时自动导入
3. 或通过 API 手动触发导入：
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat/ingest
   ```

### 文档结构

知识库已预填充：
- Gemini API 文档
- LangChain 文档
- Chroma DB 文档

## 运行应用

### 启动后端

```bash
cd backend
D:\PythonVenv\Scripts\python.exe -m pip install -r requirements.txt
D:\PythonVenv\Scripts\python.exe -m uvicorn src.main:app --reload
```

后端地址：http://localhost:8000
API 文档：http://localhost:8000/docs

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端地址：http://localhost:3000

## API 使用示例

### 创建会话

```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"title": "我的聊天"}'
```

### 发送聊天消息（流式）

```javascript
// 在浏览器中使用 EventSource API
const response = await fetch('/api/v1/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: '什么是 RAG？',
    session_id: 'your-session-uuid',
    enable_web_search: false,
    enable_deep_thinking: false
  })
});
```

## 故障排查

### 后端无法启动

- 检查 PostgreSQL 是否在 5432 端口运行
- 验证 PostgreSQL 凭证（用户：postgres，密码：6666）
- 检查 Python 虚拟环境是否正确：`D:\PythonVenv\Scripts\python.exe`

### 前端无法连接后端

- 确保后端在 http://localhost:8000 运行
- 检查 `backend/src/core/config.py` 中的 CORS 设置
- 验证 `frontend/vite.config.ts` 中的 API 代理

### RAG 未返回相关结果

- 检查文档是否已导入（调用 `/api/v1/chat/ingest`）
- 验证 Chroma DB 是否在 `backend/chroma_db/` 创建
- 检查文档是否为 Markdown 格式

## Gemini API

Gemini API 密钥已预配置：
- API Key: `AIzaSyCzRQ3CnG0yK8gE8zqVPYDr3eBYOgf0oCc`
- Model: `gemini-3.5-pro-preview`

要更改模型，请在 `.env` 文件中更新 `GEMINI_MODEL`。

## Git 配置

### GitHub 仓库

- 仓库：https://github.com/SinCloak/zev_simple_rag
- 邮箱：zeagglefkus@gmail.com
- 密码：zHZ48484

推送更改：

```bash
git remote add origin https://github.com/SinCloak/zev_simple_rag.git
git branch -M main
git push -u origin main
```

当提示输入凭证时：
- 用户名：zeagglefkus@gmail.com
- 密码：zHZ48484
