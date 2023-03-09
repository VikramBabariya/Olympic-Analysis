def get_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if (year == 'overall' and country == 'overall'):
        temp_df = medal_df
    elif (year == 'overall' and country != 'overall'):
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif (year != 'overall' and country == 'overall'):
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif (year != 'overall' and country != 'overall'):
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if (flag == 0):
        temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                            ascending=False).reset_index()
    else:
        temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    temp_df['total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    return temp_df


def get_data_list(df, col):
    data = df[col].dropna().unique().tolist()
    data.sort()
    data.insert(0, 'overall')

    return data

def data_over_years(df, col):
    data = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    if col == 'region': data.rename(columns={'index': 'Edition', 'Year': 'No. Of Countries'}, inplace=True)
    if col == 'Event': data.rename(columns={'index': 'Edition', 'Year': 'No. Of Events'}, inplace=True)
    if col == 'Name': data.rename(columns={'index': 'Edition', 'Year': 'No. Of Athletes'}, inplace=True)
    return data

def get_event_table(df):
    data = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pt = data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    return pt


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top = temp_df['Name'].value_counts().reset_index()
    top_info = top.merge(df, how='left', left_on='index', right_on='Name')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')

    top_info.rename(columns={'index': 'Name', 'Name_x': 'Medals', 'region': 'Country'}, inplace=True)

    return top_info

def get_country_sport_table(df, country):
    temp_df = df
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    top = temp_df['Name'].value_counts().reset_index().head(10)
    top_info = top.merge(df, how='left', left_on='index', right_on='Name')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')

    top_info.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return top_info

def wt_vs_ht(df, sport):
    ath_df = df.drop_duplicates(subset=['Name', 'Sex', 'region'])
    ath_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'overall':
        temp_df = ath_df[ath_df['Sport'] == sport]
        return temp_df
    return ath_df

def men_vs_women(df):
    ath_df = df.drop_duplicates(subset=['Name', 'Sex', 'region'])
    men = ath_df[ath_df['Sex'] == 'M'].groupby('Year').count()[['Name']].reset_index()
    women = ath_df[ath_df['Sex'] == 'F'].groupby('Year').count()[['Name']].reset_index()
    both = men.merge(women, how='left', on='Year')
    both.fillna(0, inplace=True)
    both.rename(columns={'Name_x':'Men', 'Name_y':'Women'}, inplace=True)
    return both

