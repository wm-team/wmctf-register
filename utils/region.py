from country_list.country_list import countries_for_language

region_code = [i[0] for i in countries_for_language('zh_CN')]


def list_region(lang: str = 'en_US'):
    return countries_for_language(lang)


def get_region_name(region_code: str, lang: str = 'en_US'):
    return ','.join(i[1] for i in countries_for_language(lang) if i[0] == region_code)


def is_valid_region_code(code: str):
    return code in region_code
