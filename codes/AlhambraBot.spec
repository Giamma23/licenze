# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['AlgoPoldo.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['selenium.common', 'selenium.common.exceptions', 'selenium.webdriver', 'selenium.webdriver.chrome', 'selenium.webdriver.chrome.options', 'selenium.webdriver.chrome.remote_connection', 'selenium.webdriver.chrome.service', 'selenium.webdriver.chrome.webdriver', 'selenium.webdriver.chromium', 'selenium.webdriver.chromium.options', 'selenium.webdriver.chromium.remote_connection', 'selenium.webdriver.chromium.service', 'selenium.webdriver.chromium.webdriver', 'selenium.webdriver.common', 'selenium.webdriver.common.by', 'selenium.webdriver.common.desired_capabilities', 'selenium.webdriver.common.driver_finder', 'selenium.webdriver.common.options', 'selenium.webdriver.common.service', 'selenium.webdriver.common.utils', 'selenium.webdriver.remote.webdriver', 'selenium.webdriver.remote.webelement', 'selenium.webdriver.remote.errorhandler', 'selenium.webdriver.remote.remote_connection', 'selenium.webdriver.support', 'selenium.webdriver.support.ui', 'selenium.webdriver.support.expected_conditions', 'selenium.webdriver.support.wait', 'webdriver_manager.chrome'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AlhambraBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
