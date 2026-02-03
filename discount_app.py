#!/usr/bin/env python3
"""
Discount App - A tool to find sales and deals for computer parts, consoles, and televisions.

This is the base file for the discount app that will search for deals across various retailers.
"""

import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}
REQUEST_TIMEOUT = 10
MAX_RESULTS_PER_RETAILER = 5
DEFAULT_MAX_WORKERS = 6
CACHE_TTL_SECONDS = 300


class ProductCategory(Enum):
    """Enum for different product categories."""
    CPU = "CPU"
    GPU = "GPU"
    RAM = "RAM"
    MOTHERBOARD = "Motherboard"
    SSD = "SSD"
    HDD = "HDD"
    PSU = "Power Supply"
    CASE = "PC Case"
    CONSOLE = "Console"
    TELEVISION = "Television"
    MONITOR = "Monitor"


CATEGORY_SEARCH_TERMS = {
    ProductCategory.CPU: "cpu processor",
    ProductCategory.GPU: "graphics card",
    ProductCategory.RAM: "ddr5 ram",
    ProductCategory.MOTHERBOARD: "motherboard",
    ProductCategory.SSD: "nvme ssd",
    ProductCategory.HDD: "hard drive",
    ProductCategory.PSU: "power supply",
    ProductCategory.CASE: "pc case",
    ProductCategory.CONSOLE: "game console",
    ProductCategory.TELEVISION: "4k tv",
    ProductCategory.MONITOR: "gaming monitor",
}


class Deal:
    """Represents a deal or sale on a product."""
    
    def __init__(
        self,
        product_name: str,
        category: ProductCategory,
        original_price: float,
        sale_price: float,
        retailer: str,
        url: str = "",
        description: str = "",
    ):
        self.product_name = product_name
        self.category = category
        self.original_price = original_price
        self.sale_price = sale_price
        self.retailer = retailer
        self.url = url
        self.description = description
        self.discount_percentage = self._calculate_discount()
        self.timestamp = datetime.now()
    
    def _calculate_discount(self) -> float:
        """Calculate the discount percentage."""
        if self.original_price <= 0:
            return 0.0
        return round(((self.original_price - self.sale_price) / self.original_price) * 100, 2)
    
    def to_dict(self) -> Dict:
        """Convert deal to dictionary format."""
        return {
            'product_name': self.product_name,
            'category': self.category.value,
            'original_price': self.original_price,
            'sale_price': self.sale_price,
            'discount_percentage': self.discount_percentage,
            'retailer': self.retailer,
            'url': self.url,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation of the deal."""
        return (
            f"{self.product_name} ({self.category.value})\n"
            f"  Retailer: {self.retailer}\n"
            f"  Original Price: ${self.original_price:.2f}\n"
            f"  Sale Price: ${self.sale_price:.2f}\n"
            f"  Discount: {self.discount_percentage}% OFF\n"
            f"  URL: {self.url if self.url else 'N/A'}"
        )


class DealSearcher:
    """Main class for searching deals across retailers."""
    
    def __init__(
        self,
        max_results_per_retailer: int = MAX_RESULTS_PER_RETAILER,
        request_delay: float = 0.0,
        max_workers: int = DEFAULT_MAX_WORKERS,
        cache: Optional[Dict[Tuple[str, str, str], Tuple[float, List["Deal"]]]] = None,
        cache_ttl_seconds: int = CACHE_TTL_SECONDS,
    ):
        self.deals: List[Deal] = []
        self.retailer_scrapers = {
            "Best Buy": self._scrape_bestbuy,
            "Newegg": self._scrape_newegg,
        }
        self.retailers = list(self.retailer_scrapers.keys())
        self.request_delay = request_delay
        self.max_results_per_retailer = max_results_per_retailer
        self.max_workers = max_workers
        self._cache = cache if cache is not None else {}
        self.cache_ttl_seconds = cache_ttl_seconds
    
    def search_deals(
        self,
        categories: Optional[List[ProductCategory]] = None,
        search_term: Optional[str] = None,
    ) -> List[Deal]:
        """
        Search for deals across all retailers.
        
        Args:
            categories: List of product categories to search for. If None, search all.
            search_term: Optional user-provided search term to narrow results.
        
        Returns:
            List of Deal objects found.
        """
        if categories is None:
            categories = list(ProductCategory)
        
        logger.info("Searching for deals in categories: %s", [cat.value for cat in categories])
        if search_term:
            logger.info("Using search term: %s", search_term)
        
        self.deals = self._fetch_deals_from_retailers(categories, search_term)
        
        return self.deals
    
    def _fetch_deals_from_retailers(
        self,
        categories: List[ProductCategory],
        search_term: Optional[str] = None,
    ) -> List[Deal]:
        """
        Fetch deals from various retailers.
        
        This is a placeholder method that should be implemented with actual
        web scraping logic or API calls to retailers.
        
        Args:
            categories: List of categories to search for.
        
        Returns:
            List of Deal objects.
        """
        logger.info("Fetching deals from retailers...")

        deals: List[Deal] = []
        seen = set()
        normalized_term = search_term.strip() if search_term else ""
        tasks = []

        for category in categories:
            category_term = CATEGORY_SEARCH_TERMS.get(category, category.value)
            if normalized_term:
                if category_term.lower() in normalized_term.lower():
                    query = normalized_term
                else:
                    query = f"{normalized_term} {category_term}".strip()
            else:
                query = category_term
            logger.info("Searching '%s' for %s", query, category.value)
            for retailer, scraper in self.retailer_scrapers.items():
                tasks.append((retailer, scraper, query, category))

        if tasks and self.max_workers and len(tasks) > 1:
            max_workers = min(self.max_workers, len(tasks))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_task = {
                    executor.submit(
                        self._scrape_with_cache,
                        retailer,
                        scraper,
                        query,
                        category,
                    ): (retailer, query, category)
                    for retailer, scraper, query, category in tasks
                }
                for future in as_completed(future_to_task):
                    retailer, query, category = future_to_task[future]
                    try:
                        retailer_deals = future.result()
                    except Exception as exc:
                        logger.warning(
                            "Scrape failed for %s (%s): %s",
                            retailer,
                            query,
                            exc,
                        )
                        continue
                    self._merge_deals(retailer_deals, deals, seen)
        else:
            for retailer, scraper, query, category in tasks:
                retailer_deals = self._scrape_with_cache(retailer, scraper, query, category)
                self._merge_deals(retailer_deals, deals, seen)
                if self.request_delay:
                    time.sleep(self.request_delay)

        if not deals:
            logger.warning("No deals found from the live scrapers.")

        return deals

    def _merge_deals(self, retailer_deals: List[Deal], deals: List[Deal], seen: set) -> None:
        if retailer_deals:
            logger.info("Found %s deals from %s", len(retailer_deals), retailer_deals[0].retailer)
        for deal in retailer_deals:
            key = (deal.retailer, deal.product_name.lower())
            if key in seen:
                continue
            deals.append(deal)
            seen.add(key)

    def _cache_key(self, retailer: str, query: str, category: ProductCategory) -> Tuple[str, str, str]:
        return (retailer, query.strip().lower(), category.value)

    def _cache_get(self, key: Tuple[str, str, str]) -> Optional[List["Deal"]]:
        cached = self._cache.get(key)
        if not cached:
            return None
        timestamp, deals = cached
        if time.time() - timestamp > self.cache_ttl_seconds:
            self._cache.pop(key, None)
            return None
        return deals

    def _cache_set(self, key: Tuple[str, str, str], deals: List["Deal"]) -> None:
        self._cache[key] = (time.time(), deals)

    def _scrape_with_cache(
        self,
        retailer: str,
        scraper,
        query: str,
        category: ProductCategory,
    ) -> List[Deal]:
        key = self._cache_key(retailer, query, category)
        cached = self._cache_get(key)
        if cached is not None:
            logger.info("Cache hit for %s (%s)", retailer, query)
            return cached
        deals = scraper(query, category, self.max_results_per_retailer)
        self._cache_set(key, deals)
        return deals

    @staticmethod
    def _parse_price(text: str) -> Optional[float]:
        if not text:
            return None
        match = re.search(r"([0-9]+(?:,[0-9]{3})*(?:\.\d{2})?)", text)
        if not match:
            return None
        return float(match.group(1).replace(",", ""))

    def _scrape_bestbuy(
        self,
        search_term: str,
        category: ProductCategory,
        limit: int,
    ) -> List[Deal]:
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={quote_plus(search_term)}"
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.warning("Best Buy request failed for '%s': %s", search_term, exc)
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("li.sku-item")
        deals: List[Deal] = []

        for item in items:
            title_tag = item.select_one("h4.sku-title a")
            price_tag = item.select_one("div.priceView-customer-price span")

            if not title_tag or not price_tag:
                continue

            sale_price = self._parse_price(price_tag.get_text(strip=True))
            if sale_price is None:
                continue

            original_price = sale_price
            prev_price_tag = item.select_one("div.priceView-previous-price span")
            prev_price = self._parse_price(prev_price_tag.get_text(strip=True)) if prev_price_tag else None
            if prev_price and prev_price > sale_price:
                original_price = prev_price

            product_name = title_tag.get_text(strip=True)
            product_url = title_tag.get("href", "")
            if product_url.startswith("/"):
                product_url = f"https://www.bestbuy.com{product_url}"

            description_tag = item.select_one("div.sku-description")
            description = description_tag.get_text(" ", strip=True) if description_tag else ""

            deals.append(
                Deal(
                    product_name=product_name,
                    category=category,
                    original_price=original_price,
                    sale_price=sale_price,
                    retailer="Best Buy",
                    url=product_url,
                    description=description,
                )
            )

            if len(deals) >= limit:
                break

        return deals

    def _scrape_newegg(
        self,
        search_term: str,
        category: ProductCategory,
        limit: int,
    ) -> List[Deal]:
        url = f"https://www.newegg.com/p/pl?d={quote_plus(search_term)}"
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.warning("Newegg request failed for '%s': %s", search_term, exc)
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.item-cell")
        deals: List[Deal] = []

        for item in items:
            title_tag = item.select_one("a.item-title")
            price_tag = item.select_one("li.price-current")
            if not title_tag or not price_tag:
                continue

            price_text = price_tag.get_text(" ", strip=True)
            if "see price in cart" in price_text.lower():
                continue

            sale_price = self._parse_price(price_text)
            if sale_price is None:
                continue

            original_price = sale_price
            was_tag = item.select_one("li.price-was")
            was_price = self._parse_price(was_tag.get_text(" ", strip=True)) if was_tag else None
            if was_price and was_price > sale_price:
                original_price = was_price

            product_name = title_tag.get_text(strip=True)
            product_url = title_tag.get("href", "")

            deals.append(
                Deal(
                    product_name=product_name,
                    category=category,
                    original_price=original_price,
                    sale_price=sale_price,
                    retailer="Newegg",
                    url=product_url,
                    description="",
                )
            )

            if len(deals) >= limit:
                break

        return deals
    
    def filter_deals_by_category(self, category: ProductCategory) -> List[Deal]:
        """Filter deals by a specific category."""
        return [deal for deal in self.deals if deal.category == category]
    
    def filter_deals_by_min_discount(self, min_discount: float) -> List[Deal]:
        """Filter deals by minimum discount percentage."""
        return [deal for deal in self.deals if deal.discount_percentage >= min_discount]
    
    def filter_deals_by_max_price(self, max_price: float) -> List[Deal]:
        """Filter deals by maximum sale price."""
        return [deal for deal in self.deals if deal.sale_price <= max_price]
    
    def sort_deals_by_discount(self, reverse: bool = True) -> List[Deal]:
        """Sort deals by discount percentage."""
        return sorted(self.deals, key=lambda d: d.discount_percentage, reverse=reverse)
    
    def sort_deals_by_price(self, reverse: bool = False) -> List[Deal]:
        """Sort deals by sale price."""
        return sorted(self.deals, key=lambda d: d.sale_price, reverse=reverse)
    
    def export_deals_to_json(self, filename: str = "deals.json") -> None:
        """Export deals to a JSON file."""
        deals_data = [deal.to_dict() for deal in self.deals]
        with open(filename, 'w') as f:
            json.dump(deals_data, f, indent=2)
        logger.info(f"Exported {len(self.deals)} deals to {filename}")
    
    def print_deals(self) -> None:
        """Print all deals to console."""
        if not self.deals:
            logger.info("No deals found.")
            return
        
        print("\n" + "=" * 80)
        print(f"Found {len(self.deals)} Deals:")
        print("=" * 80 + "\n")
        
        for i, deal in enumerate(self.deals, 1):
            print(f"Deal #{i}:")
            print(deal)
            print("-" * 80)


def main():
    """Main function to run the discount app."""
    print("=" * 80)
    print("DISCOUNT APP - Find the Best Deals on Tech Products")
    print("=" * 80)
    print()
    
    # Initialize the deal searcher
    searcher = DealSearcher()
    
    # Search for deals in all categories
    print("Searching for deals...")
    deals = searcher.search_deals()
    
    # Display all deals
    searcher.print_deals()
    
    # Example: Filter by category
    print("\n\n" + "=" * 80)
    print("COMPUTER PARTS (CPU & GPU) DEALS:")
    print("=" * 80 + "\n")
    
    cpu_deals = searcher.filter_deals_by_category(ProductCategory.CPU)
    gpu_deals = searcher.filter_deals_by_category(ProductCategory.GPU)
    
    for deal in cpu_deals + gpu_deals:
        print(deal)
        print("-" * 80)
    
    # Example: Filter by minimum discount
    print("\n\n" + "=" * 80)
    print("DEALS WITH 20% OR MORE OFF:")
    print("=" * 80 + "\n")
    
    high_discount_deals = searcher.filter_deals_by_min_discount(20.0)
    for deal in high_discount_deals:
        print(deal)
        print("-" * 80)
    
    # Export to JSON
    searcher.export_deals_to_json("deals.json")
    print("\nDeals exported to deals.json")


if __name__ == "__main__":
    main()
