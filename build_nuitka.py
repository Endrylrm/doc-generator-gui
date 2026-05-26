import platform
import os
import subprocess


def build_nuitka():
    currentOS = platform.system()

    if currentOS == "Windows":
        subprocess.run(
            [
                ".venv/Scripts/python.exe",
                "-m",
                "nuitka",
                "--assume-yes-for-downloads",
                "--mode=app-dist",
                "--plugin-enable=upx",
                f"--upx-binary={os.getcwd()}/upx/upx.exe",
                "--enable-plugin=pyside6",
                "--playwright-include-browser=none",
                "--windows-console-mode=disable",
                "--windows-icon-from-ico=gen_document.ico",
                "--include-data-dir=./documents=documents",
                "--include-data-dir=./data=data",
                "--include-data-files=./gen_document.ico=gen_document.ico",
                "--include-data-files=./.venv/Lib/site-packages/PySide6/translations/qt_*=PySide6/translations/",
                "--include-data-files=./.venv/Lib/site-packages/PySide6/translations/qtbase_*=PySide6/translations/",
                "./src/doc_generator_gui/main.py",
            ]
        )

    if currentOS == "Linux":
        subprocess.run(
            [
                ".venv/bin/python",
                "-m",
                "nuitka",
                "--assume-yes-for-downloads",
                "--mode=app-dist",
                "--plugin-enable=upx",
                f"--upx-binary={os.getcwd()}/upx/upx",
                "--enable-plugin=pyside6",
                "--playwright-include-browser=none",
                "--linux-icon=gen_document.ico",
                "--disable-console",
                "--include-data-dir=./documents=documents",
                "--include-data-dir=./data=data",
                "--include-data-files=./gen_document.ico=gen_document.ico",
                "--include-data-files=./.venv/lib/python3.13/site-packages/PySide6/Qt/translations/qt_*=PySide6/Qt/translations/",
                "--include-data-files=./.venv/lib/python3.13/site-packages/PySide6/Qt/translations/qtbase_*=PySide6/Qt/translations/",
                "./src/doc_generator_gui/main.py",
            ]
        )

    if currentOS == "Darwin":
        subprocess.run(
            [
                ".venv/bin/python",
                "-m",
                "nuitka",
                "--assume-yes-for-downloads",
                "--mode=app-dist",
                "--enable-plugin=pyside6",
                "--playwright-include-browser=none",
                "--macos-app-console-mode=disable",
                "--macos-create-app-bundle",
                "--macos-app-icon=gen_document.icns",
                "--include-data-dir=./documents=documents",
                "--include-data-dir=./data=data",
                "--include-data-files=./gen_document.ico=gen_document.ico",
                "--include-data-files=./.venv/lib/python3.13/site-packages/PySide6/Qt/translations/qt_*=PySide6/Qt/translations/",
                "--include-data-files=./.venv/lib/python3.13/site-packages/PySide6/Qt/translations/qtbase_*=PySide6/Qt/translations/",
                "./src/doc_generator_gui/main.py",
            ]
        )


build_nuitka()
