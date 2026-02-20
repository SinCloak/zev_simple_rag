@echo off
chcp 65001 >nul
title 停止 Zev RAG 服务

echo ========================================
echo    停止 Zev RAG 服务
echo ========================================
echo.

echo [信息] 正在停止 Python (uvicorn)...
taskkill /FI "WINDOWTITLE eq Zev RAG - 后端*" /T /F >nul 2>&1

echo [信息] 正在停止 Node.js (vite)...
taskkill /FI "WINDOWTITLE eq Zev RAG - 前端*" /T /F >nul 2>&1

echo [信息] 正在清理 Python 进程...
taskkill /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" /T /F >nul 2>&1

echo [信息] 正在清理 Node.js 进程...
taskkill /IM node.exe /FI "WINDOWTITLE eq *npm*" /T /F >nul 2>&1

echo.
echo [完成] 所有服务已停止
echo.
pause
