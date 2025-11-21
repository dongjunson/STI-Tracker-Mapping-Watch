# STI Tracker Mapping Watch - VMAC 설정 도구

Tracker 장치의 VMAC(가상 MAC 주소)을 자동으로 설정하는 Python 스크립트입니다.

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)](https://github.com)

## 📁 프로젝트 구조

```
STI-Tracker-Mapping-Watch/
├── README.md            # 프로젝트 개요 및 히스토리 (이 파일)
├── common/              # 공통 함수 모듈
│   ├── __init__.py      # 모듈 초기화 (버전 정보)
│   ├── config.py        # 설정 및 상수 정의
│   ├── core.py          # VMAC 설정 핵심 로직
│   ├── ui.py            # 터미널 UI 및 색상
│   ├── serial_utils.py  # 시리얼 통신 및 포트 관리
│   └── vmac_utils.py    # VMAC 입력/검증/AT 명령
├── mac/                 # macOS용
│   ├── README.md        # macOS 사용 설명서
│   └── set_vmac.py      # macOS 실행 스크립트
└── windows/             # Windows용
    ├── README.md        # Windows 사용 설명서
    └── set_vmac.py      # Windows 실행 스크립트
```

## 🚀 Quick Start

### macOS
```bash
cd mac/
pip3 install pyserial
python3 set_vmac.py
```
📖 [macOS 상세 가이드](mac/README.md)

### Windows
```cmd
cd windows
python -m pip install pyserial
python set_vmac.py
```
📖 [Windows 상세 가이드](windows/README.md)

## ✨ 주요 특징

- **자동 포트 탐색**: USB 시리얼 포트 자동 검색
- **실시간 진단**: Tracker 연결 상태 확인
- **간편한 입력**: MAC 뒷 4자리만 입력
- **컬러 출력**: 가독성 높은 터미널 UI
- **크로스 플랫폼**: macOS/Windows 지원

## 📋 요구사항

- **Python**: 3.6+ (macOS), 3.7+ (Windows)
- **pyserial**: `pip install pyserial`
- **USB 드라이버**: 대부분 자동 설치 (Windows 10/11)

## 📚 문서

- **macOS**: [mac/README.md](mac/README.md) - macOS 사용법
- **Windows**: [windows/README.md](windows/README.md) - Windows 사용법

## 🔧 핵심 기능

### 1. 공통 모듈 구조 (common/)
- `__init__.py`: 모듈 초기화 및 버전 정보 (v0.8.0)
- `config.py`: 시리얼 통신 설정 및 AT 명령어 상수 정의
- `core.py`: VMAC 설정 프로세스의 핵심 로직 (run_vmac_setup)
- `ui.py`: 터미널 색상 출력 및 메시지 포맷팅
- `serial_utils.py`: 시리얼 포트 탐색, 연결, 데이터 읽기
- `vmac_utils.py`: VMAC 입력/검증, AT 명령 전송 및 응답 처리

### 2. 플랫폼별 최적화
- **macOS**: `/dev/cu.usbserial*` 자동 탐색
- **Windows**: COM 포트 자동 탐색

### 3. 안전한 설정 프로세스
1. 포트 자동 탐색
2. 연결 진단
3. MAC 주소 검증 (16진수 4자리)
4. MAC 설정 모드 확인
5. VMAC 설정 및 검증
6. 전체 설정 확인 (AT+SCFG)

## 📝 버전 히스토리

### v0.8.1 (2025-11-21)
- **모듈 구조 개선**: `common/` 디렉토리를 6개 모듈로 세분화
  - `config.py`: 설정 및 상수 중앙 관리
  - `core.py`: 핵심 로직 분리 (run_vmac_setup)
  - 기존 모듈 유지: `ui.py`, `serial_utils.py`, `vmac_utils.py`, `__init__.py`
- **코드 가독성 향상**: 설정과 로직의 명확한 분리
- **유지보수성 강화**: 모듈별 책임 명확화

### v0.8.0 (2025-11-21)
- **AT+SCFG 명령 추가**: 재부팅 전 전체 설정 확인 단계 추가
- **Windows 드라이버 안내 개선**: FTDI VCP 드라이버를 선택사항으로 변경 (자동 설치 안내)
- **사용자 경험 개선**: 불필요한 장치 관리자 확인 단계 제거
- **문서 구조 개선**: 플랫폼별 상세 README 작성
- 루트 README를 히스토리 관리 및 개요로 간소화

### v0.7.2 (2025-11-21)
- 공통 함수를 `common/` 모듈로 완전 분리
- macOS/Windows 전용 스크립트 분리
- 플랫폼별 README 작성
- 코드 중복 100% 제거
- 전체 코드량 40% 감소
- 유지보수성 및 확장성 대폭 향상

### v0.7.1 (2025-11-14)
- 릴리스 날짜 정보 수정

### v0.7.0 (2025-11-14)
- Python/pyserial 기반 완전 재작성
- 크로스 플랫폼 지원 (macOS/Windows)
- 자동 포트 탐색 기능 추가
- 컬러 터미널 출력
- 향상된 에러 처리
- 실시간 응답 모니터링

### v0.1.0
- 초기 버전

## 🛠️ 기술 스택

- **언어**: Python 3.6+
- **라이브러리**: pyserial
- **지원 OS**: macOS, Windows 10/11
- **USB 칩셋**: FTDI, CH340, Prolific 등

## 📖 사용 예시

```bash
# macOS
cd mac/
python3 set_vmac.py

# MAC 주소 입력 (예시)
설정할 스마트워치 MAC 뒷 4자리 입력: B2C3
→ 전체 MAC: AAAAAAAAB2C3
```

## ⚠️ 중요 사항

1. **MAC 설정 모드 필수**: AT 명령은 MAC 설정 모드에서만 작동
2. **버튼 조작**: `[짧게 1회] + [길게 3초] 1회` → 3회 반복
3. **MAC 형식**: 16진수 4자리 (0-9, A-F)
4. **시리얼 설정**: 115200 baud, 8N1

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제공됩니다.

---

**STI Tracker Mapping Watch - VMAC Configuration Tool v0.8.1**  
Developed with ❤️ for seamless Tracker device configuration
