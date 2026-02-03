#!/usr/bin/env python3
"""
Discount App - A tool to find sales and deals for computer parts, consoles, and televisions.

This is the base file for the discount app that will search for deals across various retailers.
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
    
    def __init__(self):
        self.deals: List[Deal] = []
        self.retailers = [
            "Amazon",
            "Newegg",
            "Best Buy",
            "Micro Center",
            "B&H Photo",
            "Walmart",
            "Target"
        ]
    
    def search_deals(self, categories: Optional[List[ProductCategory]] = None) -> List[Deal]:
        """
        Search for deals across all retailers.
        
        Args:
            categories: List of product categories to search for. If None, search all.
        
        Returns:
            List of Deal objects found.
        """
        if categories is None:
            categories = list(ProductCategory)
        
        logger.info(f"Searching for deals in categories: {[cat.value for cat in categories]}")
        
        # This is where you would implement actual web scraping or API calls
        # For now, we'll return a placeholder
        self.deals = self._fetch_deals_from_retailers(categories)
        
        return self.deals
    
    def _fetch_deals_from_retailers(self, categories: List[ProductCategory]) -> List[Deal]:
        """
        Fetch deals from various retailers.
        
        This is a placeholder method that should be implemented with actual
        web scraping logic or API calls to retailers.
        
        Args:
            categories: List of categories to search for.
        
        Returns:
            List of Deal objects.
        """
        # Placeholder for actual implementation
        # In a real implementation, this would scrape websites or call APIs
        logger.info("Fetching deals from retailers...")
        logger.info("Note: This is a base implementation. Add web scraping or API logic here.")
        
        # Example deals to demonstrate the structure
        example_deals = [
            Deal(
                product_name="AMD Ryzen 9 5900X",
                category=ProductCategory.CPU,
                original_price=549.99,
                sale_price=399.99,
                retailer="Newegg",
                url="https://www.newegg.com/example",
                description="12-Core, 24-Thread Desktop Processor"
            ),
            Deal(
                product_name="NVIDIA RTX 4070",
                category=ProductCategory.GPU,
                original_price=599.99,
                sale_price=499.99,
                retailer="Best Buy",
                url="https://www.bestbuy.com/example",
                description="12GB GDDR6X Graphics Card"
            ),
            Deal(
                product_name="PlayStation 5",
                category=ProductCategory.CONSOLE,
                original_price=499.99,
                sale_price=449.99,
                retailer="Amazon",
                url="https://www.amazon.com/example",
                description="PS5 Console with Controller"
            ),
            Deal(
                product_name="Samsung 55\" 4K TV",
                category=ProductCategory.TELEVISION,
                original_price=799.99,
                sale_price=599.99,
                retailer="Target",
                url="https://www.target.com/example",
                description="55-inch 4K UHD Smart TV"
            ),
        ]
        
        return example_deals
    
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
