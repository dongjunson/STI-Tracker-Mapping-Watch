"""
VMAC 설정 관련 공통 함수
VMAC 입력, 검증, AT 명령 전송 기능을 제공합니다.
"""

import re
import time
from .ui import Colors, print_header, print_success, print_info, print_error
from .serial_utils import read_with_timeout


def get_vmac_input():
    """VMAC 입력받기 (뒷 4자리만)"""
    print_header("4. VMAC 설정 준비")
    
    while True:
        vmac_suffix = input("설정할 스마트워치 MAC 뒷 4자리 입력 (예: B2C3): ").strip()
        
        # 공백 제거
        vmac_suffix = vmac_suffix.replace(' ', '')
        
        # 영문과 숫자만 허용
        if not re.match(r'^[A-Za-z0-9]+$', vmac_suffix):
            print_error("형식 오류: 영문과 숫자만 입력할 수 있습니다.")
            print(f"   입력된 값: {vmac_suffix}")
            continue
        
        # 4자리 16진수 검증
        if not re.match(r'^[A-Fa-f0-9]{4}$', vmac_suffix):
            print_error("형식 오류: 4자리 16진수(0-9, A-F)만 입력해야 합니다.")
            print(f"   입력된 값: {vmac_suffix} (길이: {len(vmac_suffix)})")
            continue
        
        # 앞 8자리는 A로 채움
        vmac = "AAAAAAAA" + vmac_suffix.upper()
        print()
        print(f"{Colors.GREEN}📝 설정할 전체 MAC 주소: {vmac}{Colors.ENDC}")
        print()
        
        return vmac


def wait_for_mac_mode():
    """MAC 설정 모드 진입 대기"""
    print_header("5. MAC 설정 모드 진입")
    
    print(f"{Colors.YELLOW}⚠️  MAC 설정 모드로 진입해야 AT+VMAC 명령이 작동합니다!{Colors.ENDC}")
    print()
    print("📌 버튼 조작 방법:")
    print("   ▶ [짧게 1회] + [길게 3초] 1회 → 이 조합을 3회 반복")
    print()
    print_info("MAC 설정 모드로 진입하면:")
    print("   - LED가 특정 패턴으로 표시됩니다")
    print("   - AT+VMAC 명령에 응답합니다")
    print("   - 30초 후 자동으로 재부팅됩니다")
    print()
    
    input("MAC 설정 모드로 진입한 후 Enter 키를 누르세요: ")
    
    print()
    print_success("MAC 설정 모드 진입 완료. VMAC 설정을 시작합니다.")
    print()
    time.sleep(2)


def send_at_command(ser, command, description, wait_time=3):
    """AT 명령 전송 및 응답 수신"""
    print(f"📝 {description} → {command}")
    
    # 입력 버퍼 클리어
    ser.reset_input_buffer()
    
    # 명령 전송
    ser.write((command + '\r\n').encode())
    ser.flush()
    
    # 응답 대기
    print(f"   ⏳ 응답 대기 중... ({wait_time}초)")
    time.sleep(wait_time)
    
    # 응답 읽기
    response = read_with_timeout(ser, timeout=1)
    
    print()
    print("📋 응답:")
    print("----------------------------------------")
    
    if response:
        # AT 명령 응답 찾기
        at_lines = [line for line in response.split('\n') if 'VMAC' in line or 'OK' in line or 'ERROR' in line or 'AT' in line]
        
        if at_lines:
            print("   [AT 명령 응답]")
            for line in at_lines[-10:]:
                if line.strip():
                    print(f"   {line}")
            print()
        
        # 최근 Tracker 로그
        all_lines = [line.strip() for line in response.split('\n') if line.strip()]
        recent_logs = all_lines[-10:]
        
        if recent_logs and not at_lines:
            print("   [최근 Tracker 로그]")
            for line in recent_logs:
                print(f"   {line}")
        
        if not at_lines and not recent_logs:
            print("   (응답 없음)")
    else:
        print("   (응답 없음)")
    
    print("----------------------------------------")
    print()
    
    return response

