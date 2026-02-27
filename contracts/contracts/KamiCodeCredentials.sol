// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract KamiCodeCredentials is ERC721, ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    event AchievementMinted(address indexed to, uint256 indexed tokenId, string achievementType, string uri);

    constructor(address initialOwner)
        ERC721("KamiCode Credentials", "KAMICRED")
        Ownable(initialOwner)
    {}

    function mintAchievement(address to, string memory achievementType, string memory uri)
        public
        onlyOwner
        returns (uint256)
    {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);

        emit AchievementMinted(to, tokenId, achievementType, uri);
        return tokenId;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
