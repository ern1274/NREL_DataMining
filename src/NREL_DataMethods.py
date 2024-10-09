import NREL_DataMining.src.apriori_NREL as apriori
import pandas as pd

def prep_apriori(data):
    #data is array of panda Series, convert to Dataframe.
    df = pd.DataFrame(data)
    item_attribs = ['Month','Temperature','Wind Speed', 'DNI', 'GHI']
    minsup = 10
    lk = apriori.apriori(3, df, item_attribs, minsup)
    apriori.print_apriori_data(lk)

