import PyInstaller.__main__
import os
import shutil
import subprocess


def Build_Nuitka():
    subprocess.run(
        [
            ".venv/Scripts/python.exe",
            "-m",
            "nuitka",
            "--standalone",
            "--enable-plugin=pyside6",
            "--disable-console",
            "--windows-icon-from-ico=gen_document.ico",
            "./src/main.py",
        ]
    )

    os.mkdir("./main.dist/Termos")
    shutil.copytree("./translations/", "./main.dist/PySide6/translations")
    shutil.copytree("./Templates/", "./main.dist/Templates")
    shutil.copy("gen_document.ico", "./main.dist/")


def Build_PyInstaller():
    PyInstaller.__main__.run(
        [
            "./src/main.py",
            "--noconsole",
            "--icon",
            "gen_document.ico",
            # other pyinstaller options...
        ]
    )

    os.mkdir("./dist/main/Termos")
    shutil.copytree("./Templates/", "./dist/main/Templates")
    shutil.copy("gen_document.ico", "./dist/main/")