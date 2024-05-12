# Company without websites Scraper

## Overview

This application enables users to scrape company data from web services using the Google Maps API and subsequently manage this data within a user-friendly GUI. Users can load, filter, edit, and save company data stored in CSV format.

## Features

- Scrape company data from Google Maps API.
- Load scraped data from CSV files.
- Apply filters based on various attributes such as company name, city, business type, phone number, and contact status.
- Edit contact statuses directly in the UI.
- Save modified data back to CSV files.

## Installation

### Prerequisites

- Python 3.x
- pip
- Google Maps API key
- Internet connection to download dependencies and to perform data scraping.

### Obtaining a Google Maps API Key

To use the Google Maps API, you must have an API key. This key allows you to make requests to the API and is crucial for accessing the functionalities needed for scraping data:

1. Visit the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to "APIs & Services" > "Credentials".
4. Click on "Create Credentials" and select "API key".
5. Once you have your key, restrict its usage to prevent unauthorized use, by setting application restrictions and limiting API services that the key can access.

### Configuring the Scraper

The scraper can be customized to target specific business types and cities. For instance, you might want to scrape data for specific business types like 'Local Coffee Shops' or 'Organic Grocery Stores' across various French cities:

- `business_types`: Define the types of businesses you are interested in. This list should be customized based on your specific needs.
- `cities`: List of cities where you want to search for these businesses.

Here is an example of how you might set up these variables in your script:

```python
business_types = ['Local Coffee Shops', 'Boutique Clothing Stores', 'Artisanal Bakeries', ...]
cities = ['Paris', 'Marseille', 'Lyon', ...]
```
### Dependencies

All dependencies required for scraping and GUI operations can be installed via pip:

```bash
pip install -r requirements.txt
