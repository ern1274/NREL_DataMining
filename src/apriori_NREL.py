
import NREL_DataMining.src.Data_Preprocess as preprocess
# Convert this code to fit NREL dataframe and set attributes beforehand.
# Assume you are getting one single collection of data, separation of data based upon
# regions and/or other attirbutes are handled outside of this algorithm.
# This reduces complexity

class Itemset:
    def __init__(self, items, count):
        self.items = items
        self.count = count

def frequency_check(subsets, Lki):
    fullset = [itemset.items for itemset in Lki]
    for set in subsets:
        if set not in fullset:
            return False
    return True

def joinable(p_list, q_list, k):
    if (k - 2) == 0:
        return True
    p_k_list = [p_list[i] for i in range(k - 2)]
    q_k_list = [q_list[i] for i in range(k - 2)]
    p_comp = p_list[k-2]
    q_comp = q_list[k-2]
    #print("P and q comp respectively")
    #print(p_comp)
    #print(q_comp)
    #print("done")
    if p_k_list == q_k_list and q_comp > p_comp:
        return True
    return False

def make_subsets(joined, p, q):
    subsets = []
    for i in range(len(joined)-1,-1,-1):
        subset = joined.copy()
        del subset[i]
        subsets.append(subset)
    return [item for item in subsets if item not in [p,q]]

def apriori_gen(Lki, k):
    total_joined = 0
    total_pruned = 0
    candidates = []
    for p in range(0, len(Lki)):
        p_select = list(Lki[p].items)
        for q in range(p + 1, len(Lki)):
            q_select = list(Lki[q].items)
            is_joinable = joinable(p_select,q_select, k)
            if is_joinable:
                total_joined += 1
                joined = p_select + [q_select[k-2]]
                subsets = make_subsets(joined, p_select, q_select)
                if frequency_check(subsets, Lki):
                    new_c = Itemset(joined, 0)
                    candidates.append(new_c)
                else:
                    total_pruned += 1
    return candidates, total_joined, total_pruned

def apriori(k, data, item_attribs, minsup):
    i = 1
    if k < 1:
        return
    lki = apriori_L1(item_attribs, data, minsup)
    while i < k:
        i += 1
        row_list = []
        for index, row in data.iterrows():
            row = set([str(iid_attrib +":" +str(preprocess.bucket_data(iid_attrib,row[iid_attrib]))) for iid_attrib in item_attribs])
            row_list.append(row)
        candidates, total_joined, total_pruned = apriori_gen(lki, i)
        print("Total joined: " + str(total_joined) + " Total Pruned: " + str(total_pruned))
        most_occurring = Itemset([],0)
        for row in row_list:
            for candidate in candidates:
                #print("Row and Candidate")
                #print(row)
                #print(candidate.items)
                c_itemset = candidate.items
                if set(c_itemset).issubset(row):
                    candidate.count += 1
                    if most_occurring.count < candidate.count:
                        most_occurring = candidate
        total_insuff_support = sum([True for h in range(len(candidates)) if candidates[h].count < minsup])
        lki = [candidates[h] for h in range(len(candidates)) if candidates[h].count >= minsup]
        print("L"+str(i)+" Finished: ")
        #print_apriori_data(lki)
        print("Total Insufficient Support: " + str(total_insuff_support))
        print("Most Occurring itemset: ")
        print(str(most_occurring.items) + " : " + str(most_occurring.count))
    print("Returning L" + str(k))
    return lki

def print_apriori_data(lk):
    for entry in lk:
        print(str(entry.items) + " : " + str(entry.count))


def apriori_L1(item_attribs, df, minsup):
    transactions = {}
    for index, row in df.iterrows():
        iids = []
        for iid_attrib in item_attribs:
            conv = iid_attrib + ":"+str(preprocess.bucket_data(iid_attrib, row[iid_attrib]))
            iids.append(conv)
        transactions[index] = iids

    counts = {}
    selected = []
    for iids in transactions.values():
        for item_id in iids:
            if item_id not in counts:
                counts[item_id] = 0
            counts[item_id] += 1
            if counts[item_id] >= minsup and item_id not in selected:
                selected.append(item_id)
    lone = []
    for item_id in selected:
        lone.append(Itemset([item_id], counts[item_id]))
    return lone



