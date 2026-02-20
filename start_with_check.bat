@echo off
chcp 65001 >nul
title Zev 简易 RAG AI 助手 - 启动（带依赖检查）

echo ========================================
echo    Zev 简易 RAG AI 助手
echo ========================================
echo.

REM 设置项目根目录
set "PROJECT_ROOT=%~dp0
set "BACKEND_DIR=%PROJECT_ROOT%backend
set "FRONTEND_DIR=%PROJECT_ROOT%frontend

echo [1/5] 检查环境...

REM 检查 Python
echo [检查] Python 虚拟环境...
if not exist "D:\PythonVenv\Scripts\python.exe" (
    echo [错误] 未找到 Python 虚拟环境: D:\PythonVenv\Scripts\python.exe
    pause
    exit /b 1
)
echo [OK] Python 虚拟环境已找到

REM 检查后端依赖
echo [检查] 后端 Python 依赖...
cd /d "%BACKEND_DIR%"
D:\PythonVenv\Scripts\python.exe -c "import fastapi, uvicorn, sqlalchemy, langchain" >nul 2>&1
if errorlevel 1 (
    echo [提示] 后端依赖未安装，正在安装...
    D:\PythonVenv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 后端依赖安装失败
        pause
        exit /b 1
    )
)
echo [OK] 后端依赖已就绪

REM 检查 Node.js 和前端依赖
echo [检查] 前端 Node.js 依赖...
cd /d "%FRONTEND_DIR%"
if not exist "node_modules" (
    echo [提示] 前端依赖未安装，正在安装...
    call npm install
    if errorlevel 1 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
)
echo [OK] 前端依赖已就绪

echo.
echo [2/5] 环境检查完成！
echo.
echo [3/5] 启动后端服务...
start "Zev RAG - 后端" cmd /k "cd /d %BACKEND_DIR% && D:\PythonVenv\Scripts\python.exe -m uvicorn src.main:app --reload"

timeout /t 3 /nobreak >nul

echo [4/5] 启动前端服务...
start "Zev RAG - 前端" cmd /k "cd /d %FRONTEND_DIR% && npm run dev"

echo.
echo [5/5] 启动完成！
echo.
echo ========================================
echo    服务信息
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo 前端地址: http://localhost:3000
echo.
echo 提示: 关闭本窗口不会影响后端和前端运行
echo.
pause
