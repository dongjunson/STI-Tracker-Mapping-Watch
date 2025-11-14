@echo off
REM =========================================
REM  Tracker Windows 환경 설정 스크립트
REM =========================================

echo.
echo =========================================
echo   Tracker Windows 환경 설정 스크립트
echo =========================================
echo.

REM Python 설치 확인
echo [1/3] Python 설치 확인 중...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [오류] Python이 설치되어 있지 않습니다!
    echo.
    echo Python 다운로드: https://www.python.org/downloads/
    echo.
    echo 설치 시 주의사항:
    echo   - "Add Python to PATH" 옵션을 반드시 체크하세요!
    echo   - Python 3.7 이상 버전을 설치하세요.
    echo.
    pause
    exit /b 1
)

python --version
echo Python 설치 확인 완료!
echo.

REM pip 확인
echo [2/3] pip 설치 확인 중...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [오류] pip가 설치되어 있지 않습니다!
    echo.
    echo Python을 재설치하거나 다음 명령을 실행하세요:
    echo   python -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

python -m pip --version
echo pip 설치 확인 완료!
echo.

REM pyserial 설치
echo [3/3] pyserial 패키지 설치 중...
echo.
python -m pip install --upgrade pyserial
if %errorlevel% neq 0 (
    echo.
    echo [오류] pyserial 설치 실패!
    echo.
    echo 수동 설치 방법:
    echo   python -m pip install pyserial
    echo.
    pause
    exit /b 1
)

echo.
echo =========================================
echo   설치 완료!
echo =========================================
echo.
echo 이제 set_vmac.bat을 실행하여 Tracker를 설정할 수 있습니다.
echo.
pause

