import pandas as pd

def _determine_if_street_name_component(x):         
    x = x.strip()
        
    UNWANTED_STREET_NAME_COMPONENTS = ["-", "plz", "plaza", "rd", "road", "hwy", "highway", "cir", "circle", "ter", "terrace", "pl", "place", "dr", "drive", "ct", "court", "unit", "st", "st.", "street", "ave", "ave.", "avenue", "way", "e", "w", "n", "s", "blvd", "boulevard", "ln", "lane"]
    if not x: 
        return False 
    elif x.isdigit(): 
        return False
    elif x[:-1].isdigit(): 
        return False 
    elif x.startswith("#"): 
        return False 
    elif x in UNWANTED_STREET_NAME_COMPONENTS: 
        return False 
    else: 
        return True 

def extract_queryable_street_name(raw_addr):
    if not raw_addr or not isinstance(raw_addr, str) : 
        return ""
    
    lc_addr = raw_addr.lower()

    unit_ind = lc_addr.find("unit")
    if unit_ind != -1: 
        lc_addr = lc_addr[:unit_ind]
    
    # remove penthouse substring
    ph_ind = lc_addr.find("ph")
    if ph_ind != -1: 
        lc_addr = lc_addr[:ph_ind]
    
    split = lc_addr.split()
    
    modified_split = list(filter(_determine_if_street_name_component, split))
    return ' '.join(modified_split)

def extract_queryable_street_nos(raw_addr): 
    if not raw_addr or not isinstance(raw_addr, str) : 
        return []
    
    lc_addr = raw_addr.lower()
    split = lc_addr.split()
    
    range_start_raw = split[0] if len(split) > 0 else "" 
    range_end_raw = split[2] if len(split) > 2 else "" 
    
    range_start = int(range_start_raw) if range_start_raw.isdigit() else -1
    ## check for street no with plot letter at end 
    range_start = int(range_start_raw[:-1]) if not range_start_raw.isdigit() and range_start_raw[:-1].isdigit() else range_start 
    
    range_end = int(range_end_raw) if range_end_raw.isdigit() else -1
    ## check for street no with plot letter at end 
    range_end = int(range_end_raw[:-1]) if not range_end_raw.isdigit() and range_end_raw[:-1].isdigit() else range_end
    
    range_delimitter_found = (split[1] == "-") if range_end > 0 else False
    
    if range_start > 0 and range_end > 0 and range_delimitter_found: 
        return list(range(range_start, range_end+1))
    elif range_start > 0: 
        return [range_start]
    else: 
        return []


def load_sf_listings_df(): 
    df = pd.read_csv("redfin_sf_listings.csv")
    df = df.rename(columns={
        "URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)": "URL",
        "ZIP OR POSTAL CODE": "ZIP"
    })
    df = df.drop(["FAVORITE", "INTERESTED", "LATITUDE", "LONGITUDE", "STATE OR PROVINCE", "CITY", "SALE TYPE", "SOLD DATE", "SOURCE"], axis=1)
    df = df.fillna('None')
    return df

def _add_queryable_street_name_to_df(df):
    if len(df.index) == 0:
        return df  
    df['QUERYABLE STREET NAME'] = df.apply(lambda row: extract_queryable_street_name(row['ADDRESS']), axis=1)
    return df

def load_queryable_sf_listing_df(): 
    df = load_sf_listings_df() 
    df_1 = _add_queryable_street_name_to_df(df)
    return df_1