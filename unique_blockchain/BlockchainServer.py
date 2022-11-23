from concurrent import futures
import logging
from blockchain import Blockchain
from agents import Doctor, Miner, Patient, NMPA
from agents import *
import grpc

import blockchain_pb2_grpc, blockchain_pb2
from blockchain import startMining, diagnosis


class BlockchainServer(blockchain_pb2_grpc.BlockchainServicer):
    def __init__(self):
        incompatibilities = {'medicine1': ['illness1', 'illness2'],
                             'medicine2': ['illness1'],
                             'medicine3': ['illness2', 'illness3']}
        self.blockchain = Blockchain(NMPA, incompatibilities)

    def startMining(self, request, context):
        result = startMining(self.blockchain)
        return blockchain_pb2.startMiningResponse(result=result)

    def diagnosis(self, request, context):
        result = diagnosis(self.blockchain, request.doctorname, request.patientname, request.prescription, request.fee)
        return blockchain_pb2.diagnosisResponse(result=result)


# server setting
def serve():
    port = '50090'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blockchain_pb2_grpc.add_BlockchainServicer_to_server(BlockchainServer(), server)
    server.add_insecure_port('127.0.0.1:' + port)
    server.start()
    print("blockchain-demo started, listening on " + port)
    server.wait_for_termination()


# run the server
if __name__ == '__main__':
    logging.basicConfig()
    serve()
