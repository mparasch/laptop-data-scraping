# Laptop Shopping Web Scraper

## Overview
This script scrapes product data from Microcenter's website. It retrieves product details such as SKU, description, color, processor type, RAM, graphics, price, and savings, and stores the information in a CSV file. The data is retrieved from multiple pages of the product listing and organized into a structured format using Pandas.

## Requirements
The following Python packages are required to run the script:
- `BeautifulSoup4`
- `requests`
- `pandas`
- `re`

These packages can be installed using the following command:
```bash
pip install beautifulsoup4 requests pandas
```

## Functionality

### Main Execution

The script performs the following actions:
1. **URL Construction**: It constructs a URL for the product listing page based on the page number.
2. **Page Scraping**: It sends a request to each page, retrieves the HTML, and parses it using BeautifulSoup.
3. **Data Extraction**: The `create_df` function is called for each page to extract relevant product details.
4. **CSV Export**: The final product data is stored in a CSV file (`df_final.csv`).

### Pagination
- The script automatically calculates the number of pages available based on the status section of the product page.
- It retrieves data from each page by iterating through the pages and scraping the content.

### Sample Output
The output CSV file `df_final.csv` contains the following columns:
- `sku`: The product SKU.
- `title`: The product title.
- `color`: The color of the product.
- `processor`: The processor type.
- `clock speed`: The clock speed of the processor.
- `RAM`: The type of RAM.
- `RAM_power`: The amount of RAM in GB.
- `drive`: The type of storage drive (e.g., SSD, HDD).
- `drive_size`: The size of the storage drive.
- `graphics`: The graphics card details.
- `price`: The price of the product.
- `savings`: The discount amount or savings.

## Example Usage

To run the script, simply execute it in a Python environment. The script will automatically scrape the product pages, extract the relevant details, and save them in a CSV file.

```bash
python app.py
```
