import platform
import PyInstaller.__main__


def build_pyinstaller():
    currentOS = platform.system()

    if currentOS == "Windows":
        PyInstaller.__main__.run(
            [
                "--noconsole",
                "--icon",
                "./assets/icons/gen_document.ico",
                "--upx-dir",
                "./upx/",
                "--contents-directory=.",
                "--add-data=data;data",
                "--add-data=documents;documents",
                "--add-data=./assets/icons/gen_document.png;.",
                "./src/doc_generator_gui/main.py",
            ]
        )

    if currentOS == "Linux":
        PyInstaller.__main__.run(
            [
                "--noconsole",
                "--icon",
                "./assets/icons/gen_document.png",
                "--upx-dir",
                "./upx/",
                "--contents-directory=.",
                "--add-data=data:data",
                "--add-data=documents:documents",
                "--add-data=./assets/icons/gen_document.png:.",
                "./src/doc_generator_gui/main.py",
            ]
        )

    if currentOS == "Darwin":
        PyInstaller.__main__.run(
            [
                "--noconsole",
                "--icon",
                "./assets/icons/gen_document.icns",
                "--contents-directory=.",
                "--add-data=data:data",
                "--add-data=documents:documents",
                "--add-data=./assets/icons/gen_document.png:.",
                "./src/doc_generator_gui/main.py",
            ]
        )


build_pyinstaller()
