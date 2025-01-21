import streamlit as st
import pandas as pd
import Preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv(r'D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\dataset\Data_set\Athlete_events.csv')
region_df=pd.read_csv(r"D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\dataset\Data_set\noc_regions.csv")

df = Preprocessor.preprocessor(df,region_df)

st.sidebar.title("Olympics Analysis")

user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-wise Analysis')
    
)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    
    if selected_year =='Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
        
    if selected_year !='Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+ str(selected_year) + ' in Olympics')
        
    if selected_year =='Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall performance')
        
    if selected_year !='Overall' and selected_country != 'Overall':
        st.title(selected_country+' Performance in ' + str(selected_year)+' Olympics')
    
    st.table(medal_tally)
    
if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique()[0]
    sports = df['Sport'].unique()[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
        
    with col2:
        st.header('Hosts')
        st.title(cities)
        
    with col3:
        st.header('Sports')
        st.title(sports)
        
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
        
    with col2:
        st.header('Nations')
        st.title(nations)
        
    with col3:
        st.header('Athletes')
        st.title(athletes)
            
    nations_over_time = helper.data_overtime(df,'region')

    fig = px.line(nations_over_time,x="Edition",y="region",title="Participating Nations Over Time",labels={"Edition": "Year", "No of Countries": "Number of Countries"},markers=True)
    fig.update_layout(title_font=dict(size=18, family="Arial", color="darkblue"),xaxis=dict(title="Year", showgrid=True, gridcolor="lightgrey"),yaxis=dict(title="Number of Participating Countries Over years", showgrid=True, gridcolor="lightgrey"),template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    
    nations_over_time = helper.data_overtime(df,'Event')

    fig = px.line(nations_over_time,x="Edition",y="Event",title="Events Over Time",labels={"Edition": "Year", "Events": "Number of Events"},markers=True)
    fig.update_layout(title_font=dict(size=18, family="Arial", color="darkblue"),xaxis=dict(title="Year", showgrid=True, gridcolor="lightgrey"),yaxis=dict(title="Number of Events Over years", showgrid=True, gridcolor="lightgrey"),template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    
    athletes_over_time = helper.data_overtime(df,'Name')

    fig = px.line(athletes_over_time,x="Edition",y="Name",title="Athletes Over Time",labels={"Edition": "Year", "Name": "Athletes of Events"},markers=True)
    fig.update_layout(title_font=dict(size=18, family="Arial", color="darkblue"),xaxis=dict(title="Year", showgrid=True, gridcolor="lightgrey"),yaxis=dict(title="Number of Athletes Over years", showgrid=True, gridcolor="lightgrey"),template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    st.title("Number Of Event Overtime (Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])

        # Create the pivot table with aggregation for counting events
    pivot_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)

    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pivot_data,  cbar_kws={'label': 'Event Count'}, ax=ax)

    # Manually add annotations to the heatmap cells
    for i in range(pivot_data.shape[0]):  # Iterate over rows
        for j in range(pivot_data.shape[1]):  # Iterate over columns
            ax.text(j + 0.5, i + 0.5, str(pivot_data.iloc[i, j]), ha='center', va='center', fontsize=12, color='white')

    # Display the plot in Streamlit
    st.pyplot(fig)
#for running the app
#streamlit run "D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\app.py"
