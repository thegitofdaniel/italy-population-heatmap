import folium
import streamlit as st
import streamlit.components.v1 as components
from maps.maps import Plotter
from maps.utils import DataQuery, north_italy, south_italy

st.set_page_config(layout="wide")

st.title("Italian Municipalities with Pension Benefits")

st.sidebar.title("Settings")

south_only = st.sidebar.checkbox("Only municipalities in the South")

tax_benefit_only = st.sidebar.checkbox("Highlight municipalities with Pension Benefits")


@st.cache_resource(show_spinner=True)
def fetch_and_plot_data(south_only):
    if south_only:
        regions = south_italy
    else:
        regions = north_italy + south_italy

    gdf = DataQuery(level="municipality").filter(regions=regions)

    plotter = Plotter(gdf=gdf)
    m_highlight = plotter.explore_plot()
    fig_highlight = folium.Figure().add_child(m_highlight).render()

    m_normal = plotter.explore_plot_without_highlight()
    fig_normal = folium.Figure().add_child(m_normal).render()
    return (fig_highlight, fig_normal)


fig_highlight, fig_normal = fetch_and_plot_data(south_only=south_only)

with st.spinner("Loading map..."):
    if tax_benefit_only:
        components.html(fig_highlight, height=600)
    else:
        components.html(fig_normal, height=600)
