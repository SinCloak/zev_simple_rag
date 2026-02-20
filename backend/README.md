# Zev 简易 RAG 后端

RAG AI 助手的 FastAPI 后端。

## 安装

```bash
# 使用固定的虚拟环境
D:\PythonVenv\Scripts\python.exe -m pip install -r requirements.txt
```

## 运行

```bash
# 开发模式（热重载）
D:\PythonVenv\Scripts\python.exe -m uvicorn src.main:app --reload

# 或直接运行主模块
D:\PythonVenv\Scripts\python.exe -m src.main
```

## API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
src/
├── api/
│   ├── dependencies.py    # FastAPI 依赖注入
│   └── v1/
│       ├── sessions.py    # 会话管理接口
│       └── chat.py        # 聊天接口
├── application/
│   ├── dtos.py            # Pydantic 模式
│   └── services.py        # 业务逻辑
├── domain/
│   └── entities.py        # 领域模型
├── infrastructure/
│   ├── database/
│   │   ├── models.py      # SQLAlchemy 模型
│   │   └── session.py     # 数据库会话管理
│   ├── ml/
│   │   └── rag_service.py # LangChain + Chroma RAG
│   └── repositories/
│       └── session_repository.py
├── core/
│   ├── config.py          # 配置
│   └── logging.py         # 日志配置
└── main.py                # FastAPI 入口
```
