import json, os, pprint, datetime
import pickle

import web3
from twisted.internet import defer
from twisted.internet import threads
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
from network import network_calls as Network

class Ethereum():

    def __init__(self):
        self.work_dir = os.environ[ 'WORK_DIR' ]
        self.ballotregulator_ip = os.environ[ 'TWISTED_BALLOTREGULATOR_IP' ]

        self.web3 = Web3(IPCProvider("/usr/src/ethereumDB/testnet/geth.ipc"))
        # self.web3 = Web3(KeepAliveRPCProvider( host=self.ballotregulator_ip))
        self.abi = Network.request_contract_abi().wait(5)

    def ballotInfo(self, ballot_address):
        ContractFactory = self.web3.eth.contract(address=ballot_address, abi=self.abi)

        return_dict = {
            'ballot_name' : ContractFactory.call().getBallotName(),
            'ballot_finalized' : ContractFactory.call().getOptionsFinalized(),
            'ballot_registered_voter_count' : ContractFactory.call().getRegisteredVoterCount(),
            'ballot_options_range' : range(ContractFactory.call().getVotingOptionsLength()),
            'ballot_options_length' : ContractFactory.call().getVotingOptionsLength(),
            'ballot_end_time' : ContractFactory.call().getBallotEndTime(),
            'ballot_options_name' : [],
            'ballot_options_vote_count' :  []
        }

        for i in range(0, return_dict['ballot_options_length']):
            return_dict['ballot_options_name'].append(ContractFactory.call().getVotingOptionsName(i))
            return_dict['ballot_options_vote_count'].append(ContractFactory.call().getVotingOptionsVoteCount(i))

        return return_dict

    def userInfo(self, ballot_address, voter_address):
        ContractFactory = self.web3.eth.contract(address=ballot_address, abi=self.abi)
        data_voter = ContractFactory.call().voters(voter_address)
        return_dict = {
            'voter_eligable_to_vote' : data_voter[0],
            'voter_cast_vote' : data_voter[1],
            'voter_voted_index' : data_voter[2]
        }
        return return_dict


    def registerPrivateKey(self, private_key, password):
        web3_address = self.web3.personal.importRawKey(private_key, password)
        return web3_address

    def vote(self, ballot_address, voting_index, voter_address, voter_password):

        self.web3.personal.unlockAccount(voter_address, voter_password, 60)
        ContractFactory = self.web3.eth.contract(address=ballot_address, abi=self.abi)
        tx_hash = ContractFactory.transact({'from': voter_address}).vote(voting_index)
        return tx_hash
