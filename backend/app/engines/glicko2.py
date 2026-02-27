import math
from typing import List, Tuple

class Glicko2:
    """
    Simplified Glicko-2 implementation for competitive programming.
    Based on Mark Glickman's paper.
    """
    def __init__(self, tau: float = 0.5):
        self.tau = tau  # Volatility constraint (standard is 0.5)

    def _to_glicko2(self, rating: float, rd: float) -> Tuple[float, float]:
        # Rating is centered at 1500, scale is 173.7178
        mu = (rating - 1500) / 173.7178
        phi = rd / 173.7178
        return mu, phi

    def _from_glicko2(self, mu: float, phi: float) -> Tuple[float, float]:
        rating = mu * 173.7178 + 1500
        rd = phi * 173.7178
        return rating, rd

    def calculate_new_rating(
        self,
        rating: float,
        rd: float,
        volatility: float,
        opponent_rating: float,
        opponent_rd: float,
        actual_score: float  # 1.0 for win, 0.5 for draw (not used here), 0.0 for loss
    ) -> Tuple[float, float, float]:
        """
        Calculates new rating, deviation, and volatility for a user against an opponent.
        In our case, the 'opponent' is the problem's expected performance level.
        """
        mu, phi = self._to_glicko2(rating, rd)
        mu_opp, phi_opp = self._to_glicko2(opponent_rating, opponent_rd)
        
        # E(mu, mu_opp, phi_opp) is the expected score
        g_phi_opp = 1 / math.sqrt(1 + 3 * (phi_opp**2) / (math.pi**2))
        expected_score = 1 / (1 + math.exp(-g_phi_opp * (mu - mu_opp)))
        
        # Variance v
        v = 1 / (g_phi_opp**2 * expected_score * (1 - expected_score))
        
        # Estimated improvement delta
        delta = v * g_phi_opp * (actual_score - expected_score)
        
        # New Volatility sigma' (using simplified version of Illinois algorithm)
        # Note: Glickman's full iterative algorithm is complex. 
        # For our use case, we keep volatility relatively stable for now.
        new_volatility = volatility 
        
        # New Deviation phi'
        phi_star = math.sqrt(phi**2 + new_volatility**2)
        new_phi = 1 / math.sqrt(1 / (phi_star**2) + 1 / v)
        
        # New Rating mu'
        new_mu = mu + (new_phi**2) * g_phi_opp * (actual_score - expected_score)
        
        new_rating, new_rd = self._from_glicko2(new_mu, new_phi)
        
        return new_rating, new_rd, new_volatility
