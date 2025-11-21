"""
VMAC 설정 핵심 로직
macOS와 Windows에서 공통으로 사용하는 메인 로직을 포함합니다.
"""

import sys
import time
from .ui import (
    init_colors, print_header, print_success, 
    print_error, print_warning, print_info, Colors
)
from .serial_utils import (
    find_tracker_port, configure_serial, test_connection
)
from .vmac_utils import (
    get_vmac_input, wait_for_mac_mode, send_at_command
)
from .config import (
    AT_CMD_VMAC, AT_CMD_SCFG, AT_CMD_RBOT,
    WAIT_TIME_NORMAL, WAIT_TIME_SHORT
)

def run_vmac_setup(platform_name: str) -> int:
    """
    VMAC 설정 프로세스 실행
    
    Args:
        platform_name (str): 'macOS' 또는 'Windows'
    """
    # 색상 초기화 (Windows의 경우 필요)
    init_colors()
    
    print_header(f"Tracker VMAC 자동 설정 스크립트 ({platform_name})")
    
    # pyserial 설치 확인
    try:
        import serial
    except ImportError:
        print_error("pyserial이 설치되어 있지 않습니다.")
        print("\n설치 방법:")
        if platform_name == 'Windows':
            print("   python -m pip install pyserial")
        else:
            print("   pip3 install pyserial")
        return 1
    
    # 1. 포트 찾기
    port_name = find_tracker_port()
    if not port_name:
        return 1
    
    print()
    
    # 2. 시리얼 포트 연결
    ser = configure_serial(port_name)
    if not ser:
        return 1
    
    try:
        # 3. 연결 진단
        if not test_connection(ser):
            ser.close()
            return 1
        
        # 4. VMAC 입력
        vmac = get_vmac_input()
        
        # 5. MAC 설정 모드 진입 대기
        wait_for_mac_mode()
        
        # 6. 현재 VMAC 조회 (설정 전)
        print_header("6. 현재 VMAC 조회 (설정 전)")
        send_at_command(ser, AT_CMD_VMAC, "현재 VMAC 조회", wait_time=WAIT_TIME_NORMAL)
        
        # 7. VMAC 설정
        print_header("7. VMAC 설정")
        print_info("MAC 설정 모드에서 VMAC 설정을 진행합니다.")
        print()
        send_at_command(ser, f"{AT_CMD_VMAC}={vmac}", "VMAC 설정", wait_time=WAIT_TIME_NORMAL)
        
        # 8. VMAC 조회 (설정 후)
        print_header("8. VMAC 확인 (설정 후)")
        print_info("MAC 설정 모드에서 설정된 VMAC을 확인합니다.")
        print()
        send_at_command(ser, AT_CMD_VMAC, "설정 후 VMAC 조회", wait_time=WAIT_TIME_NORMAL)
        
        # 9. 전체 설정 확인
        print_header("9. 전체 설정 확인")
        print_info(f"{AT_CMD_SCFG} 명령으로 현재 설정 정보를 확인합니다.")
        print()
        send_at_command(ser, AT_CMD_SCFG, "전체 설정 조회", wait_time=WAIT_TIME_NORMAL)
        
        # 10. 재부팅 여부
        print_header("10. 재부팅")
        reboot = input(f"Tracker 재부팅({AT_CMD_RBOT})을 실행할까요? (y/n): ").strip().lower()
        
        if reboot == 'y':
            send_at_command(ser, AT_CMD_RBOT, "재부팅", wait_time=WAIT_TIME_SHORT)
        
        # 종료
        print()
        print_success("모든 과정 완료!")
        print(f"{Colors.BOLD}{'='*50}{Colors.ENDC}")
        
    except KeyboardInterrupt:
        print()
        print_warning("사용자가 중단했습니다.")
        return 1
    except Exception as e:
        print()
        print_error(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if ser and ser.is_open:
            ser.close()
            print()
            print("🔌 시리얼 포트 연결 종료")
    
    return 0
