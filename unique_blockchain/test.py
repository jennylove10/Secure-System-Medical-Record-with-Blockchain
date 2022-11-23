from agents import Doctor, Miner, Patient, NMPA
from blockchain import Blockchain

if __name__ == '__main__':
    incompatibilities = {'medicine1': ['illness1', 'illness2'],
                         'medicine2': ['illness1'],
                         'medicine3': ['illness2', 'illness3']}

    Health_block = Blockchain(NMPA, incompatibilities)
    # Miners
    miner1 = Miner(Health_block)
    miner2 = Miner(Health_block)
    miner3 = Miner(Health_block)
    miner4 = Miner(Health_block)
    miner5 = Miner(Health_block)

    # Doctors
    doctor1 = Doctor('Doctor Tang')
    doctor2 = Doctor('Doctor Song')
    doctor3 = Doctor('Doctor Yuan')
    doctor4 = Doctor('Doctor Ming')

    # Patients
    patient1 = Patient('Mr. Qin')
    patient2 = Patient('Mr. Chu')
    patient3 = Patient('Mr. Yan')
    patient4 = Patient('Mr. Qi')
    patient5 = Patient('Mr. Wei')
    patient6 = Patient('Mr. Jin')

    # Health_block.NMPA.incompatibilities

    # Health_block.NMPA.incompatibilities['medicine4'] = ['illness2']

    # We first create the 2 transactions
    # Health_block.new_diagnosis(doctor2, patient1, 'illness2', 0.20)
    # Health_block.new_diagnosis(doctor2, patient3, 'illness3', 0.20)

    # Then we mine a block including all the miners
    miners = [miner1, miner2, miner3, miner4]
    # Health_block.mine(miners)
    Health_block.new_authorization(doctor1, 0.50)
    Health_block.mining(miner1)


    #
    # Health_block.new_diagnosis(doctor1, patient1, 'illness2', 0.20)
    # Health_block.mine(miners)
    # Health_block.mining(miner1)
    # Health_block.mine(miners)

    # time.sleep(3)
    # Health_block.mine(miners)
    print(Health_block.chain)
    print(type(Health_block.chain))