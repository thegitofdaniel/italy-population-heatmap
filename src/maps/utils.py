import geopandas as gpd
import pandas as pd


def get_codes_from_page(page):
    array = page["municipalities"]
    codes = [a["municipality_code"] for a in array]
    return codes


def get_codes_from_provinces(provinces):
    all_codes = []
    for province in provinces:
        for page in province:
            codes = get_codes_from_page(page)
            all_codes.extend(codes)
    return all_codes


north_italy = [
    "Valle d'Aosta",
    "Piemonte",
    "Lombardia",
    "Trentino-Alto Adige",
    "Veneto",
    "Friuli-Venezia Giulia",
    "Liguria",
    "Emilia-Romagna",
    "Toscana",
    "Umbria",
    "Marche",
    "Lazio",
]

south_italy = [
    "Abruzzo",
    "Molise",
    "Campania",
    "Puglia",
    "Basilicata",
    "Calabria",
    "Sicilia",
    "Sardegna",
]


class DataQuery:
    def __init__(self):
        pass

    def get_province_codes(self, regions):
        region_data = pd.Series(regions).italy_geopop.from_region()

        codes = get_codes_from_provinces(region_data["provinces"])

        return codes

    def get_municipality_data(self, regions):
        codes = self.get_province_codes(regions)

        data = pd.Series(codes)
        geodata = data.italy_geopop.from_municipality(population_limits="total")

        geodata = geodata[
            ["municipality_code", "municipality", "geometry", "population"]
        ]
        geodata["eligible_for_pension_benefit"] = geodata["population"] < 20000

        gdf = gpd.GeoDataFrame(geodata)
        return gdf
