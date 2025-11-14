#!/usr/bin/env python3
"""
Tracker VMAC 자동 설정 스크립트 (Python/pyserial 버전)
macOS와 Windows에서 Tracker 장치의 VMAC을 설정합니다.

Version: 0.7.0
Date: 2024-11-14
"""

import serial
import serial.tools.list_ports
import time
import sys
import re
import os
import platform
from threading import Thread, Event

# Windows에서 ANSI 색상 코드 활성화
if platform.system() == 'Windows':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass  # 실패해도 계속 진행 (색상만 표시 안됨)

class Colors:
    """터미널 컬러 코드"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_header(text):
    """헤더 출력"""
    print(f"\n{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{text:^50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*50}{Colors.ENDC}\n")

def print_success(text):
    """성공 메시지"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """에러 메시지"""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """경고 메시지"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    """정보 메시지"""
    print(f"{Colors.BLUE}💡 {text}{Colors.ENDC}")

def find_tracker_port():
    """Tracker USB 시리얼 포트 자동 탐색"""
    print_header("1. USB 시리얼 포트 자동 탐색")
    
    ports = list(serial.tools.list_ports.comports())
    
    # 운영체제별 포트 필터링
    if platform.system() == 'Windows':
        # Windows: COM 포트 중 USB 시리얼 찾기 (FTDI, Prolific, CH340 등)
        usb_ports = [p for p in ports if 'COM' in p.device and 
                     ('USB' in p.description.upper() or 
                      'SERIAL' in p.description.upper() or
                      'FTDI' in p.description.upper() or
                      'CH340' in p.description.upper() or
                      'PROLIFIC' in p.description.upper())]
    else:
        # macOS/Linux: usbserial 또는 ttyUSB 찾기
        usb_ports = [p for p in ports if 'usbserial' in p.device.lower() or 'ttyUSB' in p.device]
    
    if not usb_ports:
        print_error("Tracker 포트를 찾을 수 없습니다.")
        print("   USB 연결 또는 드라이버 확인!")
        print("\n사용 가능한 포트:")
        for p in ports:
            print(f"   - {p.device}: {p.description}")
        return None
    
    port = usb_ports[0].device
    print(f"{Colors.GREEN}🔌 Tracker 포트 발견: {port}{Colors.ENDC}")
    print(f"   설명: {usb_ports[0].description}")
    
    return port

def configure_serial(port_name):
    """시리얼 포트 설정 및 연결 (매뉴얼 기준)"""
    print_header("2. 시리얼 포트 설정 및 연결")
    
    print("🔧 매뉴얼 기준 설정:")
    print("   - Protocol: Serial")
    print("   - Baud rate: 115200")
    print("   - Data bits: 8")
    print("   - Parity: None")
    print("   - Stop bits: 1")
    print("   - Flow control: None")
    print()
    
    try:
        ser = serial.Serial(
            port=port_name,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,
            xonxoff=False,  # Software flow control: None
            rtscts=False,   # Hardware flow control: None
            dsrdtr=False
        )
        
        # 버퍼 클리어
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        print_success("시리얼 포트 연결 완료")
        print(f"   포트: {ser.port}")
        print(f"   Baudrate: {ser.baudrate}")
        # parity를 안전하게 출력 (문자열 또는 정수 모두 처리)
        parity_map = {serial.PARITY_NONE: 'N', serial.PARITY_ODD: 'O', serial.PARITY_EVEN: 'E'}
        parity_str = parity_map.get(ser.parity, 'N') if isinstance(ser.parity, int) else str(ser.parity)
        print(f"   설정: {ser.bytesize}{parity_str}{ser.stopbits}")
        
        return ser
        
    except serial.SerialException as e:
        print_error(f"시리얼 포트 연결 실패: {e}")
        return None

def read_with_timeout(ser, timeout=2):
    """타임아웃을 가지고 시리얼 데이터 읽기"""
    start_time = time.time()
    data = b''
    
    while (time.time() - start_time) < timeout:
        if ser.in_waiting > 0:
            chunk = ser.read(ser.in_waiting)
            data += chunk
            time.sleep(0.1)  # 추가 데이터를 위해 잠시 대기
        else:
            time.sleep(0.1)
    
    return data.decode('utf-8', errors='ignore')

def monitor_logs(ser, duration=5):
    """Tracker 로그 모니터링"""
    print(f"⏳ Tracker 로그 수집 중... ({duration}초)")
    print("----------------------------------------")
    
    logs = []
    start_time = time.time()
    
    while (time.time() - start_time) < duration:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"   {line}")
                logs.append(line)
        time.sleep(0.1)
    
    print("----------------------------------------")
    return logs

def test_connection(ser):
    """Tracker 연결 진단"""
    print_header("3. Tracker 연결 진단")
    
    print_info("참고: Tracker는 항상 로그를 출력하지는 않습니다.")
    print("   로그가 없어도 MAC 설정 모드에서는 정상 동작합니다.")
    print()
    
    print("🔍 Tracker 응답 테스트 중...")
    print("   Enter 키를 전송하여 응답을 확인합니다.")
    print()
    
    # Enter 키 3번 전송
    for i in range(3):
        ser.write(b'\r\n')
        time.sleep(0.5)
    
    # 로그 모니터링
    logs = monitor_logs(ser, duration=5)
    
    if logs:
        print_success("Tracker가 정상적으로 응답하고 있습니다!")
        if any('LED' in log or 'Button' in log or 'Mode' in log for log in logs):
            print("   (LED, Button 등의 내부 로그 확인됨)")
    else:
        print_warning("Tracker 응답 없음 (로그 0개)")
        print()
        print("   가능한 상황:")
        print("   1. Tracker가 유휴 상태 (정상일 수 있음)")
        print("   2. Tracker가 로그를 출력하지 않는 모드")
        print("   3. 통신 문제 또는 잘못된 포트")
        print()
        print_info("MAC 설정 모드에서는 AT 명령에 응답합니다.")
    
    print()
    response = input("다음 단계로 진행하시겠습니까? (y/n): ").strip().lower()
    if response != 'y':
        print_error("사용자가 취소했습니다.")
        return False
    
    return True

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

def main():
    """메인 함수"""
    print_header("Tracker VMAC 자동 설정 스크립트 (Python)")
    
    # pyserial 설치 확인
    try:
        import serial
    except ImportError:
        print_error("pyserial이 설치되어 있지 않습니다.")
        print("\n설치 방법:")
        if platform.system() == 'Windows':
            print("   python -m pip install pyserial")
            print("   또는 windows\\install.bat 실행")
        else:
            print("   pip3 install pyserial")
            print("   또는")
            print("   python3 -m pip install pyserial")
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
        send_at_command(ser, "AT+VMAC", "현재 VMAC 조회", wait_time=3)
        
        # 7. VMAC 설정
        print_header("7. VMAC 설정")
        print_info("MAC 설정 모드에서 VMAC 설정을 진행합니다.")
        print()
        send_at_command(ser, f"AT+VMAC={vmac}", "VMAC 설정", wait_time=3)
        
        # 8. VMAC 조회 (설정 후)
        print_header("8. VMAC 확인 (설정 후)")
        print_info("MAC 설정 모드에서 설정된 VMAC을 확인합니다.")
        print()
        send_at_command(ser, "AT+VMAC", "설정 후 VMAC 조회", wait_time=3)
        
        # 9. 재부팅 여부
        print_header("9. 재부팅")
        reboot = input("Tracker 재부팅(AT+RBOT)을 실행할까요? (y/n): ").strip().lower()
        
        if reboot == 'y':
            send_at_command(ser, "AT+RBOT", "재부팅", wait_time=2)
        
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

if __name__ == "__main__":
    sys.exit(main())

