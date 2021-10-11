## IP Geolocation API

The API is available under https://ipgeoapp.herokuapp.com/api/geolocations/

auto-generated coreapi docs: https://ipgeoapp.herokuapp.com/api/docs/

List of IP addresses (you can use it as test data): https://www.dotcom-monitor.com/blog/technical-tools/network-location-ip-addresses/

To add geolocation information to database, you'd like to do POST request with IP parameter in its body.

Example POST request body:
```
{"ip": "23.81.0.59"}
```
its response:
```
{
        "id": 1,
        "location": {
            "languages": [
                {
                    "code": "en",
                    "name": "English",
                    "native": "English"
                }
            ],
            "geoname_id": 5809844,
            "capital": "Washington D.C.",
            "country_flag": "https://assets.ipstack.com/flags/us.svg",
            "country_flag_emoji": "🇺🇸",
            "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
            "calling_code": "1",
            "is_eu": false
        },
        "ip": "23.81.0.59",
        "type": "ipv4",
        "continent_code": "NA",
        "continent_name": "North America",
        "country_code": "US",
        "country_name": "United States",
        "region_code": "WA",
        "region_name": "Washington",
        "city": "Seattle",
        "zip": "98161",
        "latitude": 47.60150146484375,
        "longitude": -122.33039855957031
    },
    {
        "id": 2,
        "location": {
            "languages": [
                {
                    "code": "en",
                    "name": "English",
                    "native": "English"
                }
            ],
            "geoname_id": 5037784,
            "capital": "Washington D.C.",
            "country_flag": "https://assets.ipstack.com/flags/us.svg",
            "country_flag_emoji": "🇺🇸",
            "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
            "calling_code": "1",
            "is_eu": false
        },
        "ip": "65.49.22.66",
        "type": "ipv4",
        "continent_code": "NA",
        "continent_name": "North America",
        "country_code": "US",
        "country_name": "United States",
        "region_code": "MN",
        "region_name": "Minnesota",
        "city": "Minnetonka",
        "zip": "55364",
        "latitude": 44.93484115600586,
        "longitude": -93.66797637939453
    }
```

Existing user is **u: krystian p: password**, but feel free to create your own one.

### Requirements
* Docker
* .env file

### Installation
Clone the repo
```
git clone https://github.com/krystianjarmul/geolocation-api.git
```
go to project directory
```
cd geolocation-api
```
create .env file with required environment variables

build and run docker containers
```
docker-compose up --build
```
App is running under localhost:8000 

To run unittests:
```
docker-compose exec api sh -c "python manage.py test"
```

### UML DB Entities

![alt text](https://i.ibb.co/7SS7xdf/geolocation-this.png)

