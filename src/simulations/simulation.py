from patient import Patient
from event import Event
from doctor import Doctor

l = locals()


# --- PATIENTS --- #
Zhao = Patient("P-123MU")
Qian = Patient("P-456UL")
Sun = Patient("P-789UZ")
Li = Patient("P-372GE")
Zhou = Patient("P-348KE")
Wu = Patient("P-856EV")
Zheng = Patient("P-806DM")
Wang = Patient("P-936DA")
Feng = Patient("P-622NL")
Chen = Patient("P-462TV")
Zhu = Patient("P-367TO")
Wei = Patient("P-421PT")
Jiang = Patient("P-985WV")
Shen = Patient("P-621WQ")
Han = Patient("P-261TV")
Yang = Patient("P-761FV")

# --- DISEASES --- #
arthritis = Event("disease", "arthritis", loc=l)
asthma = Event("disease", "asthma", loc=l)
bulimia = Event("disease", "bulimia", loc=l)
celiac = Event("disease", "celiac", loc=l)
diabetes = Event("disease", "diabetes", loc=l)
ebola = Event("disease", "ebola", loc=l)
fever = Event("disease", "rhinitis", loc=l)
flatulence = Event("disease", "flatulence", loc=l)
gastroenteritis = Event("disease", "gastroenteritis", loc=l)
hemorrhoids = Event("disease", "hemorroids", loc=l)
insomnia = Event("disease", "insomnia", loc=l)
keratitis = Event("disease", "keratitis", loc=l)
nephritis = Event("disease", "nephritis", loc=l)
neuritis = Event("disease", "neuritis", loc=l)
pneumonia = Event("disease", "pneumonia", loc=l)
rhinitis = Event("disease", "rhinitis", loc=l)






# --- PRESCRIPTIONS --- #
"""To avoid misinformation, prescriptions will not take real names."""
prescription_1 = Event("prescription", "drug_1", loc=l, incompatibilities=None)
prescription_2 = Event("prescription", "drug_2", loc=l, incompatibilities=["pneumonia"])
prescription_3 = Event("prescription", "drug_3", loc=l, incompatibilities=["arthritis", "diabetes"])
prescription_4 = Event("prescription", "drug_4", loc=l, incompatibilities=["bulimia", "flatulence", "insomnia"])
prescription_5 = Event("prescription", "drug_5", loc=l, incompatibilities=["arthritis", "nephritis"])
prescription_6 = Event("prescription", "drug_6", loc=l, incompatibilities=["rhinitis"])
prescription_7 = Event("prescription", "drug_7", loc=l, incompatibilities=None)
prescription_8 = Event("prescription", "drug_8", loc=l, incompatibilities=["diabetes"])
prescription_9 = Event("prescription", "drug_9", loc=l, incompatibilities=["celiac", "insomnia"])
prescription_10 = Event("prescription", "drug_10", loc=l, incompatibilities=None)
prescription_11 = Event("prescription", "drug_11", loc=l, incompatibilities=["flatulence", "hemorrhoids", "diabetes"])
prescription_12 = Event("prescription", "drug_12", loc=l, incompatibilities=["keratitis", "celiac", "diabetes"])
prescription_13 = Event("prescription", "drug_13", loc=l, incompatibilities=["pneumonia", "rhinitis"])
prescription_14 = Event("prescription", "drug_14", loc=l, incompatibilities=["flatulence", "fever"])
prescription_15 = Event("prescription", "drug_15", loc=l, incompatibilities=["celiac", "asthma"])


# --- DOCTORS --- #
DrZhao = Doctor("D-T621JP")
DrQian = Doctor("D-Y567UK")
DrSun = Doctor("D-K661TC")
DrLi = Doctor("D-Z421RY")
DrZhou = Doctor("D-M902XZ")
DrWu = Doctor("D-U566PX")
DrZheng = Doctor("D-H921AM")
DrWang = Doctor("D-Y639PX")
DrFeng = Doctor("D-Q606RT")
DrChen = Doctor("D-Z682VH")
