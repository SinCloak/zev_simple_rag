@echo off
chcp 65001 >nul
title Zev 简易 RAG AI 助手 - 一键启动

echo ========================================
echo    Zev 简易 RAG AI 助手
echo ========================================
echo.

REM 检查 Python 虚拟环境
if not exist "D:\PythonVenv\Scripts\python.exe" (
    echo [错误] 未找到 Python 虚拟环境: D:\PythonVenv\Scripts\python.exe
    pause
    exit /b 1
)

REM 检查后端目录
if not exist "backend\requirements.txt" (
    echo [错误] 未找到后端项目目录
    pause
    exit /b 1
)

REM 检查前端目录
if not exist "frontend\package.json" (
    echo [错误] 未找到前端项目目录
    pause
    exit /b 1
)

echo [信息] 正在启动后端服务...
start "Zev RAG - 后端" cmd /k "cd /d %~dp0backend && D:\PythonVenv\Scripts\python.exe -m uvicorn src.main:app --reload"

timeout /t 3 /nobreak >nul

echo [信息] 正在启动前端服务...
start "Zev RAG - 前端" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo    启动完成！
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo 前端地址: http://localhost:3000
echo.
echo 按任意键关闭此窗口（后端和前端将继续运行）...
pause >nul
