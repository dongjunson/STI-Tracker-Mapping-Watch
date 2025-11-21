# Tracker VMAC 설정 - Windows

Tracker 장치의 VMAC(가상 MAC 주소)을 설정하는 Python 스크립트입니다.

## 🚀 Quick Start

```cmd
REM 1. pyserial 설치
python -m pip install pyserial

REM 2. 실행
python set_vmac.py
```

## 📋 사전 요구사항

1. **Windows 10/11**
2. **Python 3.7 이상** (⚠️ 설치 시 "Add Python to PATH" 옵션 필수!)
3. **pyserial 라이브러리**
4. **USB 케이블** 및 Tracker 장치

💡 **참고**: Windows 10/11은 대부분의 USB-Serial 드라이버를 자동으로 설치합니다.  
만약 포트가 인식되지 않을 경우에만 FTDI VCP 드라이버를 설치하세요.

## 💿 설치

### 1. Python 설치
https://www.python.org/downloads/ 에서 다운로드

⚠️ **중요**: 설치 시 반드시 **"Add Python to PATH"** 체크!

### 2. pyserial 설치
```cmd
python -m pip install pyserial
```

### 3. USB 드라이버 (선택사항)

💡 **대부분의 경우 드라이버 자동 설치됨**

Windows 10/11은 USB-Serial 장치를 자동으로 인식합니다.  
Tracker를 USB로 연결하면 보통 자동으로 `COM3`, `COM4` 등으로 인식됩니다.

**드라이버 수동 설치가 필요한 경우:**
- 장치 관리자에서 "알 수 없는 장치"로 표시될 때
- 포트를 찾을 수 없다는 오류가 발생할 때

**FTDI VCP 드라이버 다운로드:**  
https://ftdichip.com/drivers/vcp-drivers/

## 📱 사용 방법

### 1단계: Tracker 연결
USB 케이블로 Tracker를 PC에 연결합니다.

### 2단계: 스크립트 실행

**방법 1: 명령 프롬프트 (권장)**
```cmd
python set_vmac.py
```

**방법 2: PowerShell**
```powershell
python .\set_vmac.py
```

**방법 3: 더블클릭**
`set_vmac.py` 파일을 직접 더블클릭

### 3단계: 안내에 따라 진행
1. **포트 자동 탐색**: COM 포트를 자동으로 찾습니다
2. **연결 진단**: Tracker 응답 확인
3. **MAC 주소 입력**: 뒷 4자리 입력 (예: B2C3)
4. **MAC 설정 모드 진입**: 
   - 버튼 조작: `[짧게 1회] + [길게 3초] 1회` → 이 조합을 3회 반복
5. **VMAC 설정**: 자동으로 설정 및 확인
6. **전체 설정 확인**: AT+SCFG로 현재 설정 정보 확인
7. **재부팅**: 필요시 재부팅

## 📸 실행 예시

```
==================================================
  Tracker VMAC 자동 설정 스크립트 (Windows)
==================================================

🔌 Tracker 포트 발견: COM4
   설명: USB Serial Port (COM4)

✅ 시리얼 포트 연결 완료
   포트: COM4
   Baudrate: 115200

설정할 스마트워치 MAC 뒷 4자리 입력 (예: B2C3): B2C3
📝 설정할 전체 MAC 주소: AAAAAAAAB2C3
```

## ⚙️ 시리얼 통신 설정

- **Protocol**: Serial
- **Baud rate**: 115200
- **Data bits**: 8
- **Parity**: None
- **Stop bits**: 1
- **Flow control**: None

## 🔧 문제 해결

### Python을 찾을 수 없음
```
'python'은(는) 내부 또는 외부 명령... 아닙니다.
```

**해결 방법:**
1. Python 재설치 시 "Add Python to PATH" 체크
2. `python` 대신 `py` 명령어 시도:
   ```cmd
   py set_vmac.py
   ```

### pyserial이 없음
```cmd
python -m pip install pyserial

REM 네트워크 문제가 있는 경우
python -m pip install --upgrade pip
python -m pip install pyserial --user
```

### COM 포트를 찾을 수 없음

스크립트가 포트를 자동으로 찾지 못하는 경우:

**해결 방법:**
1. USB 케이블 재연결
2. 다른 USB 포트 시도
3. PC 재부팅 (드라이버 자동 설치 대기)
4. 다른 프로그램이 COM 포트를 사용 중인지 확인
   - Arduino IDE, PuTTY, 시리얼 터미널 등 종료
5. 장치 관리자에서 확인 (`Windows + X` → 장치 관리자)
   - "포트(COM & LPT)" 항목에서 COM 포트 확인
   - "알 수 없는 장치"가 있으면 → 우클릭 → 드라이버 업데이트
6. 위 방법으로도 안 되면 FTDI VCP 드라이버 수동 설치

### 포트 접근 권한 오류

**해결 방법:**
- 명령 프롬프트를 **관리자 권한**으로 실행
- 다른 프로그램이 포트를 사용 중이지 않은지 확인

### AT+VMAC 명령 응답 없음

**가장 흔한 원인**: MAC 설정 모드 미진입
- 버튼 조작: `[짧게 1회] + [길게 3초] 1회` → 이 조합을 3회 반복
- LED 패턴이 변경되는지 확인

## ⚠️ 주의사항

- MAC 주소 뒷 4자리는 **16진수 4자리** (예: B2C3)
- 앞 8자리는 자동으로 `AAAAAAAA`로 고정됨
- 영문(A-F)과 숫자(0-9)만 입력 가능
- 콜론(:) 없이 입력
- **MAC 설정 모드에서만 AT 명령 작동**
- 스크립트 실행 중 다른 프로그램에서 같은 포트 사용 금지

## 📚 FAQ

**Q: Tracker 로그가 보이지 않습니다.**  
A: 정상일 수 있습니다. Tracker는 항상 로그를 출력하지 않으며, MAC 설정 모드에서만 AT 명령에 응답합니다.

**Q: MAC 주소 형식은?**  
A: 뒷 4자리만 입력 (예: B2C3) → 전체: AAAAAAAAB2C3

**Q: 어떤 USB 칩셋을 지원하나요?**  
A: FTDI, CH340, Prolific 등 대부분의 USB-Serial 칩셋 지원

**Q: 스크립트가 포트를 찾지 못합니다.**  
A: 
1. USB 케이블을 다시 연결하세요
2. PC를 재부팅하세요 (Windows가 자동으로 드라이버 설치)
3. 장치 관리자(`Windows + X`)에서 "알 수 없는 장치" 확인
4. 여전히 안 되면 FTDI VCP 드라이버를 수동 설치하세요

## 🔗 유용한 링크

- **Python 다운로드**: https://www.python.org/downloads/
- **FTDI VCP 드라이버**: https://ftdichip.com/drivers/vcp-drivers/

---

**버전**: 0.8.0  
**플랫폼**: Windows 10/11  
**Python**: 3.7+

