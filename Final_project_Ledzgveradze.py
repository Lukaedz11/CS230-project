"""
Class: CS230-5
Name: Luka Edzgveradze
Nuclear Explosions
"""

import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt

#Loads Data from CSV file
def data():
    df = pd.read_csv('nuclear_explosions.csv')
    df['latitude'] = pd.to_numeric(df['latitude'])
    return df

#Consolidates date month, day and Year for display in the map.
def date_column(df): #[DA8], [DA9]
    for index, row in df.iterrows():
        day = row['Date.Day']
        month = row['Date.Month']
        year = row['Date.Year']
        date_string = f"{month}/{day}/{year}"
        df.at[index, 'Date'] = date_string
    return df

#Counts and displays countries that has most explosions
def top_three(df): #[DA3], [DA2]
    country_counts = df['Weapon_source_country'].value_counts()
    sorted_country_counts = country_counts.sort_values(ascending=False)
    top3_countries = sorted_country_counts.head(3)
    st.write("**Top 3 countries with the most bombs dropped:**")
    for country, count in top3_countries.items():
        st.write(f"- {country}: {count} bombs dropped")

#Piecahrt for number of Explosions for each country
def piechart(df):#[VIZ2]
    countrysource = df['Weapon_source_country'].value_counts()
    labels = [f"{country}: {count} bombs" for country, count in countrysource.items()] #[PY4][PY5]
    plt.style.use('dark_background')
    plt.figure(figsize=(8, 8))
    plt.pie(countrysource.values, autopct='%1.1f%%', startangle=140, textprops={'color': 'black'})
    plt.title('Weapon Source Country', color='white')
    plt.legend(countrysource.index, title='Country', loc='best')
    plt.axis('equal')
    st.pyplot(plt)
    st.write("**Labels for the pie chart:**")
    for label in labels:
        st.write(label)

#LineChart that compares bomb explosions for USA and USSR. Would be useful for cold war statistics
def linechart_usa_ussr(df):
    filtered_df = df[df['Weapon_source_country'].isin(['USA', 'USSR'])]
    grouped_df = filtered_df.groupby(['Date.Year', 'Weapon_source_country']).size().unstack().fillna(0)
    grouped_df.plot(kind='line', color = ['blue', 'red'])
    plt.title('Number of Explosions by USA and USSR')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.legend(title='Country')
    st.pyplot()

#Pivottable that displays each year how may bombs were tested
def pivot_table(df): #[DA6][DA7][VIZ3]
    pivot_table = df.pivot_table(index='Date.Year', aggfunc='size').reset_index(name='Number of Explosions')
    st.write(pivot_table)
    plt.figure(figsize=(10, 6))
    plt.bar(pivot_table['Date.Year'], pivot_table['Number of Explosions'])
    plt.xlabel('Year')
    plt.ylabel('Number of Explosions')
    plt.title('Count of Explosions by Year')
    st.pyplot(plt)
    return pivot_table

#map
def pydeckmap(filtered_df): #[VIZ1][PY1][PY3]
    layer = pdk.Layer(
        'ScatterplotLayer',
        filtered_df,
        get_position='[longitude,latitude]',
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=1,
        radius_max_pixels=100,
        radius_min_pixels=1,
        get_radius=10,
        get_fill_color=[255, 140, 0],
    )

    r = pdk.Deck(
        layers=[layer],
        tooltip={
            "text": "{Data.Name}\n{Data.Type}, {Date}, {Data.Purpose} {Weapon_source_country}"}
    )
    st.pydeck_chart(r)

    return None


def main():
    df = data()
    st.title("Nuclear Explosions")
    tab1, tab2, tab3, tab4 = st.tabs(["Map", "Pie Chart", "Pivot Table", "Linechart"])
    country = df['Weapon_source_country'].value_counts()
    country_df = pd.DataFrame(country).reset_index()
    country_df.columns = ['Weapon_source_country', 'count']
    selected_country = st.sidebar.selectbox('Select a country', country.index)  # [DA4][ST1][ST4]
    slider_value = st.sidebar.slider("Select Value", 1945, 1998, 1972)
    dateDf = date_column(df)
    filtered_df = dateDf[(dateDf['Weapon_source_country'] == selected_country) & (
                dateDf['Date.Year'] == slider_value)]  # [DA5][ST1][ST2]
    show_all = st.sidebar.checkbox("Show All")  # [ST3]
    with tab1:  # [VIZ1]
        st.header("Map of Nuclear Explosions")
        if show_all:
            pydeckmap(df)
        else:
            pydeckmap(filtered_df)  # [PY3]
    with tab2:  # [VIZ2]
        piechart(df)
        top_three(df)
    with tab3:  # [VIZ3]
        pivot_table(df)
    with tab4:
        linechart_usa_ussr(df)


main()
st.set_option('deprecation.showPyplotGlobalUse', False) #streamlit gave me this code to shut warning so it is not connected to my project, just for technical purposes
#The support for global pyplot instances is planned to be removed soon. this is warning
