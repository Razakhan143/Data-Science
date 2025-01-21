import numpy as np

    
def fetch_medal_tally(df,year,country):
    
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df = medal_tally
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df = medal_tally[medal_tally['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df = medal_tally[medal_tally['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        temp_df = medal_tally[(medal_tally['Year']==int(year)) & (medal_tally['region']==country)]
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:    
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']
    
    return x 

def country_year_list(df):
    
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country

def data_overtime(df,col):
    nations_over_time = df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns={'Year':'Edition','count':col},inplace=True)
    nations_over_time = nations_over_time.sort_values(by="Edition")
    return nations_over_time


def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates(['Name'])
    x.rename(columns={'count':'Medals'},inplace=True)
    return x   
    