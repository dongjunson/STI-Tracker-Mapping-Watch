# Tracker MAC 설정 자동 스크립트

macOS와 Windows에서 Tracker 장치의 MAC 주소를 자동으로 설정하는 스크립트입니다.

## Quick Start

### macOS
```bash
# 1. 설치
./install.sh

# 2. 실행 (Python 버전 권장)
./set_vmac.py
```

### Windows
```cmd
REM 1. 설치
cd windows
install.bat

REM 2. 실행
set_vmac.bat
```

## 버전 비교

| 항목 | Python (set_vmac.py) ⭐ | Bash (set_mac.sh) |
|------|------------------------|-------------------|
| 설치 | pyserial 필요 | 추가 설치 불필요 |
| 안정성 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 응답 확인 | 명확하고 실시간 | 불안정할 수 있음 |
| 에러 처리 | 우수 | 보통 |
| 가독성 | 컬러 출력 | 기본 출력 |
| 에러 발생 | 없음 | Assertion 에러 가능 |

## 버전

### Python 버전 (set_vmac.py) - 권장 ⭐

**장점:**
- ✅ 시리얼 포트 설정이 정확하고 안정적
- ✅ AT 명령 응답을 실시간으로 명확하게 확인
- ✅ 에러 처리가 우수
- ✅ 컬러 출력으로 가독성 향상
- ✅ Assertion 에러 없음

**단점:**
- pyserial 설치 필요

### Bash 버전 (set_mac.sh)

**장점:**
- ✅ 추가 설치 불필요 (screen 기본 제공)

**단점:**
- ⚠️ screen 로그 수집이 불안정할 수 있음
- ⚠️ 일부 macOS 버전에서 Assertion 에러 발생 가능

## 사전 요구사항

### Python 버전 (set_vmac.py - 권장)
#### macOS
1. **macOS 시스템**
2. **Python 3.6 이상**
3. **pyserial 라이브러리**
4. **USB 케이블** 및 Tracker 장치

#### Windows
1. **Windows 10/11**
2. **Python 3.7 이상** (설치 시 "Add Python to PATH" 옵션 필수!)
3. **pyserial 라이브러리**
4. **FTDI VCP 드라이버** (USB 드라이버)
5. **USB 케이블** 및 Tracker 장치

### Bash 버전 (set_mac.sh - macOS 전용)
1. **macOS 시스템**
2. **screen 명령어** (macOS에 기본 포함)
3. **USB 케이블** 및 Tracker 장치

## 시리얼 통신 설정

스크립트는 다음 시리얼 통신 설정을 사용합니다:

- **Baud rate**: 115200
- **Data bits**: 8
- **Parity**: None
- **Stop bits**: 1
- **Flow control**: None

이 설정은 Tracker 매뉴얼에 명시된 표준 설정입니다.

## 설치 방법

### macOS - 빠른 설치 (자동)

```bash
./install.sh
```

이 명령은 자동으로:
- Python 확인
- pyserial 설치
- 실행 권한 부여

### Windows - 빠른 설치 (자동)

```cmd
cd windows
install.bat
```

이 명령은 자동으로:
- Python 확인
- pip 확인
- pyserial 설치

### 수동 설치

#### macOS - Python 버전 (권장)

1. pyserial 설치:
```bash
pip3 install pyserial
# 또는
pip3 install -r requirements.txt
```

2. 스크립트에 실행 권한 부여:
```bash
chmod +x set_vmac.py
```

#### macOS - Bash 버전

1. 스크립트에 실행 권한 부여:
```bash
chmod +x set_mac.sh
```

#### Windows - 수동 설치

1. Python 설치 (https://www.python.org/downloads/)
   - ⚠️ **중요**: "Add Python to PATH" 옵션 반드시 체크!

2. pyserial 설치:
```cmd
python -m pip install pyserial
```

3. FTDI VCP 드라이버 설치 (https://ftdichip.com/drivers/vcp-drivers/)

## 사용 방법

### macOS - Python 버전 (권장)

1. Tracker 장치를 USB 케이블로 Mac에 연결합니다.

2. 스크립트 실행:
```bash
./set_vmac.py
# 또는
python3 set_vmac.py
```

### macOS - Bash 버전

1. Tracker 장치를 USB 케이블로 Mac에 연결합니다.

2. 스크립트 실행:
```bash
./set_mac.sh
```

### Windows

1. Tracker 장치를 USB 케이블로 PC에 연결합니다.

2. 장치 관리자에서 COM 포트 확인 (선택사항):
   - `Windows + X` → 장치 관리자
   - "포트(COM & LPT)" 항목에서 확인

3. 스크립트 실행:
```cmd
cd windows
set_vmac.bat
```

또는 `windows\set_vmac.bat` 파일을 더블클릭

## 실행 단계 (공통)

3. 스크립트가 자동으로 시리얼 포트를 찾습니다.

4. **Tracker 연결 진단 (자동)**
   - 스크립트가 Enter 키를 전송하여 Tracker 응답을 테스트합니다.
   - Tracker 로그(LED, Button 등)가 보이면 정상 연결된 것입니다.
   - **참고**: Tracker는 항상 로그를 출력하지는 않습니다. 로그가 없어도 MAC 설정 모드에서는 정상 동작합니다.
   - 진단 완료 후 다음 단계로 진행합니다.

5. **스마트워치 MAC 주소 입력**
   - 뒷 4자리를 입력합니다 (4자리 16진수, 형식: `XXXX`).
   - 앞 8자리는 자동으로 `AAAAAAAA`로 채워집니다.
   - 입력은 영문과 숫자만 허용됩니다 (0-9, A-F).
   - 예: `B2C3`을 입력하면 → `AAAAAAAAB2C3`로 설정됩니다.

6. **Tracker MAC 설정 모드 진입**
   - 버튼 조작: [짧게 1회] + [길게 3초] 1회 → 이 조합을 3회 반복
   - MAC 설정 모드로 진입한 후 Enter 키를 누릅니다.
   - **중요**: MAC 설정 모드에서만 AT+VMAC 명령이 작동합니다.

7. **자동 VMAC 설정 및 확인**
   - 현재 설정된 VMAC 조회 (설정 전)
   - 새로운 VMAC 설정 (`AT+VMAC=AAAAAAAAXXXX`)
   - 설정된 VMAC 확인 (설정 후)

8. 필요시 Tracker 재부팅 (`AT+RBOT`)을 선택합니다.

## 문제 해결

### AT+VMAC 명령 응답이 없는 경우

**가장 흔한 원인: MAC 설정 모드에 진입하지 않음**
- AT+VMAC 명령은 **MAC 설정 모드에서만** 작동합니다
- 버튼 조작: [짧게 1회] + [길게 3초] 1회 → 이 조합을 3회 반복
- LED 패턴이 변경되는지 확인

**기타 원인:**
- 시리얼 통신 설정 오류 → Python 버전 사용 권장
- 포트가 다른 프로그램에서 사용 중
- USB 케이블 문제

### Tracker 로그가 보이지 않는 경우
- **정상일 수 있음**: Tracker는 항상 로그를 출력하지는 않습니다
- MAC 설정 모드에서만 AT 명령에 응답하므로 로그 없이도 진행 가능
- Tracker 버튼을 눌러 LED 반응이 있는지 확인
- 다른 USB 포트를 시도

### 시리얼 포트를 찾을 수 없는 경우

#### macOS
- USB 케이블이 제대로 연결되었는지 확인하세요.
- 다른 USB 포트를 시도해보세요.
- `ls /dev/cu.*` 명령어로 사용 가능한 포트를 확인할 수 있습니다.

#### Windows
- USB 케이블 재연결
- FTDI VCP 드라이버 설치 확인
- 장치 관리자에서 포트 상태 확인 (`Windows + X` → 장치 관리자)
- 다른 USB 포트 시도
- 다른 프로그램(Arduino IDE, PuTTY 등)이 COM 포트를 사용 중이지 않은지 확인

### Python을 찾을 수 없음 (Windows)
```
'python'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.
```

**해결 방법:**
1. Python을 재설치하고 "Add Python to PATH" 옵션을 체크
2. 또는 시스템 환경 변수에 Python 경로 추가

### screen 명령어 오류 (macOS)
- macOS에는 screen이 기본 포함되어 있습니다.
- 없다면 Homebrew로 설치: `brew install screen`

### 권한 오류 (macOS)
- 스크립트에 실행 권한이 있는지 확인: `chmod +x set_mac.sh`

## 주의사항

- 스마트워치 MAC 주소 뒷 4자리는 반드시 16진수 4자리 문자열이어야 합니다 (예: `B2C3`).
- 앞 8자리(`AAAAAAAA`)는 자동으로 고정됩니다.
- 입력은 영문과 숫자만 허용됩니다 (특수문자, 공백, 한글 등 불가).
- 콜론(:) 없이 입력하세요.
- Tracker가 MAC 설정 모드에 진입한 후에 명령을 전송해야 합니다.
- 스크립트 실행 중에는 다른 터미널에서 같은 포트를 사용하지 마세요.

## 파일 구성

### 루트 디렉토리
- `set_vmac.py` - Python 버전 메인 스크립트 (macOS/Windows 공통) ⭐
- `set_mac.sh` - Bash 버전 메인 스크립트 (macOS 전용)
- `install.sh` - 자동 설치 스크립트 (macOS)
- `requirements.txt` - Python 의존성 파일
- `README.md` - 사용 설명서

### windows/ 디렉토리 (독립 실행 가능)
- `windows/set_vmac.py` - Python 메인 스크립트 (루트의 복사본)
- `windows/set_vmac.bat` - Windows용 실행 배치 파일
- `windows/install.bat` - Windows용 자동 설치 스크립트
- `windows/README.md` - Windows 사용 설명서

⚠️ Windows 사용자는 `windows/` 폴더만 복사해서 독립적으로 사용할 수 있습니다.

## Python 버전의 주요 특징

### 정확한 시리얼 통신 설정
```python
serial.Serial(
    port='/dev/cu.usbserial-XXXX',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,    # Data bits: 8
    parity=serial.PARITY_NONE,     # Parity: None
    stopbits=serial.STOPBITS_ONE,  # Stop bits: 1
    xonxoff=False,                 # Software flow control: None
    rtscts=False                   # Hardware flow control: None
)
```

### 실시간 응답 확인
- 명령 전송 즉시 응답 수신
- 타임아웃 설정으로 안정적인 응답 대기
- AT 명령 응답과 Tracker 로그 구분 표시

### 우수한 에러 처리
- try-except로 모든 에러 캡처
- 명확한 에러 메시지
- Assertion 에러 없음

