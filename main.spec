# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import platform
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

current_platform = platform.system().lower()
architecture = 'x64' if sys.maxsize > 2**32 else 'x86'

# Define executable name and paths based on the operating system
if current_platform.startswith('win'):
    exe_name = f'scrapegoat_windows_{architecture}.exe'
    build_path = 'D:\\a\\scrapegoat\\scrapegoat\\dist\\'
    chrome_portable_path = '.\ungoogled_chromium\ungoogled-chromium_129.0.6668.58-1.1_windows\'
    chromedriver_path = './chromedriver/win64/'
    chromedriver_binary = 'chromedriver.exe'
    chrome_binary = 'chrome.exe'
elif current_platform == 'darwin':
    exe_name = f'scrapegoat_macos_{architecture}'
    build_path = '/Users/runner/work/scrapegoat/scrapegoat/dist/'
    chrome_portable_path = './chrome_portable/ungoogled-chromium_128.0.6613.137-1.1_x86-64-macos-signed.app/Contents/MacOS/'
    chromedriver_path = './chromedriver/mac-x64/'
    chromedriver_binary = 'chromedriver'
    chrome_binary = 'ungoogled-chromium_128.0.6613.137-1.1_x86-64-macos-signed'
else:  # Linux
    exe_name = 'scrapegoat_linux'
    build_path = '/home/runner/work/scrapegoat/scrapegoat/dist/'
    chrome_portable_path = './chrome_portable/ungoogled-chromium_128.0.6613.137-1_linux/'
    chromedriver_path = './chromedriver/linux64/'
    chromedriver_binary = 'chromedriver'
    chrome_binary = 'chrome'

# Adjust paths when running as a frozen executable
if getattr(sys, 'frozen', False):
    chrome_portable_path = os.path.join(sys._MEIPASS, 'chrome_portable')
    chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')

# Analysis step
a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[
        (os.path.join(chromedriver_path, chromedriver_binary), 'chromedriver'),
        (os.path.join(chrome_portable_path, chrome_binary), 'chrome')
    ],
    datas=[
        (chrome_portable_path, 'chrome_portable'),
        (chromedriver_path, 'chromedriver')
    ],
    hiddenimports=collect_submodules('tkinter') + collect_submodules('ttkbootstrap') + ['win32ctypes.pywin32', 'pywintypes', 'win32api'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
