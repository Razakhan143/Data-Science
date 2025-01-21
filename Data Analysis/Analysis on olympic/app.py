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
    
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    
    if selected_year =='Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year =='Overall' and selected_country != 'Overall':
        st.title('Medal Tally in '+ str(selected_year) + 'in Olympics')
    if selected_year !='Overall' and selected_country == 'Overall':
        st.title(selected_year+ 'Overall performance')
    if selected_year !='Overall' and selected_country != 'Overall':
        st.title(selected_country+'Performance in' + str(selected_year)+'Olympics')
    
    st.table(medal_tally)
    
    
    
#for running the app
#streamlit run "D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\app.py"
