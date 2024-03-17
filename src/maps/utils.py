def flatten_iter(nested_list):
    flat_list = []
    for item in nested_list:
        if hasattr(item, '__iter__') and not isinstance(item, str):
            flat_list.extend([i for i in item])
        else:
            flat_list.append(item)
    return flat_list

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
    "Lazio"
]

south_italy = [
    "Abruzzo",
    "Molise",
    "Campania",
    "Puglia",
    "Basilicata",
    "Calabria",
    "Sicilia",
    "Sardegna"
]