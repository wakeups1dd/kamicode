const hre = require("hardhat");

async function main() {
    const [deployer] = await hre.ethers.getSigners();
    console.log("🚀 Deploying contracts with the account:", deployer.address);

    const KamiCodeCredentials = await hre.ethers.getContractFactory("KamiCodeCredentials");
    const contract = await KamiCodeCredentials.deploy(deployer.address);

    await contract.waitForDeployment();

    console.log("✅ KamiCodeCredentials deployed to:", await contract.getAddress());
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
