"""
UI 관련 공통 함수
터미널 색상 및 출력 포맷팅 기능을 제공합니다.
"""

import platform


class Colors:
    """터미널 컬러 코드"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def init_colors() -> None:
    """Windows에서 ANSI 색상 코드 활성화"""
    if platform.system() == 'Windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass  # 실패해도 계속 진행 (색상만 표시 안됨)


def print_header(text: str) -> None:
    """헤더 출력"""
    print(f"\n{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{text:^50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*50}{Colors.ENDC}\n")


def print_success(text: str) -> None:
    """성공 메시지"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str) -> None:
    """에러 메시지"""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


def print_warning(text: str) -> None:
    """경고 메시지"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_info(text: str) -> None:
    """정보 메시지"""
    print(f"{Colors.BLUE}💡 {text}{Colors.ENDC}")

