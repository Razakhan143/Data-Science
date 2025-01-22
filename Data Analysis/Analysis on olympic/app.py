import streamlit as st
import pandas as pd
import Preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# Load data
df = pd.read_csv(r'Data Analysis\Analysis on olympic\dataset\Data_set\Olympics_2024_.csv')
df = df[df['Season'] == 'Summer']

# Page configuration
st.set_page_config(
    page_title="Olympics Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Sidebar
st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image('Olympic logo.png', use_container_width=True)
st.sidebar.markdown("Explore the rich history of the Olympics through interactive data visualizations.")

# Sidebar menu
user_menu = st.sidebar.radio(
    'Navigation',
    ['Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-wise Analysis']
)

# Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header("🎖 Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years, index=0)
    selected_country = st.sidebar.selectbox("Select Country", country, index=0)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    st.title('🏅 Medal Tally')
    st.write("Explore the medal tallies for different countries and years.")

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader(' Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader(f'🎯 Medal Tally in {selected_year} Olympics')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader(f'🏅 {selected_country} Overall Performance')
    else:
        st.subheader(f'🎖 {selected_country} Performance in {selected_year} Olympics')

    st.table(medal_tally)

# Overall Analysis Section
if user_menu == "Overall Analysis":
    st.title("📊 Top Statistics")
    st.markdown("An overview of key statistics in the history of the Olympics.")

    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    # Display key stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Editions", editions)
    with col2:
        st.metric("Host Cities", cities)
    with col3:
        st.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Events", events)
    with col2:
        st.metric("Nations", nations)
    with col3:
        st.metric("Athletes", athletes)

    # Line charts for trends
    st.markdown("---")
    st.title("📈 Trends Over the Years")
    nations_over_time = helper.data_overtime(df, 'region')
    fig = px.line(
        nations_over_time, 
        x="Edition", y="region", 
        title="Participating Nations Over Time",
        labels={"Edition": "Year", "region": "Number of Nations"}, 
        markers=True,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    nations_over_time = helper.data_overtime(df,'Event')

    fig = px.line(nations_over_time,x="Edition",y="Event",title="Events Over Time",labels={"Edition": "Year", "Events": "Number of Events"},markers=True)
    fig.update_layout(title_font=dict(size=14, family="Arial", color="black"),xaxis=dict(title="Year", showgrid=True, gridcolor="lightgrey"),yaxis=dict(title="Number of Events Over years", showgrid=True),template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    athletes_over_time = helper.data_overtime(df,'Name')

    fig = px.line(athletes_over_time,x="Edition",y="Name",title="Athletes Over Time",labels={"Edition": "Year", "Name": "Athletes of Events"},markers=True)
    fig.update_layout(title_font=dict(size=14, family="Arial", color="black"),xaxis=dict(title="Year"),yaxis=dict(title="Number of Athletes Over years", gridcolor="lightgrey"),template="plotly_white")
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

# Country-Wise Analysis Section
if user_menu == "Country-Wise Analysis":
    st.sidebar.title(" Country-Wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_coun = st.sidebar.selectbox("Select a Country", country_list)
    country_medal_tally = helper.year_wise_medal_tally(df, selected_coun)

    st.title(f"🏅 {selected_coun}'s Medal Tally Over the Years")
    fig = px.line(
        country_medal_tally, 
        x="Year", y="Medal", 
        title=f"🎖 {selected_coun}'s Medal Trend",
        markers=True,
        labels={"Year": "Year", "Medal": "Number of Medals"},
        template="plotly_white"
    )
    st.plotly_chart(fig)
    
 
    st.title('🎖'+selected_coun + ' Excels in the following Sports')
    
    pivot_data=helper.country_event_heatmap(df,selected_coun)
    pivot_data = pivot_data.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pivot_data,  cbar_kws={'label': 'Event Count'}, ax=ax)

    for i in range(pivot_data.shape[0]): 
        for j in range(pivot_data.shape[1]):  
            ax.text(j + 0.5, i + 0.5, str(pivot_data.iloc[i, j]), ha='center', va='center', fontsize=12, color='white')

    st.pyplot(fig)
    
    
    st.title('Top 10 🎖 Athletes of '+selected_coun )
    top10= helper.most_successful_countryathlete(df,selected_coun)
    st.table(top10)
    
    
    
    
    
    
if user_menu == "Athlete-wise Analysis":
    st.title("🏃 Athlete Analysis")

    athlete_df = df.dropna(subset=['Name', 'region'])
    age_data = [
        athlete_df['Age'].dropna(),
        athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna(),
        athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna(),
        athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    ]
    age_labels = ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists']

    # Age distribution
    fig = ff.create_distplot(age_data, age_labels, show_hist=False, show_rug=False)
    fig.update_layout(title="🏅 Age Distribution of Medalists", template="plotly_white")
    st.plotly_chart(fig)




            
        
    medal = ['Gold', 'Silver', 'Bronze']

    st.title('Distribution of Age WRT Sport :')
    medal_type = st.selectbox("Select Medal Type", medal, label_visibility='visible')
    famous_sport = df['Sport'].unique()
    x = []
    name = []
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        spor = temp_df[temp_df['Medal'] == medal_type]['Age'].dropna()
        x.append(spor)
        name.append(sport)

    selected_sports = st.multiselect('Select Sports to View', name)

    # Check if any sports are selected
    if selected_sports:
        # Filter data for selected sports
        selected_data = [x[name.index(sport)] for sport in selected_sports]

        # Create the plot
        fig = ff.create_distplot(selected_data, selected_sports, show_hist=False, show_rug=False)
        fig.update_layout(
            title="🏅 Age Distribution of Medalists by Sport",
            xaxis_title="Age",
            yaxis_title="Density",
            template="plotly_white",
            legend_title="Sports",
        )
        st.plotly_chart(fig)

        


    
    st.title('Weight VS Height of Athletes ' )
    selected_sport = st.selectbox('Select Sports to View', name)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=40)
    st.pyplot(fig)
    


    # Men vs Women Participation
    st.markdown("---")
    st.title("Gender Participation Over the Years")
    gender_trend = helper.men_vs_women(df)
    fig = px.line(
        gender_trend, 
        x="Year", y=["Male", "Female"], 
        title="Gender Participation Trends",
        markers=True,
        template="plotly_white"
    )
    st.plotly_chart(fig)























#for running the app
#streamlit run "D:\PROFESSIONAL\AI\Data Science\Data Analysis\Analysis on olympic\app.py"