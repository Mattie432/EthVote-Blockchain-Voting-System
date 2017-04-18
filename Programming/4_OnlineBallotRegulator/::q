#!/bin/bash

mkdir -p /usr/src/ethereumDB/testnet/

# Fix permissions on ethererum directory.
chmod -R o+rwx /usr/src/ethereumDB/testnet/

# Add our main account in charge of the ballots.
echo "Importing key files"
geth --testnet --datadir /usr/src/ethereumDB/ \
     --password $WORK_DIR/ethereum/keys/ethereum_password account import $WORK_DIR/ethereum/keys/ethereum_private_key

# For unlocking our account
account_address=$(cat $WORK_DIR/ethereum/keys/ethereum_address)

# Start geth in background
echo "Starting Ethereum node."
geth --testnet --datadir /usr/src/ethereumDB --fast --cache=1024 \
     --bootnodes "enode://20c9ad97c081d63397d7b685a412227a40e23c8bdc6688c6f37e97cfbc22d2b4d1db1510d8f61e6a8866ad7f0e17c02b14182d37ea7c3c8b9c2683aeb6b733a1@52.169.14.227:30303,enode://6ce05930c72abc632c58e2e4324f7c7ea478cec0ed4fa2528982cf34483094e9cbc9216e7aa349691242576d552a2a56aaeae426c5303ded677ce455ba1acd9d@13.84.180.240:30303" \
     --unlock $account_address --password $WORK_DIR/ethereum/keys/ethereum_password \
     2> /usr/src/ethereumDB/testnet/geth.log &
