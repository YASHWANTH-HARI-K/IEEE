// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title DebrisBountyEscrow
 * @dev Handles automated escrow minting and release for targeted ghost net retrieval.
 */
contract DebrisBountyEscrow {
    struct Bounty {
        uint256 id;
        string targetCoordinates;
        uint256 rewardAmount;
        address payable creator;
        address payable retriever;
        bool isClaimed;
    }

    uint256 public bountyCount;
    mapping(uint256 => Bounty) public bounties;

    event BountyMinted(uint256 indexed bountyId, string targetCoordinates, uint256 rewardAmount);
    event BountyClaimed(uint256 indexed bountyId, address indexed retriever);

    function mintBounty(string memory _targetCoordinates) external payable {
        require(msg.value > 0, "Escrow requires collateral funds.");
        bountyCount++;
        
        bounties[bountyCount] = Bounty({
            id: bountyCount,
            targetCoordinates: _targetCoordinates,
            rewardAmount: msg.value,
            creator: payable(msg.sender),
            retriever: payable(address(0)),
            isClaimed: false
        });

        emit BountyMinted(bountyCount, _targetCoordinates, msg.value);
    }

    function claimBounty(uint256 _bountyId) external {
        Bounty storage bounty = bounties[_bountyId];
        require(!bounty.isClaimed, "Bounty already claimed.");
        
        bounty.isClaimed = true;
        bounty.retriever = payable(msg.sender);
        
        bounty.retriever.transfer(bounty.rewardAmount);
        emit BountyClaimed(_bountyId, msg.sender);
    }
}