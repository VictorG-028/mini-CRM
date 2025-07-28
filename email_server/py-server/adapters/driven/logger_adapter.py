from abc import ABC, abstractmethod
from typing import Optional
from core.ports.driven_ports import ILogger

RESET = "\033[0m"
PURPLE = "\033[35m"
ORANGE = "\033[38;5;208m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
LIGHT_GREEN = "\033[92;1m"
DARK_GREEN = "\033[32;1m"

class ConsoleLogger(ILogger):

    def log_info(self, msg: str) -> None:
        print(f"{PURPLE}[INFO]{RESET} {msg}")

    def log_error(self, msg: str, error: Optional[Exception] = None) -> None:
        if error:
            print(f"{RED}[ERROR]{RESET} {msg} - Error: {error}")
        else:
            print(f"{RED}[ERROR]{RESET} {msg}")

