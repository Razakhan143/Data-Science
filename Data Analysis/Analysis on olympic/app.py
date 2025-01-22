import streamlit as st
import pandas as pd
import Preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df=pd.read_csv(r'D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\dataset\Data_set\Athlete_events.csv')
region_df=pd.read_csv(r"D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\dataset\Data_set\noc_regions.csv")

df = Preprocessor.preprocessor(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('Olympic logo.png')

# page_bg_img = '''
# <style>
# .stApp {
#     background-image: url("background.jpg"); /* Use a public image URL */
#     background-repeat: repeat; /* Repeat the image */
#     background-size: auto; /* Keep original size */
#     background-attachment: fixed; /* Optional: Make the background fixed while scrolling */
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)



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

    pivot_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pivot_data,  cbar_kws={'label': 'Event Count'}, ax=ax)

    for i in range(pivot_data.shape[0]): 
        for j in range(pivot_data.shape[1]):  
            ax.text(j + 0.5, i + 0.5, str(pivot_data.iloc[i, j]), ha='center', va='center', fontsize=12, color='white')

    st.pyplot(fig)
    
    
    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_Sport= st.selectbox('Select a Sport',sport_list)
    x= helper.most_successful(df,selected_Sport)
    st.table(x)
    
    
    
    
if user_menu =='Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    country_list =df['region'].dropna().unique().tolist()
    country_list.sort() 
    
    selected_coun=st.sidebar.selectbox('Select a Country',country_list)

    st.title(selected_coun + ' Medal Tally Over the Years')
    year_medal = helper.year_wise_medal_tally(df,selected_coun)

    fig = px.line(year_medal, x="Year", y="Medal", title="Year Wise Medal Tally", labels={"Year": "Year", "Medal": "Number of Medals"}, markers=True).update_layout(title=dict(text="Participating Nations Over Time", font=dict(size=22, family="Arial Black", color="darkblue"), x=0.2, y=0.9), xaxis=dict(title="Year", showgrid=True, gridcolor="lightgrey", tickangle=45), yaxis=dict(title="Number of Medals", showgrid=True, gridcolor="lightgrey", tickformat=","), template="plotly_white", hovermode="x unified", legend=dict(title="Legend", orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
    fig.add_annotation(x=year_medal.loc[year_medal["Medal"].idxmax(), "Year"], y=year_medal["Medal"].max(), text=f"Highest ({year_medal['Medal'].max()})", showarrow=True, arrowhead=2, arrowsize=1, arrowcolor="green", font=dict(color="green", size=12))
    fig.add_annotation(x=year_medal.loc[year_medal["Medal"].idxmin(), "Year"], y=year_medal["Medal"].min(), text=f"Lowest ({year_medal['Medal'].min()})", showarrow=True, arrowhead=2, arrowsize=1, arrowcolor="red", font=dict(color="red", size=12))
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.title(selected_coun + ' Excels in the following Sports')
    
    pivot_data=helper.country_event_heatmap(df,selected_coun)
    pivot_data = pivot_data.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pivot_data,  cbar_kws={'label': 'Event Count'}, ax=ax)

    for i in range(pivot_data.shape[0]): 
        for j in range(pivot_data.shape[1]):  
            ax.text(j + 0.5, i + 0.5, str(pivot_data.iloc[i, j]), ha='center', va='center', fontsize=12, color='white')

    st.pyplot(fig)
    
    
    st.title('Top 10 Athletes of '+selected_coun )
    top10= helper.most_successful_countryathlete(df,selected_coun)
    st.table(top10)
    
    
    
    
if user_menu =='Athlete-wise Analysis':
    
    athlete_df=df.dropna(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silve']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    
    
    data = [x1, x2, x3, x4]
    labels = ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']
    colors = ['blue', 'gold', 'silver', 'brown']

    plt.figure(figsize=(10, 6))
    for i, x in enumerate(data):
        sns.kdeplot(x, label=labels[i], color=colors[i], linewidth=2)

    plt.title('Age Distribution by Medal Type', fontsize=16)
    plt.xlabel('Age', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.legend(title="Category", fontsize=12)
    plt.grid(alpha=0.3)
    st.title('Age Wise Distribution')
    # Streamlit support
    st.pyplot(plt)
    
    
    
    
    
    
    
    medal=['Gold','Silver','Bronze']
    
    st.title('Distribution of Age WRT Sport : ')
    medal_type = st.selectbox("Select Medal Type",medal,label_visibility='visible')
    famous_sport= df['Sport'].unique()
    x = []
    name = []
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport']== sport]
        spor=temp_df[temp_df['Medal']==medal_type]['Age'].dropna()
        x.append(spor)
        name.append(sport)
    selected_sports = st.multiselect('Select Sports to View', name)

# Check if any sports are selected
    if selected_sports:
        # Filter data for selected sports
        selected_data = [x[name.index(sport)] for sport in selected_sports]

        # Create the plot
        plt.figure(figsize=(12, 8))

        # Plot KDE for each selected sport on the same graph
        for i, sport_data in enumerate(selected_data):
            sns.kdeplot(sport_data, label=selected_sports[i])

        # Customize the plot
        plt.title(medal_type+" Medalists' Age Distribution by Sport ", fontsize=16)
        plt.xlabel("Age", fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.legend(title="Sports")

        # Display the plot in Streamlit
        st.pyplot(plt)

    
    st.title('Weight VS Height of Athletes ' )
    selected_sport = st.selectbox('Select Sports to View', name)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=40)
    st.pyplot(fig)
    
    
    st.title('Men VS Women')
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"], title="Participation Over the Years by Gender", labels={"value": "Number of Participants", "variable": "Gender"}, markers=True).update_traces(marker=dict(size=8), line=dict(width=3)).update_layout(title_font=dict(size=20, family="Arial", color="darkblue"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), plot_bgcolor="white")
    
    st.plotly_chart(fig)
    
    
#for running the app
#streamlit run "D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\app.py"
