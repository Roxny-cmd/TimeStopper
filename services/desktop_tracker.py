import re
import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import win32con
import win32gui, win32process
import psutil
import uiautomation as auto

import config


@dataclass
class WindowInfo:
    process: str
    title: str
    is_browser: bool
    domain: Optional[str]
    timestamp: float


URL_PATTERN = re.compile(config.REGULAR_FOR_URL)

def is_browser(proc_name: str) -> bool:
    return proc_name.lower() in config.BROWSER_PROCESSES

def extract_doamin(url: str) -> Optional[str]:
    if '://' not in url:
        url = 'http://' + url
    host = urlparse(url).hostname
    if not host:
        return None
    return host.removeprefix('www.')

def find_domain(hwnd: int) -> Optional[str]:
    window = auto.GetForegroundControl()
    if window is None:
        return None

    for control, depth in auto.WalkControl(window, maxDepth=10):
        if control.ControlType != auto.ControlType.EditControl:
            continue
        try:
            value = control.GetValuePattern().Value.strip()
        except Exception:
            continue
        if value and URL_PATTERN.match(value):
            return extract_doamin(value)
    return None

def get_active_window() -> Optional[WindowInfo]:

    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None

    tid, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        proc_name = psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

    browser = is_browser(proc_name)
    domain = find_domain(hwnd) if browser else None


    return WindowInfo(
        process=proc_name,
        title=win32gui.GetWindowText(hwnd),
        is_browser=browser,
        domain=domain,
        timestamp=time.time()
    )


