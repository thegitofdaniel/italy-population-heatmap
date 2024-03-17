import os

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from italy_geopop.pandas_extension import pandas_activate
from matplotlib.colors import ListedColormap
from pydantic import BaseModel

pandas_activate(include_geometry=True, data_year=2022)


class Plotter(BaseModel):
    gdf: gpd.GeoDataFrame

    class Config:
        arbitrary_types_allowed = True

    def validate_path(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_simple_plot(self, path="../images/simple_plot.png"):
        self.validate_path(path)

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

        fig.savefig(path)
        return fig

    def save_explore_plot(self, path="../images/explore_plot.html"):
        self.validate_path(path)

        m = folium.Map(location=[42, 10], zoom_start=6, tiles="OpenStreetMap")
        self.gdf.explore(
            column="eligible_for_pension_benefit",
            categorical=True,
            cmap=ListedColormap(["red", "green"]),
            m=m,
        )
        m.save(path)
        return m
