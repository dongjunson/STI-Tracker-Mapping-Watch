#!/usr/bin/env python3
"""
Tracker VMAC 자동 설정 스크립트 (Windows 버전)
Windows에서 Tracker 장치의 VMAC을 설정합니다.

Version: 0.8.0
Date: 2025-11-21
"""

import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.core import run_vmac_setup

def main():
    """메인 함수 (Windows)"""
    return run_vmac_setup('Windows')

if __name__ == "__main__":
    sys.exit(main())
