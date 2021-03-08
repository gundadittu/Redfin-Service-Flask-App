import pandas

from . import data_factory

def _convert_df_to_search_results(df): 
    results=[]
    for index, row in df.iterrows():
        result = { 
            'mls_no': row['MLS#'], 
            'property_type': row['PROPERTY TYPE'], 
            'address': row['ADDRESS'], 
            'zip': row['ZIP'], 
            'price': row['PRICE'], 
            'beds': row['BEDS'], 
            'baths': row['BATHS'], 
            'square_feet': row['SQUARE FEET'], 
            'year_built': row['YEAR BUILT'], 
            'price_per_square_foot': row['$/SQUARE FEET'], 
            'url': row['URL']
        }
        results.append(result)

    return results

def _filter_df_by_queryable_street_name(queryable_street_name, df): 
    if len(df.index) == 0:
        return df 
    return df[df['QUERYABLE STREET NAME'] == queryable_street_name]

def _filter_df_by_queryable_street_no(street_no, df):
    if len(df.index) == 0:
        return df  
    df['CONTAINS DESIRED STREET NO'] = df.apply(lambda row: (street_no in data_factory.extract_queryable_street_nos(row['ADDRESS'])), axis=1)
    return df[df['CONTAINS DESIRED STREET NO'] == True]

def get_all_sf_listings(): 
    df = data_factory.load_sf_listings_df()

    results = _convert_df_to_search_results(df)
    return results 

def get_sf_listings_by_street_address(street_address_input): 
    df = data_factory.load_queryable_sf_listing_df()

    street_name_input = data_factory.extract_queryable_street_name(street_address_input)
    df = _filter_df_by_queryable_street_name(street_name_input, df)

    street_nos_list = data_factory.extract_queryable_street_nos(street_address_input)
    if len(street_nos_list) > 0: 
        queryable_street_no = street_nos_list[0]
        df = _filter_df_by_queryable_street_no(queryable_street_no, df)

    results = _convert_df_to_search_results(df)
    return results