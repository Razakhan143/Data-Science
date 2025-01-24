import pandas as pd

def preprocessor(df):
    
    df = df[df['Season']=='Summer']
    df.drop_duplicates(inplace=True)
    
    df=pd.concat([df,pd.get_dummies(df['Medal']).astype('int')],axis=1)
    
    return df