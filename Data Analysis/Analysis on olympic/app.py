import streamlit as st
import pandas as pd
import Preprocessor,helper
df=pd.read_csv(r'D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\dataset\Data_set\Athlete_events.csv')
region_df=pd.read_csv(r"D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\dataset\Data_set\noc_regions.csv")


df = Preprocessor.preprocessor(df,region_df)

st.sidebar.title("Olympics Analysis")

user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','overall Analysis','Country-Wise Analysis','Athlete-wise Analysis')
    
)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    
    medal_tally = helper.medal_tally(df)
    st.dataframe(medal_tally)
    
    
    
#for running the app
#streamlit run "D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\app.py"
