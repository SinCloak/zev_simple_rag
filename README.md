# Zev 简易 RAG AI 助手

一个功能强大且易于使用的 RAG（检索增强生成）AI 助手，采用 FastAPI 后端和 Vue3 前端。

## 功能特性

- 🤖 **AI 对话**：基于 Gemini 3.5 Pro 的对话界面
- 📚 **RAG 系统**：内置 Chroma 向量数据库知识库
- 💬 **会话管理**：聊天历史和上下文持久化
- 📝 **Markdown 渲染**：美观的 AI 响应格式展示
- 📊 **Token 统计**：详细的 Token 消耗明细
- 🔄 **流式响应**：实时 AI 响应
- 📖 **引用展示**：显示 RAG 答案使用的参考来源
- 🌐 **网络搜索**：可选网络搜索功能（可配置）
- 🧠 **深度思考**：可选深度思考模式（可配置）

## 技术栈

### 后端
- **FastAPI**：现代、快速的 Python Web 框架
- **SQLAlchemy 2.0**：PostgreSQL 异步 ORM
- **LangChain**：RAG 框架
- **Chroma**：向量数据库
- **Gemini API**：Google 的大语言模型
- **PostgreSQL**：会话持久化存储

### 前端
- **Vue 3**：渐进式 JavaScript 框架
- **TypeScript**：类型安全开发
- **Vite**：快速构建工具
- **Pinia**：状态管理
- **Marked**：Markdown 解析器
- **Highlight.js**：代码语法高亮

## 项目结构

```
zev_simple_rag_1/
├── backend/
│   ├── src/
│   │   ├── api/              # API 路由
│   │   ├── application/      # 应用服务
│   │   ├── domain/           # 领域实体
│   │   ├── infrastructure/   # 数据库、RAG、仓储
│   │   ├── core/             # 配置、日志
│   │   └── main.py           # FastAPI 入口
│   ├── knowledge_base/       # Markdown 文档
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # API 客户端
│   │   ├── components/       # Vue 组件
│   │   ├── router/           # Vue 路由
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── types/            # TypeScript 类型
│   │   ├── views/            # 页面组件
│   │   └── main.ts
│   └── package.json
└── README.md
```

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### 后端设置

1. **安装依赖**：
   ```bash
   cd backend
   D:\PythonVenv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. **配置 PostgreSQL**：
   - 确保 PostgreSQL 在 5432 端口运行
   - 默认账号：用户 `postgres`，密码 `6666`

3. **启动后端**：
   ```bash
   D:\PythonVenv\Scripts\python.exe -m uvicorn src.main:app --reload
   ```

   后端地址：http://localhost:8000
   API 文档：http://localhost:8000/docs

### 前端设置

1. **安装依赖**：
   ```bash
   cd frontend
   npm install
   ```

2. **启动前端**：
   ```bash
   npm run dev
   ```

   前端地址：http://localhost:3000

## 配置说明

详见 [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) 了解详细配置选项。

## API 接口

### 会话管理
- `POST /api/v1/sessions` - 创建新会话
- `GET /api/v1/sessions` - 列出所有会话
- `GET /api/v1/sessions/{id}` - 获取会话及消息
- `PUT /api/v1/sessions/{id}` - 更新会话
- `DELETE /api/v1/sessions/{id}` - 删除会话

### 聊天
- `POST /api/v1/chat` - 发送聊天消息（非流式）
- `POST /api/v1/chat/stream` - 发送聊天消息（流式）
- `POST /api/v1/chat/ingest` - 从知识库导入文档

## 知识库

将 Markdown 文档添加到 `backend/knowledge_base/` 目录。系统会自动：
- 加载 `.md` 文件
- 将文档分块
- 存储到 Chroma 向量数据库
- 对话时检索相关文档

## 数据库表

所有表都以 `zev_simple_rag_1_` 为前缀：
- `zev_simple_rag_1_sessions` - 聊天会话
- `zev_simple_rag_1_messages` - 聊天消息（含 token 使用和引用）

## 许可证

MIT
