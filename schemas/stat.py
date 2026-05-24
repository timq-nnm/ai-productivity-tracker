from pydantic import BaseModel

class SWeeklyStats(BaseModel):
    avg_sleep: float
    avg_energy: float
    avg_clarity: float
    avg_motivation: float
    entries_count: int