import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import geopandas as gpd
import folium

def simple_plot(gdf):
    
    fig = plt.figure(figsize=(18, 18))
    ax = fig.add_subplot(1, 1, 1)
    ax = gdf.plot(column='eligible_for_pension_benefit', cmap=ListedColormap(['red', 'green']), legend=True, ax=ax)

    plt.title('Southern Municipalities Eligible for Retirement Benefits')
    plt.tight_layout()
    plt.show()
    
    plt.savefig("../images/simple_plot.png")

def explore_plot(gdf):
    
    m = folium.Map(location=[42, 10], zoom_start=6, tiles='OpenStreetMap')
    gdf.explore(column='eligible_for_pension_benefit', categorical=True, cmap=ListedColormap(['red', 'green']), m=m).save("../images/explore_plot.html")