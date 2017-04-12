import json, os, pprint, datetime
import pickle

from twisted.internet import defer
from twisted.internet import threads
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
from solc import compile_source, compile_files, link_code

class Ethereum():

    def __init__(self):
        self.work_dir = os.environ[ 'WORK_DIR' ]

        self.web3 = Web3(IPCProvider("/usr/src/ethereumDB/geth.ipc"))
        # self.web3 = Web3(KeepAliveRPCProvider())
        contract_path = self.work_dir + "ethereum/ETHVoteBallot.sol"
        compiled_contract = compile_files( [contract_path] )
        key = '{0}:ETHVoteBallot'.format(os.path.abspath(contract_path))
        self.compiled_contract = compiled_contract[key] # https://github.com/pipermerriam/py-solc

    def getBallotInterface(self):
        """
        Returns the ballots abi interface.
        :return:
        """
        return self.compiled_contract['abi']

    def registerBallot(self, ballot_name, ballot_end_date, ballot_options_array, timeout_mins=3):
        """
        Creates a new ballot on the blockchain with the ballot options specified.
        :param ballot_name:
        :param ballot_end_date:
        :param ballot_options_array:
        :param timeout_mins:
        :return: The contract address of the created ballot.
        """
        print("[ethereum - registerVoterAddressBallotId] Registering ballot '%s'" % ballot_name)
        bytecode = self.compiled_contract['bin']
        abi = self.getBallotInterface()

        deploy_address = self.interact_deploy_contract(ballot_name, ballot_end_date, abi, bytecode)

        deploy_transaction_hash_array = self.interact_add_ballot_options(deploy_address, abi, ballot_options_array)

        finalize_transaction_hash = self.interact_finalize_ballot(deploy_address, abi)

        return deploy_address

    def interact_deploy_contract(self, ballot_name, ballot_end_time, abi, bytecode, timeout_mins=3):
        """
        Deploys the contract from given abi & bytecode to the blockchain. Returns the confirmed contract address.
        :param ballot_name:
        :param ballot_end_time:
        :param abi:
        :param bytecode:
        :param timeout_mins:
        :return:
        """
        print("[ethereum - interact_deploy_contract] Deploying contract '%s' to the blockchain." % (ballot_name))

        # Create the contract factory from out abi & bytecode.
        ContractFactory = self.web3.eth.contract(abi=abi, bytecode=bytecode)

        deploy_tx_hash = ContractFactory.deploy(args=[ballot_name, int(ballot_end_time)] )
        print("                     contract_deploy_hash: %s" % deploy_tx_hash)

        # Wait 'n' mins for transaction to process.
        wait_until = datetime.datetime.now() + datetime.timedelta(minutes=timeout_mins)
        break_loop = False
        while not break_loop:
            deploy_address = self.web3.eth.getTransactionReceipt(deploy_tx_hash)
            if wait_until < datetime.datetime.now():
                raise Exception("Deploy transaction '%s' not mined. Timing out after %s mins." % (deploy_tx_hash, timeout_mins))
            elif deploy_address is not None:
                break_loop = True
                deploy_address = deploy_address['contractAddress']
                print("                   contract_deploy_address: %s" % deploy_address)

        return deploy_address

    def interact_add_ballot_options(self, contract_address, abi, ballot_options_array, timeout_mins=3):
        """
        Inserts the ballot options into the given address. Blocks until they are confirmed or timeout.
        :param contract_address:
        :param abi:
        :param ballot_options_array:
        :param timeout_mins:
        :return: Array of confirmed transaction hashes
        """
        print("[ethereum - interact_add_ballot_options] Adding '%s' to ballot '%s'" % (ballot_options_array, contract_address))

        ballot_options_transactions = []
        ContractFactory = self.web3.eth.contract(address=contract_address, abi=abi)
        for new_option in ballot_options_array:
            tx_hash = ContractFactory.transact().addVotingOption(str(new_option))
            ballot_options_transactions.append(tx_hash)
            print("                                  tx_hash: %s" % tx_hash)

        # Wait 'n' mins for transaction to process.
        wait_until = datetime.datetime.now() + datetime.timedelta(minutes=timeout_mins)
        break_loop = False
        while not break_loop:
            all_processed = []
            for option_transaction in ballot_options_transactions:
                all_processed.append(self.web3.eth.getTransactionReceipt(option_transaction))

            if wait_until < datetime.datetime.now():
                raise Exception("Add options transaction(s) '%s' not mined. Timing out after %s mins." % (ballot_options_transactions, timeout_mins))
            elif not None in all_processed: # If all transactions processed.
                all_processed_addresses = []
                for recipt in all_processed:
                    all_processed_addresses.append(recipt['transactionHash'])
                    print("                                confirmed: %s" % recipt['transactionHash'])
                break_loop = True

        return all_processed_addresses

    def interact_finalize_ballot(self, contract_address, abi, timeout_mins=3):
        """
        Finalizes the ballot at the given address.

        :param contract_address:
        :param abi:
        :param timeout_mins:
        :return: transaction hash of the finalize call.
        """
        print("[ethereum - interact_finalize_ballot] Finalizing ballot at address '%s'" % (contract_address))

        ContractFactory = self.web3.eth.contract(address=contract_address, abi=abi)
        finalize_tx_hash = ContractFactory.transact().finalizeVotingOptions()
        print("                         finalize_tx_hash: %s" % finalize_tx_hash)

        # Wait 'n' mins for transaction to process.
        wait_until = datetime.datetime.now() + datetime.timedelta(minutes=timeout_mins)
        break_loop = False
        while not break_loop:
            finalize_address = self.web3.eth.getTransactionReceipt(finalize_tx_hash)
            if wait_until < datetime.datetime.now():
                raise Exception("Finalize transaction '%s' not mined. Timing out after %s mins." % (finalize_tx_hash, timeout_mins))
            elif finalize_address is not None:
                break_loop = True
                print("                                confirmed: %s" % finalize_tx_hash)
        return finalize_tx_hash

    def interact_give_right_to_vote(self, contract_address, voter_address, abi, timeout_mins=3):
        """
        Finalizes the ballot at the given address.

        :param contract_address:
        :param abi:
        :param timeout_mins:
        :return: transaction hash of the finalize call.
        """
        print("[ethereum - interact_give_right_to_vote] Giving address '%s' the right to vote at '%s'" % (voter_address, contract_address))

        ContractFactory = self.web3.eth.contract(address=contract_address, abi=abi)

        gasEstimate = ContractFactory.estimateGas().giveRightToVote(str(voter_address)) * 1.1

        add_voter_tx_hash = ContractFactory.transact( {'gas': int(gasEstimate)  } ).giveRightToVote(str(voter_address))
        print("                        add_voter_tx_hash: %s" % add_voter_tx_hash)

        # 0.005 == $0.20
        ETH = 0.005
        ammount = self.web3.toWei(ETH, "ether")
        fund_hash = self.web3.eth.sendTransaction( { 'to':voter_address, 'value': ammount } )

        print("[ethereum - interact_give_right_to_vote] Funding voter account '%s' with %sETH" % (voter_address, ETH ))
        print("                                fund_hash: %s" % fund_hash)

        def wait_for_confirmation():
            # Wait 'n' mins for transaction to process.
            wait_until = datetime.datetime.now() + datetime.timedelta(minutes=timeout_mins)
            break_loop = False
            while not break_loop:
                finalize_address = self.web3.eth.getTransactionReceipt(add_voter_tx_hash)
                if wait_until < datetime.datetime.now():
                    raise Exception("Adding voter_address '%s' in transaction '%s' not mined. Timing out after %s mins." % (voter_address, add_voter_tx_hash, timeout_mins))
                elif finalize_address is not None:
                    break_loop = True
                    print("                                confirmed: %s" % add_voter_tx_hash)

            return add_voter_tx_hash

        def return_result(result):
            return result

        def return_errback(failure):
            print(failure.getErrorMessage())
            raise failure.raiseException()

        d = threads.deferToThread(wait_for_confirmation)
        d.addCallback(return_result).addErrback(return_errback)

        return d
