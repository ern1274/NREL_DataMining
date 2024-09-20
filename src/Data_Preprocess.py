
def organize_by_month(df):
    organized_df = {'ALL': {}}
    # 'ALL' IS A MONTH DICT NOT REGION DICT consisting of all data organized regardless of region
    for country in df.keys():
        if country not in organized_df.keys():
            organized_df[country] = {}
        for region in df[country].keys():
            regional_df = df[country][region]

            if 'Month' not in regional_df.keys():
                print("Month does not exist as an attribute within the dataframe")
                return None

            lst = {}
            for index, row in regional_df.iterrows():
                month = int(row['Month'])

                if month-1 not in lst.keys():
                    lst[month-1] = []

                lst[month - 1].append(row)
                organized_df[country][region] = lst

            organized_df['ALL'] = {**organized_df['ALL'], **lst}
    return organized_df
