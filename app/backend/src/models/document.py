from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Document:

    case_id: Optional[str]

    title: str

    citation: str

    decision_date: str

    judges: str

    petitioner: str

    respondent: str

    court: str

    path: str

    page_count: int

    word_count: int

    text: str

    def to_dict(self):
        return asdict(self)