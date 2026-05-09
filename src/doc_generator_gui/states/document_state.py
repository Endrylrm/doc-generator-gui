from dataclasses import dataclass, field


@dataclass
class DocumentState:
    """
    This class is responsible for maintaining the state
    data between our printing services.
    """

    output_path: str = ""
    input_data: dict[str, str] = field(default_factory=dict)
    input_history: dict[str, str] = field(default_factory=dict)
    company_data: dict[str, str] = field(default_factory=dict)

    def SetDefaultInputData(self):
        self.input_data = {}

        company_data = {
            data["replace"]: data["value"] for data in self.company_data.values()
        }

        self.input_data.update(company_data)
