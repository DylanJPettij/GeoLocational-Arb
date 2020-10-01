import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator) 
CostOfLiving = pd.read_excel (r'C:\Users\Dylan\PythonAnalysis\Cost Of Living Index.xlsx')
del CostOfLiving['Rank']

def mergeData():
    City_Living_Rent_LocalPurchasingPower = CostOfLiving[['City','Cost of Living Plus Rent Index', 'Local Purchasing Power Index']]
    sorted_df = City_Living_Rent_LocalPurchasingPower.sort_values('Cost of Living Plus Rent Index', ascending = True)
    return(sorted_df)

def FixData(sorted_df):
    CostOfLiving = sorted_df.sort_values('Cost of Living Plus Rent Index', ascending = True)
    BelowAverageCost = CostOfLiving[CostOfLiving['Cost of Living Plus Rent Index'] < CostOfLiving['Cost of Living Plus Rent Index'].mean()] 
    AboveAveragePurchasingPower = CostOfLiving[CostOfLiving['Local Purchasing Power Index'] > CostOfLiving['Local Purchasing Power Index'].mean()] 
    AboveAveragePurchasingPower = AboveAveragePurchasingPower.sort_values('Local Purchasing Power Index', ascending = False)
    BelowAverageCost = BelowAverageCost[BelowAverageCost['Cost of Living Plus Rent Index'] >=19] #setting a floor for cost of living
    BelowAverageCost= BelowAverageCost.reset_index()
    AboveAveragePurchasingPower= AboveAveragePurchasingPower.reset_index()
    del BelowAverageCost['index']
    del AboveAveragePurchasingPower['index']
    return BelowAverageCost, AboveAveragePurchasingPower

def Charting(Cost, PurchasingPower):
    C10 =Cost.head(30)
    C10['Cost of Living Plus Rent Index']=100*(C10['Cost of Living Plus Rent Index']/C10['Cost of Living Plus Rent Index'].mean()-1)
    x=C10['City']
    y=C10['Cost of Living Plus Rent Index']
    #charting portion
    colormat=np.where(C10['Cost of Living Plus Rent Index']>0, 'g','r')
    plt.title("Top 10 Places with the Lowest Cost of Living Index Including Rent")
    plt.xlabel("% Disparity")
    plt.ylabel("Cities")
    plt.barh(x,y,color =colormat, edgecolor="black")
    plt.show()
    plt.close()
    print("-------------------------")
    PurchasingPower = PurchasingPower.sort_values('Local Purchasing Power Index', ascending = False)

    PP30=PurchasingPower.head(30)
    PP30['Local Purchasing Power Index']=100*(PP30['Local Purchasing Power Index']/PP30['Local Purchasing Power Index'].mean()-1)
    colormat2=np.where(PP30['Local Purchasing Power Index']>0, 'g','r')
    a = PurchasingPower.head(20)['City']
    b = PurchasingPower.head(20)['Local Purchasing Power Index']
    plt.title("Purchasing Power")
    plt.xlabel("% Disparity")
    plt.ylabel("Cities")
    plt.barh(a,b,color =colormat2, edgecolor="black")
    plt.show()
    plt.close()

def main():
    sorted_df = mergeData()
    Cost, PurchasingPower =FixData(sorted_df)
    Charting(Cost, PurchasingPower)
    #you can replace the cities in your code with other cities from the cost of living index file provided for other comparisons
    
    work = PurchasingPower.loc[PurchasingPower['City'] =='Dallas, TX, United States']
    live = Cost.loc[Cost['City'] =='Medellin, Colombia']
    Arbitrage = [live['Cost of Living Plus Rent Index'][0]-work['Cost of Living Plus Rent Index'][1],work['Local Purchasing Power Index'][1]-live['Local Purchasing Power Index'][0]]
    print(work['Local Purchasing Power Index'][1])
    print(live['Local Purchasing Power Index'][0])
    data = {'Cost Of Living Arbitrage':  round(Arbitrage[0]),
        'Income Arbitrage': round(Arbitrage[1])}
    print(data)
main()
