#!/bin/bash

echo "========================================="
echo "  Tracker VMAC 자동 설정 스크립트 (macOS)"
echo "========================================="
echo ""

###########################################
# 1. USB 시리얼 포트 자동 탐색
###########################################
PORT=$(ls /dev/cu.usbserial* 2>/dev/null | head -n 1)

if [ -z "$PORT" ]; then
    echo "❌ Tracker 포트를 찾을 수 없습니다."
    echo "   USB 연결 또는 드라이버 확인!"
    exit 1
fi

echo "🔌 Tracker 포트 발견: $PORT"
echo ""

###########################################
# 2. 통신 설정 및 screen 세션 시작
###########################################
echo ""
echo "🔧 통신 설정 적용 중..."
echo "   - Baudrate: 115200"
echo "   - Data bits: 8"
echo "   - Parity: None"
echo "   - Stop bits: 1"
echo ""

# 기존 screen 세션이 있으면 정리
if screen -list | grep -q "tracker_vmac"; then
    echo "⚠️  기존 screen 세션 발견, 정리 중..."
    screen -S tracker_vmac -X quit 2>/dev/null
    sleep 1
fi

# 포트가 사용 중인지 확인
PORT_IN_USE=$(lsof "$PORT" 2>/dev/null)
if [ -n "$PORT_IN_USE" ]; then
    echo "⚠️  포트가 사용 중입니다. 기존 프로세스 확인 중..."
    echo "$PORT_IN_USE" | head -5
    read -p "포트를 계속 사용하시겠습니까? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        echo "❌ 사용자가 취소했습니다."
        exit 1
    fi
fi

###########################################
# 2-1. 포트 초기화 및 시리얼 설정 (매뉴얼 기준)
###########################################
echo "🔧 시리얼 포트 초기화 중..."
echo "   매뉴얼 기준 설정:"
echo "   - Protocol: Serial"
echo "   - Baud rate: 115200"
echo "   - Data bits: 8"
echo "   - Parity: None"
echo "   - Stop bits: 1"
echo ""

# screen 시작 전에 stty로 포트를 완전히 초기화 및 설정
# 115200: Baudrate
# cs8: Data bits = 8 (character size 8 bits)
# -parenb: Parity = None (disable parity)
# -cstopb: Stop bits = 1 (disable 2 stop bits = use 1 stop bit)
# -crtscts: Hardware flow control = None (disable RTS/CTS)
# -ixon: Software flow control off (disable XON)
# -ixoff: Software flow control off (disable XOFF)
# clocal: Ignore modem control lines
# -echo: Disable echo
echo "⚙️  stty로 포트 설정 적용 중..."
stty -f "$PORT" 115200 cs8 -parenb -cstopb -crtscts -ixon -ixoff clocal -echo 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ 포트 설정 완료"
    # 설정 확인
    echo ""
    echo "📋 적용된 설정 확인:"
    stty -f "$PORT" 2>/dev/null | head -3 | sed 's/^/   /'
else
    echo "⚠️  포트 설정 실패 - 계속 진행합니다"
fi

echo ""

# screen 세션 시작
echo "📡 screen 세션 생성 중..."
SCREEN_LOG=$(mktemp)
echo "   로그 파일: $SCREEN_LOG"
echo "   포트: $PORT"
echo ""

# screen 명령 실행
# -dmS: detached 모드로 세션 생성
# -L: 로깅 활성화 (screenlog.0 생성)
SCREEN_ERROR=$(screen -dmS tracker_vmac -L "$PORT" 115200 2>&1)
SCREEN_EXIT_CODE=$?

if [ -n "$SCREEN_ERROR" ]; then
    echo "   ⚠️  screen 경고: $SCREEN_ERROR"
fi

# screen 세션이 시작될 때까지 충분히 대기
echo "   ⏳ screen 세션 초기화 중..."
sleep 4

# screen 세션이 제대로 시작되었는지 확인
if ! screen -list | grep -q "tracker_vmac"; then
    echo "❌ screen 세션 생성 실패!"
    echo "   Exit code: $SCREEN_EXIT_CODE"
    echo "   포트: $PORT"
    echo "   포트 존재 여부: $([ -e "$PORT" ] && echo "존재" || echo "없음")"
    echo "   포트 권한: $(ls -l "$PORT" 2>/dev/null || echo "확인 불가")"
    
    # screen 에러 로그 확인
    if [ -f "$SCREEN_LOG" ]; then
        echo "   로그 파일 내용:"
        cat "$SCREEN_LOG" | head -10 | sed 's/^/      /'
    fi
    
    echo ""
    echo "💡 해결 방법:"
    echo "   1. 포트가 다른 프로그램에서 사용 중인지 확인: lsof $PORT"
    echo "   2. 포트 권한 확인: ls -l $PORT"
    echo "   3. screen을 직접 실행해보세요: screen $PORT 115200"
    exit 1
fi

echo "✅ screen 세션 생성 완료"
echo ""

# screen 세션이 안정화될 때까지 대기
sleep 2

###########################################
# 2-1. Tracker 연결 진단 및 응답 테스트
###########################################
echo ""
echo "========================================="
echo "  📊 Tracker 연결 진단"
echo "========================================="
echo ""
echo "💡 참고: Tracker는 항상 로그를 출력하지는 않습니다."
echo "   로그가 없어도 AT 명령은 정상 동작할 수 있습니다."
echo ""

# 디버깅 정보 표시
echo "🔧 연결 정보:"
echo "   - 포트: $PORT"
echo "   - 로그 파일: $SCREEN_LOG"
echo "   - screen 세션: $(screen -list | grep -c tracker_vmac) 개"
echo ""

# Tracker 응답 테스트
echo "🔍 Tracker 응답 테스트 중..."
echo "   Enter 키를 전송하여 Tracker 응답을 확인합니다."
echo ""

# Enter 키 여러 번 전송 (stuff 명령 개선)
for i in {1..3}; do
    screen -S tracker_vmac -X stuff $'\r' 2>/dev/null || true
    sleep 1
done

# 로그 수집 (screenlog.0만 사용, hardcopy는 에러 발생하므로 제거)
echo "⏳ 응답 수집 중... (5초)"
for i in {1..5}; do
    sleep 1
    # screenlog.0이 생성되면 바로 SCREEN_LOG에 복사
    if [ -f "screenlog.0" ]; then
        cat screenlog.0 > "$SCREEN_LOG" 2>/dev/null || true
    fi
done

# screenlog.0 최종 확인
if [ -f "screenlog.0" ]; then
    cat screenlog.0 > "$SCREEN_LOG" 2>/dev/null || true
fi

echo ""
echo "📁 데이터 수신 확인:"
if [ -f "$SCREEN_LOG" ]; then
    LOG_SIZE=$(wc -c < "$SCREEN_LOG" 2>/dev/null || echo "0")
    echo "   - 수신 데이터: ${LOG_SIZE} bytes"
else
    LOG_SIZE=0
    echo "   - 수신 데이터: 0 bytes"
fi
echo ""

# 로그 확인 및 표시
if [ -f "$SCREEN_LOG" ] && [ -s "$SCREEN_LOG" ]; then
    echo "📋 Tracker 응답 (최근 30줄):"
    echo "----------------------------------------"
    tail -30 "$SCREEN_LOG" 2>/dev/null | sed 's/^/   /'
    echo "----------------------------------------"
    echo ""
    
    # 로그 내용 분석
    if grep -q "LED\|Button\|Mode" "$SCREEN_LOG" 2>/dev/null; then
        echo "✅ Tracker가 정상적으로 응답하고 있습니다!"
        echo "   (LED, Button 등의 내부 로그 확인됨)"
    elif [ "$LOG_SIZE" -gt 0 ]; then
        echo "⚠️  데이터가 수신되었지만 Tracker 로그 형식이 아닐 수 있습니다."
        echo "   그러나 통신은 되고 있으므로 계속 진행합니다."
    fi
else
    echo "⚠️  Tracker 응답 없음 (로그 0 bytes)"
    echo ""
    echo "   가능한 상황:"
    echo "   1. Tracker가 유휴 상태 (정상일 수 있음)"
    echo "   2. Tracker가 로그를 출력하지 않는 모드"
    echo "   3. 통신 문제 또는 잘못된 포트"
    echo ""
    echo "   💡 Tracker는 MAC 설정 모드에서만 AT 명령에 응답합니다."
    echo "      로그가 없어도 MAC 설정 모드에서는 정상 동작할 수 있습니다."
    echo ""
fi

echo ""
echo "🧪 추가 테스트 방법:"
echo "   다른 터미널에서 다음 명령으로 직접 확인할 수 있습니다:"
echo "   "
echo "   screen -r tracker_vmac"
echo "   "
echo "   연결 후:"
echo "   - Enter 키를 여러 번 눌러보기"
echo "   - Tracker 버튼을 눌러보고 로그가 나오는지 확인"
echo "   - 종료: Ctrl+A, D (detach)"
echo ""
read -p "다음 단계로 진행하시겠습니까? (y/n, 로그 없이도 진행 가능): " CONTINUE
if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
    screen -S tracker_vmac -X quit 2>/dev/null
    rm -f "$SCREEN_LOG" screenlog.0 2>/dev/null
    echo "❌ 사용자가 취소했습니다."
    exit 1
fi

echo ""
echo "✅ 진단 완료."
echo ""

###########################################
# 3. VMAC 입력받기 (뒷 4자리만 입력, 앞 8자리는 A로 자동 채움)
###########################################
echo "========================================="
echo "  📝 VMAC 설정 준비"
echo "========================================="
echo ""
read -p "설정할 스마트워치 MAC 뒷 4자리 입력 (예: B2C3): " VMAC_SUFFIX

# 입력값에서 공백 제거
VMAC_SUFFIX=$(echo "$VMAC_SUFFIX" | tr -d '[:space:]')

# 영문과 숫자만 허용하는지 검증
if [[ ! "$VMAC_SUFFIX" =~ ^[A-Za-z0-9]+$ ]]; then
    echo "❌ 형식 오류: 영문과 숫자만 입력할 수 있습니다."
    echo "   입력된 값: $VMAC_SUFFIX"
    screen -S tracker_vmac -X quit 2>/dev/null
    rm -f "$SCREEN_LOG" screenlog.0 2>/dev/null
    exit 1
fi

# 4자리 16진수 형식 검증
if [[ ! "$VMAC_SUFFIX" =~ ^[A-Fa-f0-9]{4}$ ]]; then
    echo "❌ 형식 오류: 4자리 16진수(0-9, A-F)만 입력해야 합니다."
    echo "   입력된 값: $VMAC_SUFFIX (길이: ${#VMAC_SUFFIX})"
    screen -S tracker_vmac -X quit 2>/dev/null
    rm -f "$SCREEN_LOG" screenlog.0 2>/dev/null
    exit 1
fi

# 앞 8자리는 A로 채우고, 뒤 4자리는 사용자 입력
VMAC="AAAAAAAA$VMAC_SUFFIX"

echo ""
echo "📝 설정할 전체 MAC 주소: $VMAC"
echo ""

###########################################
# 4. Tracker 버튼 설정 모드 안내 및 진입
###########################################
echo "========================================="
echo "  🔧 MAC 설정 모드 진입"
echo "========================================="
echo ""
echo "⚠️  MAC 설정 모드로 진입해야 AT+VMAC 명령이 작동합니다!"
echo ""
echo "📌 버튼 조작 방법:"
echo "   ▶ [짧게 1회] + [길게 3초] 1회 → 이 조합을 3회 반복"
echo ""
echo "💡 MAC 설정 모드로 진입하면:"
echo "   - LED가 특정 패턴으로 표시됩니다"
echo "   - AT+VMAC 명령에 응답합니다"
echo "   - 30초 후 자동으로 재부팅됩니다"
echo ""
read -p "MAC 설정 모드로 진입한 후 Enter 키를 누르세요: " DUMMY

# MAC 설정 모드 진입 후 잠시 대기
sleep 2
echo ""
echo "✅ MAC 설정 모드 진입 완료. VMAC 설정을 시작합니다."
echo ""

# 응답 확인 함수 정의 (hardcopy 제거, screenlog.0만 사용)
check_response() {
    local log_content=""
    
    # screenlog.0을 SCREEN_LOG에 동기화 (덮어쓰기로 변경)
    if [ -f "screenlog.0" ]; then
        cat screenlog.0 > "$SCREEN_LOG" 2>/dev/null || true
    fi
    
    # 로그 파일 확인
    if [ -f "$SCREEN_LOG" ] && [ -s "$SCREEN_LOG" ]; then
        log_content=$(tail -100 "$SCREEN_LOG" 2>/dev/null)
    fi
    
    if [ -z "$log_content" ]; then
        echo "   (로그 파일이 비어있거나 찾을 수 없습니다)"
        echo "   로그 파일 경로: $SCREEN_LOG"
        if [ -f "screenlog.0" ]; then
            echo "   screenlog.0 존재 여부: 있음 ($(wc -c < screenlog.0 2>/dev/null || echo 0) bytes)"
        fi
        echo "   screen 세션을 직접 확인하세요: screen -r tracker_vmac"
        return
    fi
    
    # AT 명령 응답 찾기 (VMAC, OK, ERROR 등) - 우선 표시
    local at_response=$(echo "$log_content" | grep -E "AT\+VMAC|VMAC|OK|ERROR" | tail -15)
    
    if [ -n "$at_response" ]; then
        echo "   [AT 명령 응답]"
        echo "$at_response" | sed 's/^/   /'
        echo ""
    fi
    
    # 최근 Tracker 로그도 표시 (LED, Button 등)
    local recent_log=$(echo "$log_content" | tail -10)
    if [ -n "$recent_log" ]; then
        if [ -n "$at_response" ]; then
            echo "   [최근 Tracker 로그]"
        fi
        echo "$recent_log" | sed 's/^/   /'
    fi
    
    # AT 응답이 없으면 안내
    if [ -z "$at_response" ]; then
        echo "   (AT 명령 응답 없음 - Tracker 로그만 표시)"
    fi
}

###########################################
# 5. 현재 Tracker 상태 확인 (설정 전) - MAC 설정 모드 진입 후
###########################################
echo ""
echo "📊 현재 Tracker 상태 확인 중..."
echo "🔍 현재 VMAC 조회 → AT+VMAC"

# 명령 전송 (에러 발생 시에도 계속 진행)
screen -S tracker_vmac -X stuff "AT+VMAC"$'\r' 2>/dev/null || {
    echo "   ⚠️  명령 전송 경고 (계속 진행)"
}

# 응답을 받을 때까지 충분히 대기
sleep 4

echo ""
echo "📋 현재 VMAC (설정 전):"
echo "----------------------------------------"
check_response
echo "----------------------------------------"
echo ""

###########################################
# 6. VMAC 설정 명령 보내기 및 응답 확인
###########################################
echo "💡 MAC 설정 모드에서 VMAC 설정을 진행합니다."
echo ""
echo "📝 VMAC 설정 실행 → AT+VMAC=$VMAC"
screen -S tracker_vmac -X stuff "AT+VMAC=$VMAC"$'\r' 2>/dev/null || {
    echo "   ⚠️  명령 전송 경고 (계속 진행)"
}
sleep 4

echo ""
echo "📋 설정 응답:"
echo "----------------------------------------"
check_response
echo "----------------------------------------"
echo ""

###########################################
# 7. VMAC 조회 명령 보내기 및 응답 확인 (설정 후)
###########################################
echo "💡 MAC 설정 모드에서 설정된 VMAC을 확인합니다."
echo ""
echo "🔍 VMAC 조회 실행 → AT+VMAC"
screen -S tracker_vmac -X stuff "AT+VMAC"$'\r' 2>/dev/null || {
    echo "   ⚠️  명령 전송 경고 (계속 진행)"
}
sleep 4

echo ""
echo "📋 설정 후 VMAC (설정 후):"
echo "----------------------------------------"
check_response
echo "----------------------------------------"
echo ""

###########################################
# 8. 재부팅 여부
###########################################
read -p "Tracker 재부팅(AT+RBOT)을 실행할까요? (y/n): " REBOOT

if [ "$REBOOT" == "y" ]; then
    echo "🔄 재부팅 명령 전송 → AT+RBOT"
    screen -S tracker_vmac -X stuff "AT+RBOT"$'\r' 2>/dev/null || {
        echo "   ⚠️  명령 전송 경고 (계속 진행)"
    }
    sleep 2
    
    echo ""
    echo "📋 재부팅 응답:"
    echo "----------------------------------------"
    check_response
    echo "----------------------------------------"
    echo ""
fi

###########################################
# 9. screen 세션 종료
###########################################
screen -S tracker_vmac -X quit
sleep 1

# 로그 파일 정리
if [ -f "$SCREEN_LOG" ]; then
    rm -f "$SCREEN_LOG"
fi

# screen의 기본 로그 파일도 정리
if [ -f "screenlog.0" ]; then
    rm -f screenlog.0
fi

echo ""
echo "✅ 모든 과정 완료!"
echo "========================================="