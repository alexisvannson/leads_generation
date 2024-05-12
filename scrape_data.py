import csv
import requests
import time

#API_KEY = 'your GoogleMaps API Key'

french_cities = ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille', 'Rennes', 'Reims', 'Saint-Étienne', 'Toulon', 'Le Havre', 'Grenoble', 'Dijon', 'Angers', 'Nîmes', 'Villeurbanne', 'Clermont-Ferrand', 'Saint-Denis', 'La Rochelle', 'Le Mans', 'Aix-en-Provence', 'Brest', 'Tours', 'Amiens', 'Limoges', 'Annecy', 'Perpignan', 'Boulogne-Billancourt', 'Metz', 'Besançon', 'Orléans', 'Saint-Denis', 'Argenteuil', 'Rouen', 'Mulhouse', 'Montreuil', 'Caen', 'Nancy', 'Saint-Paul', 'Neuilly-sur-Seine', 'Versailles', 'Nanterre', 'Avignon', 'Vitry-sur-Seine', 'Créteil', 'Dunkerque']


business_types = ['Local Coffee Shops', 'Boutique Clothing Stores', 'Artisanal Bakeries', 'Independent Bookstores', 'Vintage Furniture Shops', 'Pet Grooming Salons', 'Organic Grocery Stores', 'Local Butchers', 'Flower Shops', 'Craft Breweries', 'Gyms and Fitness Studios', 'Family-Owned Restaurants', 'Homemade Ice Cream Parlors', 'Handmade Jewelry Stores', 'Interior Design Studios', 'Custom Tailoring Shops', 'Record Stores', 'Gift Shops', 'Nail Salons', 'Farmers\' Markets Vendors', 'Yoga Studios', 'Photography Studios', 'Tech Startups', 'Marketing Agencies', 'Legal Firms', 'Dental Clinics', 'Architectural Firms', 'Educational Institutions', 'Art Galleries', 'Music Schools']


def search_shops(query, city):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': query + ' in ' + city,
        'key': API_KEY
    }
    results = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()
        for result in data.get('results', []):
            place_details = get_place_details(result['place_id'])
            if 'website' not in place_details:
                results.append(result)

        if 'next_page_token' in data:
            next_page_token = data['next_page_token']
            time.sleep(2)  # Google API requires a short delay before requesting the next page.
            params['pagetoken'] = next_page_token
        else:
            break

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
    with open('cbd_shops_without_website.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['City', 'Business Type', 'Name', 'Address', 'Phone Number', 'Opening Hours']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for city in french_cities:
            for business_type in business_types:
                shops = search_shops(business_type, city)
                for shop in shops:
                    place_id = shop['place_id']
                    details = get_place_details(place_id)
                    writer.writerow({
                        'City': city,
                        'Business Type': business_type,
                        'Name': details.get('name', ''),
                        'Address': details.get('formatted_address', ''),
                        'Phone Number': details.get('formatted_phone_number', ''),
                        'Opening Hours': ', '.join(details.get('opening_hours', {}).get('weekday_text', [])),
                    })

if __name__ == '__main__':
    main()
