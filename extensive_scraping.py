import csv
import requests
import time

API_KEY = 'AIzaSyDS__hERYERxRPLCHQ-YJMQ1z6-bSwlpic'


def search_shops(query):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': query,
        'radius': 50000,  # Adjust the radius as needed (in meters)
        'key': API_KEY
    }
    results = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()
        results.extend(data.get('results', []))

        if 'next_page_token' in data:
            next_page_token = data['next_page_token']
            # Wait for a short interval before making the next request
            time.sleep(2)  # Wait for 2 seconds
            params['pagetoken'] = next_page_token
        else:
            break  # No more pages

    return results

def get_place_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website,opening_hours',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('result', {})

def main():
    shop_types = [
        'cbd shop'
    ]

    with open('shop_data.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Shop Type', 'Name', 'Address', 'Phone Number', 'Has Website', 'Opening Hours']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for shop_type in shop_types:
            shops = search_shops(shop_type)
            for shop in shops:
                place_id = shop['place_id']
                details = get_place_details(place_id)
                has_website = 'website' in details
                writer.writerow({
                    'Shop Type': shop_type,
                    'Name': details.get('name', ''),
                    'Address': details.get('formatted_address', ''),
                    'Phone Number': details.get('formatted_phone_number', ''),
                    'Has Website': has_website,
                    'Opening Hours': ', '.join(details.get('opening_hours', {}).get('weekday_text', [])),
                })

if __name__ == '__main__':
    main()
