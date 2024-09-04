from datetime import datetime
import dataclasses
from typing import Optional

@dataclasses.dataclass
class RelapseSession:
    current_step: Optional[str] = None
    date_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    situation: Optional[str] = None
    thoughts: Optional[str] = None
    emotion_type: Optional[str] = None
    emotion_score: Optional[int] = None
    physical: Optional[str] = None
    behavior: Optional[str] = None

    def to_dict(self):
        return dataclasses.asdict(self)
