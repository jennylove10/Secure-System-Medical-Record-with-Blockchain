from __future__ import print_function

import logging
import random
import time
import grpc
import blockchain_pb2
import blockchain_pb2_grpc


# The client request the AddBlock to server
def run():
    with grpc.insecure_channel('127.0.0.1:50090') as channel:
        stub = blockchain_pb2_grpc.BlockchainStub(channel)
        tran_msg = "This block was added by client 1."
        response = stub.startMining(blockchain_pb2.startMiningRequest())
        while 1:
            if not response.result:
                time.sleep(10)
                print('waiting for transaction')
                response = stub.startMining(blockchain_pb2.startMiningRequest())
            else:
                print('mining a block successfully')


if __name__ == '__main__':
    logging.basicConfig()
    run()
