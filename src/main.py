from maps.maps import Plotter
from maps.utils import DataQuery, south_italy

gdf = DataQuery(regions=south_italy).get_municipality_data()
plotter = Plotter(gdf=gdf)
plotter.save_simple_plot()
plotter.save_explore_plot()