pragma solidity ^0.4.9;

/*
*   Written for ETH Vote blockchain voting system.
*   https://github.com/Mattie432/Blockchain-Voting-System
*/

/// @title Voting ballot
contract ETHVoteBallot {

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Contract Constructor ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ //

    address owner;                  // The address of the owner. Set in 'Ballot()'
    bool    optionsFinalized;       // Whether the owner can still add voting options.
    string  ballotName;             // The ballot name.
    uint    registeredVoterCount;   // Total number of voter addresses registered.
    uint    ballotEndTime;          // End time for ballot after which no changes can be made. (seconds since 1970-01-01)

    /*
    * Modifier to only allow the owner to call a function.
    */
    modifier onlyOwner
    {
        if( msg.sender != owner )
            throw;
        _;
    }

    /*
    *  This function is called *once* at first initialization into the blockchain.
    */
    function ETHVoteBallot(string _ballotName, uint _ballotEndTime)
    {
        if( now > _ballotEndTime)
            throw;

        owner                   = msg.sender;       // Set the owner to the address creating the contract.
        optionsFinalized        = false;            // Initially false as we need to add some choices.
        ballotName              = _ballotName;      // Sets the ballot name.
        registeredVoterCount    = 0;                // Initialize voter count
        ballotEndTime           = _ballotEndTime;   // Set the end date of this ballot.
    }

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Ballot Options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ //

    /*
    *  Structure which represents a single voting option for this ballot.
    */
    struct VotingOption
    {
        string name;    // Name of this voting option
        uint voteCount; // Number of accumulated votes.
    }
    VotingOption[] public votingOptions; // dynamically sized array of 'VotingOptions'

    /*
    *  Add a new voting option for this ballot.
    *  NOTE: this can only be called by the ballot owner.
    */
    function addVotingOption(string _votingOptionName) onlyOwner
    {
        if( now > ballotEndTime) throw;

        if(optionsFinalized == true)    // Check we are allowed to add options.
            throw;

        votingOptions.push(VotingOption({
            name: _votingOptionName,
            voteCount: 0
        }));
    }

    /*
    *  Call this once all options have been added, this will stop further changes
    *  and allow votes to be cast.
    *  NOTE: this can only be called by the ballot owner.
    */
    function finalizeVotingOptions() onlyOwner
    {
        if(now > ballotEndTime) throw;

        if(votingOptions.length < 2) throw;

        optionsFinalized = true;    // Stop the addition of any more options.
    }

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Voting Options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ //

    /*
    *  Structure which represents a single voter.
    */
    struct Voter
    {
        bool eligableToVote;    // Is this voter allowed to vote?
        bool voted;             // State of whether this voter has voted.
        uint votedFor;          // Index of 'votingOptions' this voter voted for.
    }
    mapping(address => Voter) public voters; // State variable which maps any address to a 'Voter' struct.

    /*
    *  Allow an address (voter) to vote on this ballot.
    *  NOTE: this can only be called by the ballot owner.
    */
    function giveRightToVote(address _voter) onlyOwner
    {
        if(now > ballotEndTime) throw;
        voters[_voter].eligableToVote = true;

        registeredVoterCount += 1;      // Increment registered voters.
    }

    /*
    *  Allow an eligable voter to vote for their chosen votingOption.
    *  If they have already voted, then remove their vote from the previous
    *  'votingOption' and assign it to the new one.
    *
    *  NOTE: if anything fails during this call we will throw and automatically
    *        revert all changes.
    */
    function vote(uint _votingOptionIndex)
    {
        if(now > ballotEndTime) throw;

        if(optionsFinalized == false)       // If the options are not finalized, we cannto vote.
            throw;

        Voter voter = voters[msg.sender];   // Get the Voter struct for this sender.

        if(voter.eligableToVote == false)
            throw;

        if(voter.voted == true) // If the voter has already voted then we need to remove their prev vote choice.
            votingOptions[voter.votedFor].voteCount -= 1;

        voter.voted = true;
        voter.votedFor = _votingOptionIndex;

        votingOptions[_votingOptionIndex].voteCount += 1;

    }

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Getter Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ //

    /*
    * Returns the ballots name string.
    */
    function getBallotName() returns (string)
    {
        return ballotName;
    }

    /*
    * Returns the number of voting options.
    */
    function getVotingOptionsLength() returns (uint)
    {
        return votingOptions.length;
    }

    /*
    * Returns the count of registered voter addresses.
    */
    function getRegisteredVoterCount() returns (uint)
    {
        return registeredVoterCount;
    }

    /*
    * Returns the name of a voting option at a specific index.
    * Throws if index out of bounds.
    */
    function getVotingOptionsName(uint _index) returns (string)
    {
        return votingOptions[_index].name;
    }

    /*
    * Returns the number of votes for a voting option at the specified index.
    * Throws if index out of bounds.
    */
    function getVotingOptionsVoteCount(uint _index) returns (uint)
    {
        return votingOptions[_index].voteCount;
    }

    /*
    * Returns if the voting options have been finalized.
    */
    function getOptionsFinalized() returns (bool)
    {
        return optionsFinalized;
    }

    /*
    * Returns the end time of the ballot in seconds since epoch.
    */
    function getBallotEndTime() returns (uint)
    {
        return ballotEndTime;
    }

}
