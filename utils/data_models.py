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


@dataclasses.dataclass
class StartQuiz:
    current_step: Optional[str] = None
    smoking_type: Optional[str] = None
    intensity: Optional[str] = None
    period: Optional[str] = None
    reason: Optional[str] = None

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class VoiceData:
    current_step: Optional[str] = None
    file_id: Optional[str] = None
    text: Optional[str] = None
    confirmed: bool = False

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class StopSmokingData:
    time: str
    jobs: list

    def to_dict(self):
        return dataclasses.asdict(self)
