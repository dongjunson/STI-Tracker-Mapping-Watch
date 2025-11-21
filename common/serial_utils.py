"""
시리얼 통신 관련 공통 함수
시리얼 포트 설정, 데이터 읽기, 모니터링 기능을 제공합니다.
"""

import serial
import serial.tools.list_ports
import time
import platform
from .ui import Colors, print_success, print_error


def find_tracker_port():
    """Tracker USB 시리얼 포트 자동 탐색"""
    from .ui import print_header
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
    from .ui import print_header
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
    from .ui import print_header, print_info, print_warning
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

