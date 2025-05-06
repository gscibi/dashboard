import pandas as pd
def data_cleaning(df):
    '''
    This function cleans the data from the df
    Input/Output
    df = pd.Data Frame
    '''
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_', regex=False)
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y') # convert date to datetime
    df['amount'] = df['amount'].replace('[\$,]', '', regex=True).astype(float) #convert amount into float
    return df
