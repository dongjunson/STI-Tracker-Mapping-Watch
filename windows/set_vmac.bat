@echo off
REM =========================================
REM  Tracker VMAC 설정 스크립트 (Windows)
REM =========================================

setlocal enabledelayedexpansion

REM Python 설치 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [오류] Python이 설치되어 있지 않습니다!
    echo.
    echo install.bat을 먼저 실행하여 환경을 설정하세요.
    echo.
    pause
    exit /b 1
)

REM pyserial 설치 확인
python -c "import serial" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [오류] pyserial이 설치되어 있지 않습니다!
    echo.
    echo install.bat을 먼저 실행하여 환경을 설정하세요.
    echo.
    pause
    exit /b 1
)

REM Python 스크립트 실행
echo.
echo Tracker VMAC 설정을 시작합니다...
echo.

python "%~dp0set_vmac.py"

REM 종료 코드 확인
if %errorlevel% neq 0 (
    echo.
    echo [오류] 스크립트 실행 중 오류가 발생했습니다.
    echo.
    pause
    exit /b %errorlevel%
)

echo.
pause

