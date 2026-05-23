from dataclasses import dataclass


@dataclass
class DocumentContext:
    printType: str = ""
    outputPath: str = ""
    currentHTML: str = ""
