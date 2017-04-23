import csv
import numpy as np
from datetime import datetime as dt
with open('nifty2016.csv') as nifty:
    with open('mrf.csv') as mrf:
        #Open the nifty of 20/4/2016 - 19/4/2017
        niftyVals = csv.reader(nifty, delimiter=',')
        
        #Open the mrf of 20/4/2016 - 19/4/2017
        mrfVals = csv.reader(mrf, delimiter=',')
        
        #Store the closing values of nifty in NIFTY variable
        NIFTY = []
        
        mrfDates = [dt.strptime(row[0],'%d-%m-%Y') for row in mrfVals]
        for row in niftyVals:
            if dt.strptime(row[0],'%d-%b-%y') in mrfDates:
                NIFTY.append(float(row[4]))
        mrf.seek(0)
        
        MRF = [float(row[4]) for row in mrfVals]
beta = (np.cov(MRF,NIFTY)[0][1])/np.var(NIFTY)
print(beta)
