import streamlit as st
from maps.maps import Plotter
from maps.utils import DataQuery, south_italy
import folium
import streamlit.components.v1 as components

gdf = DataQuery(regions=south_italy).get_municipality_data()
plotter = Plotter(gdf=gdf)


st.set_page_config(layout="wide")

st.title("Italian Municipalities with Pension Benefits for Expats")

st.sidebar.title('Options')

tax_benefit_only = st.sidebar.checkbox('Only municipalities with tax benefit?')

if tax_benefit_only:
    st.write('Showing only municipalities with tax benefit.')
else:
    st.write('Showing all municipalities.')

with st.spinner('Loading map...'):
    m = plotter.explore_plot()
    fig = folium.Figure().add_child(m).render()
    print(type(fig))
    components.html(fig, height=800)