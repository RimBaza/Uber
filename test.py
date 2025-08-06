import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("NYC Uber Ridesharing Data")

df = pd.read_csv("uber-raw-data-sep14.csv")
df['Date/Time'] = pd.to_datetime(df['Date/Time'])
df['date'] = df['Date/Time'].dt.date
df['hour'] = df['Date/Time'].dt.hour

col1, col2 = st.columns([1, 2])

with col1:
    w1 = sorted(df['date'].unique())
    selected_date = st.selectbox("Choisissez une date :", w1)
    w2 = sorted(df[df['date'] == selected_date]['hour'].unique())
    selected_hour = st.selectbox("Choisissez une heure :", w2)

with col2:
    st.write("Explorez les trajets Uber par date et heure.")

# Filtrer les données
filtered_data = df[(df['date'] == selected_date) & (df['hour'] == selected_hour)]

# Calculer le centre
lat_center = np.average(filtered_data['Lat'])
lon_center = np.average(filtered_data['Lon'])

# Créer la carte sans Mapbox
layer = pdk.Layer(
    "HeatmapLayer",
    data=filtered_data[['Lat', 'Lon']],
    get_position='[Lon, Lat]',
    get_color=[255, 140, 0, 160] , # orange plus visible
    get_radius=80,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=lat_center,
    longitude=lon_center,
    zoom=11,
    pitch=0
)

# Affichage
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style=None  # pas de Mapbox
))




hr_count = df[df['date'] == selected_date].groupby('hour').size()

most_active = hr_count.idxmax()
least_active = hr_count.idxmin()

most_count=hr_count.max()
least_count=hr_count.min()

st.markdown(f"🕒 Heure la plus active : **{most_active}h** avec **{most_count} trajets**")
st.markdown(f"🕒 Heure la moins active : **{least_active}h** avec **{least_count} trajets**")

st.bar_chart(hr_count)