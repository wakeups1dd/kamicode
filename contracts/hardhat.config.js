const privateKey = process.env.MINTER_PRIVATE_KEY;
const accounts = (privateKey && privateKey.length >= 64 && !privateKey.startsWith("your-")) ? [privateKey] : [];

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
    solidity: "0.8.20",
    networks: {
        localhost: {
            url: "http://127.0.0.1:8545",
        },
        "base-sepolia": {
            url: process.env.CHAIN_RPC_URL || "https://sepolia.base.org",
            accounts: accounts,
        },
    },
};
