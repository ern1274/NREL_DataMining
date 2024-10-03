import pandas as pd
import NREL_DataMining.src.Data_Preprocess as preprocess
# Convert this code to fit NREL dataframe and set attributes beforehand.
# Assume you are getting one single collection of data, separation of data based upon
# regions and/or other attirbutes are handled outside of this algorithm.
# This reduces complexity
def apriori_L1(item_attribs, df, minsup):
    transactions = {}
    for index, row in df.iterrows():
        iids = []
        for iid_attrib in item_attribs:
            conv = iid_attrib + ":"+str(preprocess.bucket_data(iid_attrib, row[iid_attrib]))
            iids.append(conv)
        transactions[index] = iids

    counts = {}
    selected = set()
    for iids in transactions.values():
        for item_id in iids:
            if item_id not in counts:
                counts[item_id] = 0
            counts[item_id] += 1
            if counts[item_id] >= minsup and item_id not in selected:
                selected.add(item_id)
    lone = {}
    # cant sort because its not comparable data
    for item_id in selected:
        lone[item_id] = counts[item_id]
    return lone

def prep(data):
    #data is array of panda Series, convert to Dataframe.
    df = pd.DataFrame(data)
    item_attribs = ['Month','Temperature','Wind Speed', 'DNI', 'GHI']
    minsup = 25
    lone = apriori_L1( item_attribs, df, minsup)
    print(lone)
