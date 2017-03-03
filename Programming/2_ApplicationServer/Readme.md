# Application Server
The application server is the web interface for the voter to interact with the voting system.

## Pre Election Registration
- [ ] Receive login credentials from `External Voter Registration`

## Online Registration
- [ ] Accept login from registered voters
- [ ] Generate a blind token
- [ ] Extract signed blind token & generate voter keys
- [ ] Register voterAddress with `Online Account Verifier`

## Voting
- [ ] Request the correct ballot contract address
- [ ] Fetch the correct ballot contract
- [ ] Display voting options
- [ ] Fund the contract with the voters selected optios

## Post Election
- [ ] Show voting choices
- [ ] Allow changing of votes (if before the election deadline)
- [ ] Allow validation of voters choice in the block chain
