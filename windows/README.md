# Tracker VMAC 설정 - Windows 버전

Windows에서 Tracker 장치의 VMAC(가상 MAC 주소)을 설정하기 위한 스크립트입니다.

## 📁 포함된 파일

- `set_vmac.py` - Python 메인 스크립트
- `set_vmac.bat` - 실행 배치 파일 (더블클릭으로 실행 가능)
- `install.bat` - 환경 설정 배치 파일
- `README.md` - 사용 설명서

## 📋 필수 요구사항

### 1. Python 설치
- **Python 3.7 이상** 필요
- 다운로드: https://www.python.org/downloads/

⚠️ **중요**: Python 설치 시 반드시 **"Add Python to PATH"** 옵션을 체크하세요!

### 2. USB 드라이버 설치
Tracker 장치가 FTDI 칩을 사용하는 경우:
- **FTDI VCP 드라이버** 설치 필요
- 다운로드: https://ftdichip.com/drivers/vcp-drivers/

설치 후 Tracker를 USB로 연결하면 `COM3`, `COM4` 등의 포트로 인식됩니다.

## 🚀 사용 방법

### 1단계: 환경 설정 (최초 1회)

`install.bat`을 더블클릭하거나 명령 프롬프트에서 실행:

```cmd
install.bat
```

이 스크립트는:
- Python 설치 확인
- pip 설치 확인
- pyserial 패키지 자동 설치

### 2단계: Tracker 연결

1. Tracker를 USB 케이블로 PC에 연결
2. 장치 관리자에서 COM 포트 확인
   - `Windows + X` → 장치 관리자
   - "포트(COM & LPT)" 항목에서 확인

### 3단계: VMAC 설정

`set_vmac.bat`을 더블클릭하거나 명령 프롬프트에서 실행:

```cmd
set_vmac.bat
```

스크립트 실행 후:

1. **USB 포트 자동 탐색**: COM 포트를 자동으로 찾습니다
2. **연결 진단**: Tracker와의 통신 상태를 확인
3. **VMAC 입력**: 스마트워치 MAC 뒷 4자리 입력 (예: B2C3)
4. **MAC 설정 모드 진입**: 버튼 조작 후 대기
   - 조작 방법: `[짧게 1회] + [길게 3초] 1회` → 이 조합을 3회 반복
5. **VMAC 설정 및 확인**: 자동으로 설정하고 결과 확인

## 📝 사용 예시

```
=========================================
  Tracker VMAC 자동 설정 스크립트
=========================================

==================================================
           1. USB 시리얼 포트 자동 탐색
==================================================

🔌 Tracker 포트 발견: COM4
   설명: USB Serial Port (COM4)

==================================================
            2. 시리얼 포트 설정 및 연결
==================================================

✅ 시리얼 포트 연결 완료
   포트: COM4
   Baudrate: 115200
   설정: 8N1

...

설정할 스마트워치 MAC 뒷 4자리 입력 (예: B2C3): B2C3

📝 설정할 전체 MAC 주소: AAAAAAAAB2C3
```

## 🔧 문제 해결

### Python을 찾을 수 없음
```
'python'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.
```

**해결 방법:**
1. Python을 재설치하고 "Add Python to PATH" 옵션을 체크
2. 또는 시스템 환경 변수에 Python 경로 추가

### COM 포트를 찾을 수 없음

**해결 방법:**
1. USB 케이블 재연결
2. FTDI VCP 드라이버 설치 확인
3. 장치 관리자에서 포트 상태 확인
4. 다른 USB 포트 시도

### pyserial 설치 실패

**해결 방법:**
```cmd
python -m pip install --upgrade pip
python -m pip install pyserial
```

### 권한 오류

**해결 방법:**
- 명령 프롬프트를 관리자 권한으로 실행
- 다른 프로그램(Arduino IDE, PuTTY 등)이 COM 포트를 사용 중이지 않은지 확인

## 📚 추가 정보

### 시리얼 포트 설정
- **Protocol**: Serial
- **Baud rate**: 115200
- **Data bits**: 8
- **Parity**: None
- **Stop bits**: 1
- **Flow control**: None

### MAC 설정 모드
- LED 패턴으로 모드 진입 확인 가능
- 30초 후 자동으로 재부팅
- 재부팅 전까지 AT 명령 사용 가능

## 🆘 지원

문제가 계속되면:
1. Tracker 하드웨어 매뉴얼 참조
2. USB 드라이버 재설치
3. Python 및 pyserial 버전 확인

---

**제작**: Tracker VMAC 설정 도구
**버전**: 1.0.0
**플랫폼**: Windows 10/11

