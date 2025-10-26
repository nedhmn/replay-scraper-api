from pydantic import BaseModel


class ReplayUrlRequest(BaseModel):
    replay_url: str


class ValidatedReplayData(BaseModel):
    cleaned_url: str
    replay_id: int
