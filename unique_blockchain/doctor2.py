from __future__ import print_function
from agents import Doctor, Miner, Patient, NMPA
import logging
import random
import time
import grpc

import blockchain_pb2
import blockchain_pb2_grpc


def run():

    # doctor2 = Doctor('Doctor Song')
    # doctor3 = Doctor('Doctor Yuan')
    # doctor4 = Doctor('Doctor Ming')
    with grpc.insecure_channel('127.0.0.1:50090') as channel:
        stub = blockchain_pb2_grpc.BlockchainStub(channel)
        doctorname = 'Doctor Song'
        print("Input patient's name")
        # patientname = 'Mr. Chu'
        patientname= str(input())
        print("Input prescription")
        # prescription = 'illness2'
        prescription = str(input())
        print("Input fee")
        # fee = 0.20
        fee = float(input())

        response = stub.diagnosis(blockchain_pb2.diagnosis2Request(doctorname=doctorname, patientname=patientname ,prescription= prescription,fee= fee))
        if response :
            print(doctorname + ' made a diagnosis successful')
        else:
            print(doctorname + 'made failed')



if __name__ == '__main__':
    logging.basicConfig()
    run()
