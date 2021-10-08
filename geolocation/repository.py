from geolocation.models import Language, Geolocation, Location


def create_geolocation(data: dict) -> Geolocation:
    location_data = data.get("location", {})
    location, _ = Location.objects.get_or_create(
        geoname_id=location_data.get("geoname_id"),
        capital=location_data.get("capital"),
        country_flag=location_data.get("country_flag"),
        country_flag_emoji=location_data.get("country_flag_emoji"),
        country_flag_emoji_unicode=location_data.get(
            "country_flag_emoji_unicode"
        ),
        calling_code=location_data.get("calling_code"),
        is_eu=location_data.get("is_eu"),
    )

    languages = [
        Language.objects.get_or_create(
            code=lang.get("code"),
            name=lang.get("name"),
            native=lang.get("native")
        )[0]
        for lang in location_data.get("languages", [])
    ]

    location.languages.set(languages)

    geolocation, _ = Geolocation.objects.get_or_create(
        ip=data.get("ip"),
        type=data.get("type"),
        continent_code=data.get("continent_code"),
        continent_name=data.get("continent_name"),
        country_code=data.get("country_code"),
        country_name=data.get("country_name"),
        region_code=data.get("region_code"),
        region_name=data.get("region_name"),
        city=data.get("city"),
        zip=data.get("zip"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        location=location
    )
    return geolocation
