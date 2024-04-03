import geopandas as gpd
import italy_geopop
from pydantic import BaseModel, field_validator, model_validator

north_italy = ['Emilia-Romagna',
 'Friuli-Venezia Giulia',
 'Lazio',
 'Liguria',
 'Lombardia',
 'Marche',
 'Piemonte',
 'Toscana',
 'Trentino-Alto Adige/Südtirol',
 'Umbria',
 "Valle d'Aosta/Vallée d'Aoste",
 'Veneto']

south_italy = ['Abruzzo',
 'Basilicata',
 'Calabria',
 'Campania',
 'Molise',
 'Puglia',
 'Sardegna',
 'Sicilia']


class DataQuery(BaseModel):
    level: str
    gdf: gpd.GeoDataFrame = None

    @field_validator("level")
    def check_level(cls, v):  # noqa
        if v not in ("region", "province", "municipality"):
            raise ValueError(
                'level must be one of "region", "province", or "municipality"'
            )
        return v

    @model_validator(mode="after")
    def set_geodata(self):
        geopop = italy_geopop.geopop.Geopop(data_year=2023)
        geodata = geopop.compose_df(
            level=self.level, include_geometry=True, population_limits="total"
        )
        if self.level == "municipality":
            geodata["eligible_for_pension_benefit"] = (
                geodata["population"] < 20000
            ) & (geodata["region"].isin(south_italy))
        gdf = gpd.GeoDataFrame(geodata)
        self.gdf = gdf

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
