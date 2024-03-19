import os

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pydantic import BaseModel


class Plotter(BaseModel):
    gdf: gpd.GeoDataFrame

    class Config:
        arbitrary_types_allowed = True

    def validate_path(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def simple_plot(self):
        fig = plt.figure(figsize=(18, 18))
        ax = fig.add_subplot(1, 1, 1)
        self.gdf.plot(
            column="eligible_for_pension_benefit",
            cmap=ListedColormap(["red", "green"]),
            legend=True,
            ax=ax,
        )
        plt.title("Southern Municipalities Eligible for Retirement Benefits")
        plt.tight_layout()
        plt.show()
        return fig

    def save_simple_plot(self, path="../images/simple_plot.png"):
        self.validate_path(path)
        fig = self.simple_plot()
        fig.savefig(path)

    def explore_plot(self):
        m = folium.Map(location=[42, 10], zoom_start=6, tiles="OpenStreetMap")
        self.gdf.explore(
            column="eligible_for_pension_benefit",
            categorical=True,
            cmap=ListedColormap(["red", "green"]),
            m=m,
        )
        return m

    def explore_plot_without_highlight(self):
        m = folium.Map(location=[42, 10], zoom_start=6, tiles="OpenStreetMap")
        self.gdf.explore(m=m)
        return m

    def save_explore_plot(self, path="../images/explore_plot.html"):
        self.validate_path(path)
        m = self.explore_path()
        m.save(path)
