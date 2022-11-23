import hashlib
import json
from time import time


import nacl.encoding
import nacl.signing
import numpy as np
from agents import Patient
from cryptography.hazmat.primitives import serialization
from agents import Doctor, Miner, Patient, NMPA


class Blockchain(object):
    def __init__(self, nmpa, incompatibilities):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash=1, nounce=100)

        self.NMPA = nmpa(incompatibilities)

    def new_block(self, nounce, previous_hash=None):
        """

        Parameters
        ----------
        nounce: the nounce found by the miner
        previous_hash: the previous block hashed

        Returns
        -------

        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nounce': nounce,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        if block['previous_hash'] == 1:
            self.chain.append(block)

        # self.chain.append(block)
        return block

    def new_diagnosis(self, sender, recipient, illness, fee):
        """
        Appends a transaction to the current transactions
        Parameters
        ----------
        sender: an object Doctor
        recipient: an object Patient
        illness: the illness diagnosed by the doctor
        fee: the fee value for inserting the transaction in the block

        Returns
        -------
        The index of the current block
        """
        self.current_transactions.append({
            'type': 'diagnosis',
            'sender': sender,
            'recipient': recipient,
            'illness': illness,
            'fee': fee
        })

        return self.last_block['index'] + 1

    def new_authorization(self, recipient, fee):
        """

        Parameters
        ----------
        recipient: an object Doctor
        fee: the fee value for inserting the transaction in the block

        Returns
        -------
        The index of the current block
        """
        self.current_transactions.append({
            'type': 'authorization',
            'sender': self.NMPA,
            'recipient': recipient,
            'authorization': self.NMPA.generate_authorization(recipient),
            'fee': fee
        })

        return self.last_block['index'] + 1

    def new_prescription(self, sender, recipient, prescription, fee):
        """

        Parameters
        ----------
        sender: an object Doctor
        recipient: an object Patient
        prescription: the medicine given by the doctor to the patient
        fee: the fee value for inserting the transaction in the block

        Returns
        -------
        The index of the current block
        """
        self.current_transactions.append({
            'type': 'prescription',
            'sender': sender,
            'recipient': recipient,
            'prescription': prescription,
            'fee': fee
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Hashes the data contained in a block
        Parameters
        ----------
        block: the dictionary representing the block

        Returns
        -------
        The resulting hash
        """
        data = [str(transaction) for transaction in block['transactions']]
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Performs the proof of work
        Parameters
        ----------
        last_proof: nounce of the last block

        Returns
        -------
        The nounce solving the proof of work
        """
        nounce = 0
        while self.valid_proof(last_proof, nounce) is False:
            nounce += 1

        return nounce

    def validate_block(self, block):
        if block['index'] != len(self.chain) + 1:
            return False
        if block['timestamp'] <= self.last_block['timestamp']:
            print('Backdating.')
            return False
        return True
        # return block['previous_hash']

    @staticmethod
    def valid_proof(last_proof, nounce):
        guess = f'{last_proof}{nounce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "00"

    def verify_authorizations(self):
        """
        Verifies that doctor has a valid authorization to make diagnoses or prescriptions.
        If a transaction is invalid is removed by the list of current transactions.
        Returns
        -------

        """
        c = 0
        to_be_deleted = []
        for transaction in self.current_transactions:
            if transaction['type'] == 'authorization':
                try:
                    authorization = transaction['authorization']
                    public_key = self.NMPA.public_key
                    public_key = nacl.signing.VerifyKey(public_key, encoder=nacl.encoding.HexEncoder)
                    public_key.verify(authorization)

                except:
                    to_be_deleted.append(c)

            else:
                try:
                    authorization = transaction['sender'].authorization
                    public_key = self.NMPA.public_key
                    public_key = nacl.signing.VerifyKey(public_key, encoder=nacl.encoding.HexEncoder)
                    public_key.verify(authorization)

                except:
                    to_be_deleted.append(c)
                    print('Not valid Doctor authorization')
                if transaction['type'] == 'prescription':
                    try:
                        incompatibilites = self.NMPA.incompatibilities
                        if transaction['prescription'] in incompatibilites.keys():
                            prescription = transaction['prescription']
                            illnesses_inc = set(self.NMPA.incompatibilities[prescription])
                            illnesses_patient = set(transaction['recipient'].illnesses)
                            assert len(illnesses_inc.intersection(illnesses_patient)) == 0
                    except:
                        to_be_deleted.append(c)
                        print('Incompatibility of one prescription with the history of the patient')
            c += 1
        new_transactions = []
        for i in range(len(self.current_transactions)):
            if i not in to_be_deleted:
                new_transactions.append(self.current_transactions[i])
        self.current_transactions = new_transactions

    def add_info(self, block):
        """
        Adds related info to the recipients of the transactions.
        Authorization to the doctor and illness to the patient.
        Parameters
        ----------
        block: \

        Returns
        -------

        """
        transactions = block['transactions']
        for transaction in transactions:
            if transaction['type'] == 'diagnosis':
                recipient = transaction['recipient']
                illness = transaction['illness']
                recipient.illnesses.append(illness)
            if transaction['type'] == 'authorization':
                recipient = transaction['recipient']
                authorization = transaction['authorization']
                recipient.authorization = authorization

    def mining(self, miner):
        self.verify_authorizations()
        if len(self.current_transactions) == 0:
            print("No new transactions, mining failed.")
            return False
        nounce, total_time = miner.mine_block()
        # Forge the new Block by adding it to the chain
        last_block = self.last_block
        previous_hash = self.hash(last_block)
        # self.verify_authorizations()
        block = self.new_block(nounce, previous_hash)
        if self.validate_block(block) is True:
            self.current_transactions = []
            self.chain.append(block)
            self.add_info(block)
            print('Mined a new block with number {0}'.format(block['index']))
            # Adding fees
            last_block = self.last_block
            fees = [transaction['fee'] for transaction in last_block['transactions']]
            miner.wallet = round(miner.wallet + sum(fees), 2)
            # Broadcasting
            miner.chain = self.chain
            print('Block number {0} broadcasted to all the nodes'.format(last_block['index']))
            return True
        else:
            print('mined failed')
            return False

    def mine(self, miners):
        """
        Let each miner specified in the parameter "miners" perform the proof of work.
        As soon as a block is found, the chain is broadcasted to all the miners and the fees are
        appended only to the miner who solved the proof of work in the shortest time.
        Parameters
        ----------
        miners: list of objects "Miner"

        Returns
        -------

        """
        self.verify_authorizations()
        if len(self.current_transactions) == 0:
            print("No new transactions, mining failed.")
            return False

        times = []
        nounces = []
        for miner in miners:
            nounce, total_time = miner.mine_block()
            times.append(total_time)
            nounces.append(nounce)
        index_min = np.argmin(np.array(times))
        nounce = nounces[index_min]

        # Forge the new Block by adding it to the chain
        last_block = self.last_block
        previous_hash = self.hash(last_block)
        # self.verify_authorizations()
        block = self.new_block(nounce, previous_hash)
        if self.validate_block(block) is True:
            self.current_transactions = []
            self.chain.append(block)
            self.add_info(block)
            # print('test validate')
            # print(self.validate_block(block))
            # self.chain.append(block)
            # self.add_info(block)
            print('Mined a new block with number {0}'.format(block['index']))

            # Adding fees
            last_block = self.last_block
            fees = [transaction['fee'] for transaction in last_block['transactions']]
            winning_miner = miners[index_min]
            winning_miner.wallet = round(winning_miner.wallet + sum(fees), 2)

            # Broadcasting
            for miner in miners:
                miner.chain = self.chain
            print('Block number {0} broadcasted to all the nodes'.format(last_block['index']))

    def check_keys(self, Patient, private_key):
        """
        Check that private and public keys match.
        Parameters
        ----------
        key : _RSAPrivateKey
        patient : Patient
        Raises
        ------
        AttributeError
            If `key` is None.
        PermissionError
            If private and public keys do not match.
        """
        if private_key is None:
            raise AttributeError("Please insert a valid key.")
        public_key_temp = private_key.public_key()
        public_key_temp = public_key_temp.public_bytes(encoding=serialization.Encoding.PEM,
                                                       format=serialization.PublicFormat.SubjectPublicKeyInfo)

        public_key = Patient.public_key
        public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)

        if public_key_temp != public_key:
            raise PermissionError("You do not have access to the BlockChain of this patient.")

    def get_patient_history(self, patient, private_key):
        """
        Gets the list of illnesses of the patient specified using a private key specified by the patient.
        Parameters
        ----------
        patient: an object "Patient"
        private_key: the private key specified by the patient

        Returns
        -------

        """
        assert isinstance(patient, Patient)
        try:
            self.check_keys(patient, private_key)
            patient.refresh_keys()
            return patient.illnesses
        except:
            raise PermissionError("You do not have access to the BlockChain of this patient.")


def startMining(blockchain: Blockchain):
    miner = Miner(blockchain)
    result = blockchain.mining(miner)
    return result


def diagnosis(blockchain: Blockchain, doctorname: str, patientname: str, prescription: str, fee):
    doctor = Doctor(doctorname)
    patient = Patient(patientname)
    result = blockchain.new_diagnosis(doctor, patient, prescription, fee)
    return result


def diagnosis2(blockchain: Blockchain, doctorname: str, patientname: str, prescription: str, fee):
    doctor = Doctor(doctorname)
    result = blockchain.new_authorization(doctor, 0.5)

    miner1 = Miner(blockchain)
    blockchain.mining(miner1)
    # patient = Patient(patientname)
    # result = blockchain.new_diagnosis(doctor, patient, prescription, fee)
    return result
