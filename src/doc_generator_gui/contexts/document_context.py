from dataclasses import dataclass, field


@dataclass
class DocumentContext:
    printType: str = ""
    outputPath: str = ""
    currentHTML: dict[str, str] = field(default_factory=dict[str, str])
