# STI Tracker Mapping Watch - VMAC 설정 도구

Tracker 장치의 VMAC(가상 MAC 주소)을 자동으로 설정하는 크로스 플랫폼 Python 스크립트입니다.  
macOS와 Windows를 모두 지원하며, 시리얼 통신을 통해 Tracker 장치와 안전하게 통신합니다.

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📑 목차

- [주요 특징](#주요-특징)
- [실행 예시](#-실행-예시)
- [Quick Start](#quick-start)
- [사전 요구사항](#사전-요구사항)
- [시리얼 통신 설정](#시리얼-통신-설정)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [실행 단계](#실행-단계-공통)
- [문제 해결](#문제-해결)
- [주의사항](#주의사항)
- [프로젝트 구조](#프로젝트-구조)
- [기술적 세부 사항](#기술적-세부-사항)
- [의존성](#의존성)
- [개발 및 테스트](#개발-및-테스트)
- [FAQ](#faq-자주-묻는-질문)
- [기여하기](#기여하기)
- [버전 히스토리](#버전-히스토리)
- [라이선스](#라이선스)

## 주요 특징

✨ **완전 자동화된 워크플로우**
- USB 시리얼 포트 자동 탐색
- Tracker 연결 상태 진단
- VMAC 설정 및 확인 자동화
- 실시간 응답 모니터링

🔧 **정확한 시리얼 통신**
- Tracker 매뉴얼 기준 설정 (115200 baud, 8N1)
- pyserial 기반의 안정적인 통신
- 적절한 타임아웃 및 버퍼 관리
- AT 명령 응답 실시간 확인

🎨 **사용자 친화적 인터페이스**
- 컬러 터미널 출력 (macOS/Windows)
- 단계별 명확한 안내
- 상세한 에러 메시지와 해결 방법
- 진행 상황 실시간 표시

🌍 **크로스 플랫폼 지원**
- macOS (Intel/Apple Silicon)
- Windows 10/11
- 운영체제별 최적화된 포트 탐색

## 📸 실행 예시

스크립트를 실행하면 다음과 같은 화면이 표시됩니다:

```
==================================================
  Tracker VMAC 자동 설정 스크립트 (Python)
==================================================

==================================================
           1. USB 시리얼 포트 자동 탐색
==================================================

🔌 Tracker 포트 발견: /dev/cu.usbserial-A10KXYZ
   설명: USB Serial Port

==================================================
            2. 시리얼 포트 설정 및 연결
==================================================

🔧 매뉴얼 기준 설정:
   - Protocol: Serial
   - Baud rate: 115200
   - Data bits: 8
   - Parity: None
   - Stop bits: 1
   - Flow control: None

✅ 시리얼 포트 연결 완료
   포트: /dev/cu.usbserial-A10KXYZ
   Baudrate: 115200
   설정: 8N1

...
```

## Quick Start

### macOS
```bash
# 1. pyserial 설치
pip3 install pyserial

# 2. 실행
./set_vmac.py
# 또는
python3 set_vmac.py
```

### Windows
```cmd
REM 1. pyserial 설치
python -m pip install pyserial

REM 2. 실행
cd windows
python set_vmac.py
```

## 사전 요구사항

### macOS
1. **macOS 시스템**
2. **Python 3.6 이상** (macOS에 기본 설치됨)
3. **pyserial 라이브러리**
4. **USB 케이블** 및 Tracker 장치

### Windows
1. **Windows 10/11**
2. **Python 3.7 이상** (설치 시 "Add Python to PATH" 옵션 필수!)
3. **pyserial 라이브러리**
4. **FTDI VCP 드라이버** (USB 드라이버)
5. **USB 케이블** 및 Tracker 장치

## 시리얼 통신 설정

스크립트는 다음 시리얼 통신 설정을 사용합니다:

- **Baud rate**: 115200
- **Data bits**: 8
- **Parity**: None
- **Stop bits**: 1
- **Flow control**: None

이 설정은 Tracker 매뉴얼에 명시된 표준 설정입니다.

## 설치 방법

### macOS

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

### Windows

1. Python 설치 (https://www.python.org/downloads/)
   - ⚠️ **중요**: "Add Python to PATH" 옵션 반드시 체크!

2. pyserial 설치:
```cmd
python -m pip install pyserial
```

3. FTDI VCP 드라이버 설치 (https://ftdichip.com/drivers/vcp-drivers/)

## 사용 방법

### macOS

1. Tracker 장치를 USB 케이블로 Mac에 연결합니다.

2. 스크립트 실행:
```bash
./set_vmac.py
# 또는
python3 set_vmac.py
```

### Windows

1. Tracker 장치를 USB 케이블로 PC에 연결합니다.

2. 장치 관리자에서 COM 포트 확인 (선택사항):
   - `Windows + X` → 장치 관리자
   - "포트(COM & LPT)" 항목에서 확인

3. 스크립트 실행:
```cmd
cd windows
python set_vmac.py
```

또는 `windows\set_vmac.py` 파일을 더블클릭

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
- 포트가 다른 프로그램에서 사용 중
- USB 케이블 문제
- pyserial이 설치되지 않음

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
3. `python` 대신 `py` 명령어 시도: `py set_vmac.py`

### pyserial을 찾을 수 없음
```
ModuleNotFoundError: No module named 'serial'
```

**해결 방법:**
```bash
# macOS
pip3 install pyserial

# Windows
python -m pip install pyserial
```

### 권한 오류 (macOS)
- 스크립트에 실행 권한이 있는지 확인: `chmod +x set_vmac.py`

### 포트 사용 중 오류
- 다른 프로그램(Arduino IDE, PuTTY, 시리얼 터미널 등)이 포트를 사용 중인지 확인
- 해당 프로그램을 종료하고 다시 시도

## 주의사항

- 스마트워치 MAC 주소 뒷 4자리는 반드시 16진수 4자리 문자열이어야 합니다 (예: `B2C3`).
- 앞 8자리(`AAAAAAAA`)는 자동으로 고정됩니다.
- 입력은 영문과 숫자만 허용됩니다 (특수문자, 공백, 한글 등 불가).
- 콜론(:) 없이 입력하세요.
- Tracker가 MAC 설정 모드에 진입한 후에 명령을 전송해야 합니다.
- 스크립트 실행 중에는 다른 터미널에서 같은 포트를 사용하지 마세요.

## 프로젝트 구조

```
STI-Tracker-Mapping-Watch/
├── set_vmac.py           # macOS용 실행 스크립트
├── requirements.txt      # Python 의존성 (pyserial>=3.5)
├── README.md            # 프로젝트 문서 (본 파일)
└── windows/             # Windows 전용 디렉토리 (독립 실행 가능)
    ├── set_vmac.py      # Windows용 실행 스크립트
    └── README.md        # Windows 사용 설명서
```

### 플랫폼별 사용 방법

| 플랫폼 | 실행 파일 | 설명 |
|--------|-----------|------|
| **macOS** | `set_vmac.py` (루트) | Intel/Apple Silicon 모두 지원 |
| **Windows** | `windows/set_vmac.py` | Windows 10/11 지원, 독립 실행 가능 |

💡 **팁**: Windows 사용자는 `windows/` 폴더만 복사해서 독립적으로 사용할 수 있습니다.

## 기술적 세부 사항

### 시리얼 통신 설정 (pyserial 기반)

스크립트는 Tracker 매뉴얼에 명시된 정확한 시리얼 통신 파라미터를 사용합니다:

```python
serial.Serial(
    port='/dev/cu.usbserial-XXXX',  # macOS 예시
    baudrate=115200,                 # Baud rate: 115200
    bytesize=serial.EIGHTBITS,       # Data bits: 8
    parity=serial.PARITY_NONE,       # Parity: None
    stopbits=serial.STOPBITS_ONE,    # Stop bits: 1
    timeout=2,                       # Read timeout: 2초
    xonxoff=False,                   # Software flow control: None
    rtscts=False,                    # Hardware flow control: None
    dsrdtr=False                     # DTR/DSR flow control: None
)
```

### 주요 기능

**1. 자동 포트 탐색**
- macOS: `/dev/cu.usbserial*`, `/dev/ttyUSB*` 자동 검색
- Windows: COM 포트에서 FTDI, CH340, Prolific 등 USB 시리얼 장치 자동 검색

**2. 실시간 응답 처리**
- 명령 전송 후 즉시 응답 수신
- 타임아웃 기반 안정적인 데이터 읽기
- AT 명령 응답과 Tracker 로그를 구분하여 표시

**3. 강력한 에러 처리**
- try-except 블록으로 모든 예외 상황 처리
- 명확한 에러 메시지와 해결 방법 제시
- 리소스 자동 정리 (finally 블록)

**4. 크로스 플랫폼 컬러 출력**
- Windows: ctypes를 이용한 ANSI 색상 코드 활성화
- macOS/Linux: 네이티브 ANSI 색상 지원
- 색상 지원 실패 시에도 정상 동작

### 스크립트 실행 흐름

```
1. USB 시리얼 포트 자동 탐색
   └─> 운영체제별 최적화된 포트 검색
   
2. 시리얼 포트 설정 및 연결
   └─> 115200 baud, 8N1 설정으로 연결
   
3. Tracker 연결 진단
   ├─> Enter 키 전송으로 응답 테스트
   ├─> 로그 모니터링 (5초)
   └─> 사용자 확인 후 진행
   
4. VMAC 설정 준비
   ├─> 스마트워치 MAC 뒷 4자리 입력
   └─> 전체 MAC 주소 생성 (AAAAAAAA + 입력값)
   
5. MAC 설정 모드 진입
   └─> 버튼 조작 안내 및 대기
   
6. 현재 VMAC 조회 (설정 전)
   └─> AT+VMAC 명령 전송
   
7. VMAC 설정
   └─> AT+VMAC=AAAAAAAXXXXX 명령 전송
   
8. VMAC 확인 (설정 후)
   └─> AT+VMAC 명령 재전송
   
9. 재부팅 (선택사항)
   └─> AT+RBOT 명령 전송
```

## 의존성

- **Python**: 3.6 이상 (macOS), 3.7 이상 (Windows)
- **pyserial**: 3.5 이상

```bash
# 의존성 설치
pip3 install -r requirements.txt
```

## 개발 및 테스트

### 개발 환경
- Python 3.6+ (macOS), Python 3.7+ (Windows)
- pyserial 라이브러리
- Tracker 하드웨어 (FTDI 또는 호환 USB-Serial 칩)

### 테스트된 환경
- ✅ macOS 12.0+ (Intel & Apple Silicon)
- ✅ Windows 10 (21H2)
- ✅ Windows 11 (22H2)

### 지원 USB-Serial 칩셋
- FTDI FT232, FT2232
- CH340, CH341
- Prolific PL2303
- 기타 표준 USB CDC 장치

## FAQ (자주 묻는 질문)

### Q1. AT+VMAC 명령이 응답하지 않습니다.
**A:** MAC 설정 모드에 진입했는지 확인하세요. 버튼 조작: [짧게 1회] + [길게 3초] 1회 → 이 조합을 3회 반복

### Q2. Tracker 로그가 보이지 않습니다.
**A:** 정상일 수 있습니다. Tracker는 항상 로그를 출력하지 않으며, MAC 설정 모드에서만 AT 명령에 응답합니다.

### Q3. 시리얼 포트를 찾을 수 없습니다.
**A:** 
- USB 케이블 연결 확인
- 드라이버 설치 확인 (Windows: FTDI VCP 드라이버)
- 다른 USB 포트 시도
- `ls /dev/cu.*` (macOS) 또는 장치 관리자 (Windows)에서 포트 확인

### Q4. Windows에서 Python을 찾을 수 없다는 메시지가 나옵니다.
**A:** Python 설치 시 "Add Python to PATH" 옵션을 체크하지 않은 경우입니다. Python을 재설치하거나 `py` 명령어를 사용하세요: `py set_vmac.py`

### Q5. MAC 주소 형식은 어떻게 되나요?
**A:** 전체 12자리 중 앞 8자리는 `AAAAAAAA`로 고정되며, 뒷 4자리만 입력하면 됩니다 (예: `B2C3` 입력 → `AAAAAAAAB2C3` 설정).

## 기여하기

이 프로젝트에 기여하고 싶으시다면:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 버전 히스토리

- **v2.0.0** (2024) - Python/pyserial 기반 완전 재작성
  - 크로스 플랫폼 지원 (macOS/Windows)
  - 자동 포트 탐색
  - 컬러 터미널 출력
  - 향상된 에러 처리
  - 실시간 응답 모니터링

- **v1.0.0** (이전) - 초기 버전

## 라이선스

이 프로젝트는 교육 및 연구 목적으로 제공됩니다.

## 지원 및 문의

문제가 발생하거나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.

---

**STI Tracker Mapping Watch - VMAC Configuration Tool**  
Developed with ❤️ for seamless Tracker device configuration

