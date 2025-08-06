import streamlit as st 
import pandas as pd 
import pydeck as pdk
import numpy as np

st.set_page_config(layout="wide")
st.title("NYC Uber Ridesharing Data")

st.markdown(
    """
    <style>
    .css-1d391kg {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        padding-top: 0.5rem !important;
    }
    .css-18e3th9 {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

df=pd.read_csv("uber-raw-data-sep14.csv")

df['Date/Time'] = pd.to_datetime(df['Date/Time'])
df['date'] = df['Date/Time'].dt.date
df['hour'] = df['Date/Time'].dt.hour

#st.dataframe(df.head())

col1, col2 = st.columns([1, 2], gap="small")

with col1:
    w1= sorted(df['date'].unique())
    selected_date= st.selectbox("Choisissez une date :", w1 )

    w2=sorted(df[ df['date'] == selected_date]['hour'].unique())
    selected_hour = st.selectbox("Choisissez une heure :" , w2)

with col2:
    st.write(
        """
       
        Examining how Uber pickups vary over time in New York City's and at its major regional airports.
        By sliding the slider on the left you can view different slices of time and explore different transportation trends.
        """  )

def filterdata(df, hour):
    return df[df['Date/Time'].dt.hour == hour]

@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

midpoint = mpoint(df["Lat"], df["Lon"])

def map(data, lat, lon, zoom):
    data_to_plot = data[['Lat', 'Lon']].copy() 

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v12",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data_to_plot,
                    get_position=["Lon", "Lat"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
            tooltip={"text": "Lat: {Lat}\nLon: {Lon}"},

        )
    )


with st.container():
    st.write(f"**All New York City from {selected_hour}:00 to {(selected_hour + 1) % 24}:00**")
    filtered_data = filterdata(df, selected_hour)
    map(filtered_data, midpoint[0], midpoint[1], 11)


#row1, row2, row3, row4 = st.columns((2, 1, 1, 1))

#with row1 :
#    st.write(  f"""**All New York City from {selected_hour}:00 and {(selected_hour + 1) % 24}:00**""" )
#    map(filterdata(df, selected_hour), midpoint[0], midpoint[1], 11)
   #map(fil)


st.write(filtered_data.dtypes)


