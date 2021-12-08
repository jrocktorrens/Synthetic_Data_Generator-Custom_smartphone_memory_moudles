import configuration.location_configurations as loc_conf
import requests
from requests.structures import CaseInsensitiveDict


class HomeLocation:
    def __init__(self, coordinates: [str, None]):
        self.coordinates = coordinates
        if coordinates:
            self.data = {}
            self.extract_raw_data()
        else:
            self.data = None

    def extract_raw_data(self):
        coordinates_for_url = self.coordinates.replace(" ", "")
        coordinates_for_url = coordinates_for_url.split(',')
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={coordinates_for_url[0]}&" \
              f"lon={coordinates_for_url[1]}&format=json&apiKey={loc_conf.API_KEY}"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        resp = requests.get(url, headers=headers, verify=False).json()['results'][0]
        for d in loc_conf.DETAILS_TO_KEEP_HOME_LOCATION:
            if d not in resp.keys():
                self.data[d] = None
            else:
                self.data[d] = resp[d]

    def __str__(self):
        return str(self.data)



class Place:
    def __init__(self, dict_data):
        self.data = dict_data

    def __str__(self):
        return str(self.data['name'])



class Places:
    def __init__(self, base_coordinates: [str, None]):
        self.base_coordinates = base_coordinates
        self.places = {}
        self.get_places()

    def get_places(self):
        for t in loc_conf.PLACE_TYPES:
            self.places[t] = Places.get_all_places_by_base_coordinates_and_type(self.base_coordinates, t)

    def __str__(self):
        return str(self.places)

    @staticmethod
    def get_all_places_by_base_coordinates_and_type(base_coordinates, type):
        print(type)
        obj_place = []
        url = Places.get_url_for_request(base_coordinates, type)
        print(url)
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        resp = requests.get(url, headers=headers, verify=False).json()['features']
        for p in resp:
            properties = p["properties"]
            current_place = {}

            for d in loc_conf.DETAILS_TO_KEEP_PLACE:
                if d not in properties.keys():
                    current_place[d] = None
                else:
                    current_place[d] = properties[d]
            obj_place.append(str(Place(current_place)))
        return obj_place


    @staticmethod
    def get_url_for_request(base_coordinates, type):
        coordinates_for_url = base_coordinates.replace(" ", "")
        coordinates_for_url = coordinates_for_url.split(',')
        string_place_type = type.lower()
        string_place_type = string_place_type.split(' / ')
        string_place_type[1] = string_place_type[1].replace(" ", "_")
        string_place_type = '.'.join(string_place_type)
        url = loc_conf.MOST_BASIC_URL + string_place_type + '&' + f'filter=circle:{coordinates_for_url[1]},{coordinates_for_url[0]},' \
                                                                            f'{loc_conf.RADIUS}&bias=proximity:{coordinates_for_url[1]},{coordinates_for_url[0]}&apiKey={loc_conf.API_KEY}'
        return url


if __name__ == "__main__":
    p = Places('32.162572, 34.852054')
    for t in loc_conf.PLACE_TYPES:
        print(f'*** {t} ***')
        print(*p.places[t], sep='\n')





