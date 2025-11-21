# Tracker VMAC 설정 - macOS

Tracker 장치의 VMAC(가상 MAC 주소)을 설정하는 Python 스크립트입니다.

## 🚀 Quick Start

```bash
# 1. pyserial 설치
pip3 install pyserial

# 2. 실행
python3 set_vmac.py
```

## 📋 사전 요구사항

1. **macOS 시스템**
2. **Python 3.6 이상** (macOS에 기본 설치됨)
3. **pyserial 라이브러리**
4. **USB 케이블** 및 Tracker 장치

## 💿 설치

```bash
# pyserial 설치
pip3 install pyserial

# 실행 권한 부여 (선택사항)
chmod +x set_vmac.py
```

## 📱 사용 방법

### 1단계: Tracker 연결
USB 케이블로 Tracker를 Mac에 연결합니다.

### 2단계: 스크립트 실행
```bash
python3 set_vmac.py
```

### 3단계: 안내에 따라 진행
1. **포트 자동 탐색**: 스크립트가 자동으로 USB 포트를 찾습니다
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
  Tracker VMAC 자동 설정 스크립트 (macOS)
==================================================

🔌 Tracker 포트 발견: /dev/cu.usbserial-A10KXYZ
   설명: USB Serial Port

✅ 시리얼 포트 연결 완료
   포트: /dev/cu.usbserial-A10KXYZ
   Baudrate: 115200

설정할 스마트워치 MAC 뒷 4자리 입력 (예: B2C3): B2C3
📝 설정할 전체 MAC 주소: AAAAAAAAB2C3
```

## ⚙️ 시리얼 통신 설정

- **Baud rate**: 115200
- **Data bits**: 8
- **Parity**: None
- **Stop bits**: 1
- **Flow control**: None

## 🔧 문제 해결

### 포트를 찾을 수 없음
```bash
# 사용 가능한 포트 확인
ls /dev/cu.*

# USB 장치 확인
system_profiler SPUSBDataType
```

**해결 방법:**
- USB 케이블 재연결
- 다른 USB 포트 시도
- USB 드라이버 확인 (FTDI 칩의 경우)

### pyserial이 없음
```bash
pip3 install pyserial

# 또는 명시적으로
python3 -m pip install pyserial
```

### 권한 오류
```bash
# 실행 권한 부여
chmod +x set_vmac.py

# 또는 sudo로 실행 (권장하지 않음)
sudo python3 set_vmac.py
```

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

## 📚 FAQ

**Q: Tracker 로그가 보이지 않습니다.**  
A: 정상일 수 있습니다. Tracker는 항상 로그를 출력하지 않으며, MAC 설정 모드에서만 AT 명령에 응답합니다.

**Q: MAC 주소 형식은?**  
A: 뒷 4자리만 입력 (예: B2C3) → 전체: AAAAAAAAB2C3

**Q: 어떤 USB 칩셋을 지원하나요?**  
A: FTDI, CH340, Prolific 등 대부분의 USB-Serial 칩셋 지원

---

**버전**: 0.8.0  
**플랫폼**: macOS (Intel/Apple Silicon)  
**Python**: 3.6+

