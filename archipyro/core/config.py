from dataclasses import dataclass, field
from typing import List

@dataclass
class ProjectConfig:
    name: str
    framework: str
    architecture: str
    database: str
    features: List[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "_").replace("-", "_")

    def save(self, path: str):
        import json
        with open(path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    @classmethod
    def load(cls, path: str) -> "ProjectConfig":
        import json
        with open(path, "r") as f:
            data = json.load(f)
        return cls(**data)
