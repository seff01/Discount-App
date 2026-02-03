# Example Configuration for Discount App
# This file shows how you can customize the app for your needs

# Example: How to search for specific categories only
"""
from discount_app import DealSearcher, ProductCategory

searcher = DealSearcher()

# Search only for GPUs
gpu_deals = searcher.search_deals(categories=[ProductCategory.GPU])

# Search only for consoles and TVs
entertainment_deals = searcher.search_deals(
    categories=[ProductCategory.CONSOLE, ProductCategory.TELEVISION]
)

# Search for computer parts only
computer_parts = searcher.search_deals(
    categories=[
        ProductCategory.CPU,
        ProductCategory.GPU,
        ProductCategory.RAM,
        ProductCategory.MOTHERBOARD,
        ProductCategory.SSD
    ]
)
"""

# Example: How to filter deals
"""
from discount_app import DealSearcher, ProductCategory

searcher = DealSearcher()
searcher.search_deals()

# Find deals with at least 30% discount
hot_deals = searcher.filter_deals_by_min_discount(30.0)

# Find deals under $300
budget_deals = searcher.filter_deals_by_max_price(300.0)

# Find GPU deals only
gpu_deals = searcher.filter_deals_by_category(ProductCategory.GPU)

# Combine filters: GPUs under $500
affordable_gpus = [
    deal for deal in searcher.filter_deals_by_category(ProductCategory.GPU)
    if deal.sale_price <= 500.0
]
"""

# Example: How to implement web scraping for a retailer
"""
import requests
from bs4 import BeautifulSoup
from discount_app import Deal, ProductCategory

def scrape_newegg_gpus():
    # This is a simplified example - actual implementation would need
    # proper error handling, rate limiting, and respect for robots.txt
    
    url = "https://www.newegg.com/GPUs/SubCategory/ID-48"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    deals = []
    # Parse the HTML to extract product information
    # This is where you'd write retailer-specific parsing logic
    
    return deals
"""

# Example: Retailer-specific scraping notes
RETAILER_NOTES = {
    "Amazon": {
        "url_pattern": "https://www.amazon.com/s?k={search_term}",
        "notes": "Use Amazon Product Advertising API for better results",
        "rate_limit": "1 request per second"
    },
    "Newegg": {
        "url_pattern": "https://www.newegg.com/p/pl?d={search_term}",
        "notes": "Check for promo codes in addition to sales",
        "rate_limit": "Respect robots.txt"
    },
    "Best Buy": {
        "url_pattern": "https://www.bestbuy.com/site/searchpage.jsp?st={search_term}",
        "notes": "Has an API available for developers",
        "rate_limit": "API rate limits apply"
    },
    "Micro Center": {
        "url_pattern": "https://www.microcenter.com/search/search_results.aspx?Ntt={search_term}",
        "notes": "In-store deals may differ from online",
        "rate_limit": "Be respectful with scraping"
    }
}

# Example search terms for different categories
SEARCH_TERMS = {
    ProductCategory.CPU: ["AMD Ryzen", "Intel Core", "processor", "CPU"],
    ProductCategory.GPU: ["RTX", "AMD Radeon", "graphics card", "GPU"],
    ProductCategory.CONSOLE: ["PlayStation", "Xbox", "Nintendo Switch"],
    ProductCategory.TELEVISION: ["4K TV", "OLED TV", "Smart TV", "television"],
}
