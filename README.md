# Discount-App

A Python application to find the best sales and deals for computer parts (CPU, GPU, etc.), gaming consoles, and televisions.

## Features

- **Product Categories**: Search for deals across multiple categories including:
  - Computer Parts: CPU, GPU, RAM, Motherboard, SSD, HDD, PSU, PC Case, Monitor
  - Gaming Consoles: PlayStation, Xbox, Nintendo Switch, etc.
  - Televisions: Smart TVs, 4K TVs, OLED, etc.

- **Multiple Retailers**: Search across major retailers including:
  - Amazon
  - Newegg
  - Best Buy
  - Micro Center
  - B&H Photo
  - Walmart
  - Target

- **Deal Filtering**: Filter deals by:
  - Product category
  - Minimum discount percentage
  - Maximum price
  - Retailer

- **Deal Sorting**: Sort deals by:
  - Discount percentage (highest to lowest)
  - Sale price (lowest to highest)

- **Export Functionality**: Export found deals to JSON format for later analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/seff01/Discount-App.git
cd Discount-App
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies (when ready for web scraping):
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the app to search for deals:

```bash
python discount_app.py
```

This will:
1. Search for deals across all product categories
2. Display all found deals
3. Show filtered results (CPU/GPU deals, high-discount deals)
4. Export results to `deals.json`

### Programmatic Usage

You can also use the app as a module in your own Python scripts:

```python
from discount_app import DealSearcher, ProductCategory

# Initialize the searcher
searcher = DealSearcher()

# Search for deals
deals = searcher.search_deals()

# Filter by category
gpu_deals = searcher.filter_deals_by_category(ProductCategory.GPU)

# Filter by minimum discount
hot_deals = searcher.filter_deals_by_min_discount(30.0)

# Filter by max price
budget_deals = searcher.filter_deals_by_max_price(500.0)

# Sort by discount percentage
top_deals = searcher.sort_deals_by_discount()

# Export to JSON
searcher.export_deals_to_json("my_deals.json")
```

## Project Structure

```
Discount-App/
├── discount_app.py      # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Next Steps

This is a base implementation that provides the structure for the discount app. To make it fully functional, you'll need to:

1. **Implement Web Scraping**: Add actual web scraping logic in the `_fetch_deals_from_retailers()` method using libraries like:
   - `beautifulsoup4` for parsing HTML
   - `requests` for HTTP requests
   - `selenium` for dynamic content

2. **Add API Integration**: Some retailers offer APIs that can be used to fetch deals programmatically

3. **Add Price Tracking**: Store historical price data to identify the best deals

4. **Add Notifications**: Implement email or push notifications when good deals are found

5. **Add Database**: Store deals in a database for historical analysis

6. **Add Web Interface**: Create a web UI using Flask or Django for easier interaction

## Contributing

Feel free to contribute to this project by:
- Adding support for more retailers
- Implementing web scraping for specific retailers
- Adding new product categories
- Improving filtering and sorting options
- Adding tests

## License

This project is open source and available for personal use.