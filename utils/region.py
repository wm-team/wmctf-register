from country_list.country_list import countries_for_language

region_code = [
    f"{i[0]} - {i[1]}" for i in countries_for_language('en_US')] + ["N/A"]


def get_region_name(region_code: str | None, lang: str = 'en_US'):
    return ','.join(i[1] for i in countries_for_language(lang) if i[0] == region_code) or "N/A"
