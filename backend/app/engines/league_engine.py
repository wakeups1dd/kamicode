"""
KamiCode — League Engine

Logic for tier promotions, demotions, and grace periods based on Glicko-2 ratings.
"""

from typing import Dict, Tuple, Optional
from app.models.user import User

# Tier thresholds (Rating Floor)
TIER_THRESHOLDS = {
    "bronze": 0.0,
    "silver": 1200.0,
    "gold": 1500.0,
    "diamond": 1800.0,
    "grandmaster": 2100.0,
}

# Ordered list of tiers for promotion/demotion logic
TIERS_ORDER = ["bronze", "silver", "gold", "diamond", "grandmaster"]

class LeagueEngine:
    """Handles tier transitions for users."""

    def determine_target_tier(self, rating: float) -> str:
        """Determines which tier a user's rating corresponds to."""
        current_tier = "bronze"
        for tier in TIERS_ORDER:
            if rating >= TIER_THRESHOLDS[tier]:
                current_tier = tier
            else:
                break
        return current_tier

    def process_tier_change(self, user: User, new_rating: float) -> Optional[str]:
        """
        Calculates if a user should change tiers.
        
        Promotions: Instant when rating reaches threshold.
        Demotions: Simple threshold check for now (can add grace periods later if needed).
        
        Returns the new tier name if changed, else None.
        """
        target_tier = self.determine_target_tier(new_rating)
        
        if target_tier != user.league_tier:
            old_tier = user.league_tier
            user.league_tier = target_tier
            return target_tier
        
        return None
