import json
import os
from eth_account import Account
from web3 import Web3
from typing import Optional, Tuple
from app.core.config import get_settings

settings = get_settings()

class NFTMintingService:
    """Service to interact with the KamiCodeCredentials smart contract on Base."""

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.CHAIN_RPC_URL))
        self.minter_private_key = settings.MINTER_PRIVATE_KEY
        self.contract_address = settings.CONTRACT_ADDRESS

        # Load ABI
        abi_path = os.path.join(os.path.dirname(__file__), "..", "assets", "KamiCodeCredentials.json")
        if os.path.exists(abi_path):
            with open(abi_path, "r", encoding="utf-8") as f:
                artifact = json.load(f)
                self.abi = artifact["abi"]
        else:
            self.abi = []

    async def mint_achievement_nft(self, to_address: str, achievement_type: str, metadata_uri: str) -> Tuple[Optional[int], Optional[str]]:
        """
        Mints an achievement NFT to the user's wallet.
        Returns (token_id, transaction_hash)
        """
        if not self.minter_private_key or not self.contract_address or self.contract_address == "0x0000000000000000000000000000000000000000":
            # Mock minting for development
            import uuid
            return (999, f"0xMockTx{uuid.uuid4().hex}")

        try:
            account = Account.from_key(self.minter_private_key)
            contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

            # Build transaction
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            # Use max priority fee if supported
            try:
                max_priority_fee = self.w3.eth.max_priority_fee
            except:
                max_priority_fee = self.w3.to_wei(1, 'gwei')

            txn = contract.functions.mintAchievement(
                Web3.to_checksum_address(to_address),
                achievement_type,
                metadata_uri
            ).build_transaction({
                'chainId': 84532, # Base Sepolia
                'gas': 300000,
                'maxFeePerGas': self.w3.eth.gas_price,
                'maxPriorityFeePerGas': max_priority_fee,
                'nonce': nonce,
            })

            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.minter_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for receipt to get token ID from event
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Parse AchievementMinted event
            logs = contract.events.AchievementMinted().process_receipt(receipt)
            token_id = logs[0].args.tokenId if logs else None

            return token_id, tx_hash.hex()

        except Exception as e:
            print(f"❌ Error minting NFT: {e}")
            return None, None
