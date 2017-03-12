# Application Server
The application server is the web interface for the voter to interact with the voting system.

## Status
### Pre Election Registration
- [ ] Receive login credentials from `External Voter Registration`

### Online Registration
- [x] Accept login from registered voters
- [ ] Generate a blind token
- [ ] Extract signed blind token & generate voter keys
- [ ] Register voterAddress with `Online Account Verifier`

### Voting
- [ ] Request the correct ballot contract address
- [ ] Fetch the correct ballot contract
- [ ] Display voting options
- [ ] Fund the contract with the voters selected optios

### Post Election
- [ ] Show voting choices
- [ ] Allow changing of votes (if before the election deadline)
- [ ] Allow validation of voters choice in the block chain

## Building
1. Ensure docker is running with `sudo service docker start`.
2. Build the docker image with `docker build -t applicationserver .` while in the *2_ApplicationServer* directory.
3. Run the docker image with `docker run -p 80:80 applicationserver` and map the internal port 80 to the localhost port 80.

# Notes
* Using `crochet` for twisted reactor handling and startup.
