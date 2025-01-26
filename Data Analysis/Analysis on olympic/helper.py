import numpy as np
import pandas as pd

    
def fetch_medal_tally(df, year, country):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_tally
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_tally[medal_tally['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    else:
        temp_df = medal_tally[(medal_tally['Year'] == int(year)) & (medal_tally['region'] == country)]

    if year == 'Overall' and country != 'Overall':
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
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
    
def year_wise_medal_tally(df,country):
    
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    temp_df=temp_df[temp_df['region']==country]
    final_df=temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    temp_df=temp_df[temp_df['region']==country]
    return temp_df


def most_successful_countryathlete(df,country):
    temp_df = df.dropna(subset=['Medal'])
    
    temp_df = temp_df[temp_df['region']==country]
        
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates(['Name'])
    x.rename(columns={'count':'Medals'},inplace=True)
    return x 


def weight_v_height(df,sport):
    athlete_df=df.dropna(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    temp_df = athlete_df[athlete_df['Sport']== sport]
    return temp_df

def men_vs_women(df):
    athlete_df=df.dropna(subset=['Name','region'])
    
    men= athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women= athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    women.rename(columns={'Name':'Female'},inplace=True)
    men.rename(columns={'Name':'Male'},inplace=True)
    final = men.merge(women,on='Year',how='left')
    final.fillna(0,inplace=True)
    
    return final
