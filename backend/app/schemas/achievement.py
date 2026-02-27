from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AchievementResponse(BaseModel):
    id: str
    user_id: str
    achievement_type: str
    trigger_id: Optional[str] = None
    season_id: Optional[str] = None
    nft_token_id: Optional[int] = None
    nft_tx_hash: Optional[str] = None
    metadata_uri: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AchievementCatalogItem(BaseModel):
    id: str
    name: str
    description: str
    earned: bool = False
    earned_at: Optional[datetime] = None
    nft_status: Optional[str] = None # none, pending, minted
