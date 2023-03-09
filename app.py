import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympic Analysis')
st.sidebar.image('https://cdn.pixabay.com/photo/2013/02/15/10/58/blue-81847_1280.jpg')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years = helper.get_data_list(df, 'Year')
    countries = helper.get_data_list(df, 'region')
    year = st.sidebar.selectbox('Select Year', years)
    country = st.sidebar.selectbox('Select Country', countries)

    medal_tally = helper.get_medal_tally(df, year, country)

    if year == 'overall' and country == 'overall':
        st.title('Overall Olympic Medal Tally')
    elif year == 'overall' and country != 'overall':
        st.title(country + ' Olympic Analysis')
    elif year != 'overall' and country == 'overall':
        st.title('Olympic Analysis for ' + str(year))
    elif year != 'overall' and country != 'overall':
        st.title(country + ' Olympic Analysis for ' + str(year))

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    total_editions = df['Year'].unique().shape[0] - 1
    total_cities = df['City'].unique().shape[0]
    total_sports = df['Sport'].unique().shape[0]
    total_events = df['Event'].unique().shape[0]
    total_athletes = df['Name'].unique().shape[0]
    total_nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(total_editions)
    with col2:
        st.header('Hosts')
        st.title(total_cities)
    with col3:
        st.header('Sports')
        st.title(total_sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(total_events)
    with col2:
        st.header('Nations')
        st.title(total_nations)
    with col3:
        st.header('Athletes')
        st.title(total_athletes)

    nations_over_years = helper.data_over_years(df, 'region')
    fig = px.line(nations_over_years, x="Edition", y='No. Of Countries', title='No. Of Countries Over Editions')
    st.plotly_chart(fig)

    events_over_years = helper.data_over_years(df, 'Event')
    fig = px.line(events_over_years, x="Edition", y='No. Of Events', title='No. Of Events Over Editions')
    st.plotly_chart(fig)

    athletes_over_years = helper.data_over_years(df, 'Name')
    fig = px.line(athletes_over_years, x="Edition", y='No. Of Athletes', title='No. Of Athletes Over Editions')
    st.plotly_chart(fig)


    st.header('Sprorts Events Over Editions')
    event_table = helper.get_event_table(df)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(event_table, annot=True)
    st.pyplot(fig)


    st.header('Top Athletes')
    sports = helper.get_data_list(df, 'Sport')
    sport = st.selectbox('Select Sport', sports)
    top_info = helper.most_successful(df, sport)
    st.table(top_info)


if user_menu == 'Country-wise Analysis':
    st.sidebar.header('Country-wise Analysis')
    countries = helper.get_data_list(df, 'region')
    countries.pop(0)
    country = st.sidebar.selectbox('Select Country', countries)

    tally = helper.get_medal_tally(df, 'overall', country)
    tally = tally[['Year', 'total']]

    st.header('Country Performance Over Years')
    fig = px.line(tally, x="Year", y='total')
    st.plotly_chart(fig)

    st.header('Sport Performance of ' + country)
    cnt_sport = helper.get_country_sport_table(df, country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(cnt_sport, annot=True)
    st.pyplot(fig)

    st.header('Top 10 Athlete Of ' + country)
    top_ath = helper.most_successful_countrywise(df, country)
    if top_ath.shape[0] == 0:
        st.info('No athelete from ' + country + ' has won the medals.')
    else:
        st.table(top_ath)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)


    st.header('Weight Vs Height in the sport')
    sports = helper.get_data_list(df, 'Sport')
    sport = st.selectbox('Select Sport', sports)
    temp_df = helper.wt_vs_ht(df, sport)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.scatterplot(x=temp_df['Height'], y=temp_df['Weight'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.header("Men vs Women Participation Over Years")
    both = helper.men_vs_women(df)
    fig = px.line(both, x="Year", y=['Men', 'Women'])
    fig.update_layout(autosize=False, width=800, height=400)
    st.plotly_chart(fig)

