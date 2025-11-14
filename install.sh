#!/bin/bash

echo "========================================="
echo "  Tracker VMAC 스크립트 설치"
echo "========================================="
echo ""

# Python 버전 확인
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ Python 발견: $PYTHON_VERSION"
else
    echo "❌ Python3가 설치되어 있지 않습니다."
    echo ""
    echo "설치 방법:"
    echo "  1. Homebrew 설치: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "  2. Python 설치: brew install python3"
    exit 1
fi

echo ""

# pyserial 설치
echo "📦 pyserial 설치 중..."
pip3 install pyserial --quiet

if [ $? -eq 0 ]; then
    echo "✅ pyserial 설치 완료"
else
    echo "⚠️  pyserial 설치 실패 - 수동으로 설치하세요:"
    echo "   pip3 install pyserial"
fi

echo ""

# 실행 권한 부여
echo "🔧 실행 권한 부여 중..."
chmod +x set_vmac.py
chmod +x set_mac.sh

if [ $? -eq 0 ]; then
    echo "✅ 실행 권한 부여 완료"
fi

echo ""
echo "========================================="
echo "✅ 설치 완료!"
echo "========================================="
echo ""
echo "사용 방법:"
echo "  Python 버전 (권장): ./set_vmac.py"
echo "  Bash 버전:         ./set_mac.sh"
echo ""

