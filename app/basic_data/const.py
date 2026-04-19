class const:
    sources = None
    domains = None
    excludeDomains = None
    countries = None
    
    searchin = None
    COUNTRIES = {
        "ae",
        "ar",
        "at",
        "au",
        "be",
        "bg",
        "br",
        "ca",
        "ch",
        "cn",
        "co",
        "cu",
        "cz",
        "de",
        "eg",
        "fr",
        "gb",
        "gr",
        "hk",
        "hu",
        "id",
        "ie",
        "il",
        "in",
        "it",
        "jp",
        "kr",
        "lt",
        "lv",
        "ma",
        "mx",
        "my",
        "ng",
        "nl",
        "no",
        "nz",
        "ph",
        "pl",
        "pt",
        "ro",
        "rs",
        "ru",
        "sa",
        "se",
        "sg",
        "si",
        "sk",
        "th",
        "tr",
        "tw",
        "ua",
        "us",
        "ve",
        "za",
    }
   
    language = {
        "ae": "ar",
        "ar": "es",
        "at": "de",
        "au": "en",
        "be": "nl",
        "bg": "bg",
        "br": "pt",
        "ca": "en",
        "ch": "de",
        "cn": "zh",
        "co": "es",
        "cu": "es",
        "cz": "cs",
        "de": "de",
        "eg": "ar",
        "fr": "fr",
        "gb": "en",
        "gr": "el",
        "hk": "zh",
        "hu": "hu",
        "id": "id",
        "ie": "en",
        "il": "he",
        "in": "hi",
        "it": "it",
        "jp": "ja",
        "kr": "ko",
        "lt": "lt",
        "lv": "lv",
        "ma": "ar",
        "mx": "es",
        "my": "ms",
        "ng": "en",
        "nl": "nl",
        "no": "no",
        "nz": "en",
        "ph": "en",
        "pl": "pl",
        "pt": "pt",
        "ro": "ro",
        "rs": "sr",
        "ru": "ru",
        "sa": "ar",
        "se": "sv",
        "sg": "en",
        "si": "sl",
        "sk": "sk",
        "th": "th",
        "tr": "tr",
        "tw": "zh",
        "ua": "uk",
        "us": "en",
        "ve": "es",
        "za": "zu",
    }
    
    LANGUAGES = {"ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"}

    category = {"business", "entertainment", "general", "health", "science", "sports", "technology"}
    SORT_METHOD = {"relevancy", "popularity", "publishedAt"}
    sortBY = {"publishedAt", "popularity", "relevancy"}
    pageSize = 100
    page = 1


    def set_country(country:str):
        if not country or not country.strip():
            return "en"
        if country in const.COUNTRIES:
            return const.language[country]
        else:
            return "en"
        
    def set_language(language):
        if language in const.LANGUAGES:
            const.LANGUAGES = language
        else:
            const.LANGUAGES = "en"