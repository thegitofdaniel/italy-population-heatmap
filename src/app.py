import folium
import streamlit as st
import streamlit.components.v1 as components
from maps.maps import Plotter
from maps.utils import DataQuery, north_italy, south_italy

st.set_page_config(layout="wide")

st.title("Italian Municipalities with Pension Benefits")

st.sidebar.title("Settings")

south_only = st.sidebar.checkbox("Only municipalities in the South")

tax_benefit_only = st.sidebar.checkbox(
    "Highlight municipalities with Pension Benefits"
)

if south_only:
    regions = south_italy
else:
    regions = north_italy + south_italy

gdf = DataQuery(level="municipality").filter(regions=regions)
plotter = Plotter(gdf=gdf)

# dq.gdf["region", "province", "municipality", "geometry", "population", "eligible_for_pension_benefit"]
with st.spinner("Loading map..."):
    if tax_benefit_only:
        m = plotter.explore_plot()
    else:
        m = plotter.explore_plot_without_highlight()
    fig = folium.Figure().add_child(m).render()

    components.html(fig, height=800)
