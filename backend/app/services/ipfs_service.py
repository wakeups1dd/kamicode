import httpx
from typing import Dict, Any, Optional
from app.core.config import get_settings

settings = get_settings()

class IPFSService:
    """Service to pin metadata and images to IPFS using Pinata."""

    @staticmethod
    async def pin_json(data: Dict[str, Any]) -> str:
        """
        Pins a JSON object to IPFS and returns the CID/URI.
        """
        if not settings.PINATA_API_KEY or settings.PINATA_API_KEY.startswith("your-") or not settings.PINATA_SECRET_KEY:
            # Mock CID for development if Pinata keys are missing or placeholders
            import uuid
            return f"ipfs://QmMock{uuid.uuid4().hex[:8]}"

        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        headers = {
            "pinata_api_key": settings.PINATA_API_KEY,
            "pinata_secret_api_key": settings.PINATA_SECRET_KEY,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"pinataContent": data}, headers=headers)
            response.raise_for_status()
            cid = response.json()["IpfsHash"]
            return f"ipfs://{cid}"

    @staticmethod
    def get_achievement_metadata(achievement_type: str, username: str, description: str) -> Dict[str, Any]:
        """Generates the NFT metadata JSON following OpenSea standards."""
        return {
            "name": f"KamiCode Achievement: {achievement_type}",
            "description": f"Awarded to {username}. {description}",
            "image": f"ipfs://QmAchievementPlaceholder", # Future: actual generated image CID
            "attributes": [
                {"trait_type": "Achievement Type", "value": achievement_type},
                {"trait_type": "Recipient", "value": username},
                {"trait_type": "Platform", "value": "KamiCode"}
            ]
        }
