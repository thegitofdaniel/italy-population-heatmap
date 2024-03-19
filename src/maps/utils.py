import geopandas as gpd
import italy_geopop
import pandas as pd
from italy_geopop.pandas_extension import pandas_activate
from pydantic import BaseModel

pandas_activate(include_geometry=True, data_year=2022)


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

italy = south_italy + north_italy


from pydantic import field_validator, model_validator


class DataQuery(BaseModel):
    level: str
    gdf: gpd.GeoDataFrame = None
    units: list[str] = None

    @field_validator("level")
    def check_level(cls, v):  # noqa
        if v not in ("region", "province", "municipality"):
            raise ValueError(
                'level must be one of "region", "province", or "municipality"'
            )
        return v

    @model_validator(mode="after")
    def set_geodata(self):
        level = self.level
        units = self.units
        geopop = italy_geopop.geopop.Geopop()

        if level == "region":
            if units is None:
                units = geopop.italy_regions.region.tolist()
            data = pd.Series(units)
            geodata = data.italy_geopop.from_region()

        elif level == "province":
            if units is None:
                units = geopop.italy_provinces.province.tolist()
            data = pd.Series(units)
            geodata = data.italy_geopop.from_province()

        else:
            if units is None:
                units = geopop.italy_municipalities.municipality.tolist()
            data = pd.Series(units)
            geodata = data.italy_geopop.from_municipality(population_limits="total")
            geodata["eligible_for_pension_benefit"] = (
                geodata["population"] < 20000
            ) & (geodata["region"].isin(south_italy))

        self.units = units
        self.gdf = gpd.GeoDataFrame(geodata)

    def filter(
        self,
        regions: list[str] = [""],
        provinces: list[str] = [""],
        municipalities: list[str] = [""],
    ):
        gdf = self.gdf.copy()
        if regions != [""]:
            gdf = gdf[gdf["region"].isin(regions)]
        if provinces != [""]:
            gdf = gdf[gdf["province"].isin(provinces)]
        if municipalities != [""]:
            gdf = gdf[gdf["municipality"].isin(municipalities)]
        return gdf

    class Config:
        arbitrary_types_allowed = True
