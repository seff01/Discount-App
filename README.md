# Discount-App

A Python application to find the best sales and deals for computer parts (CPU, GPU, etc.), gaming consoles, and televisions.

## Quick Start

Want to get started right away? Here's the fastest method:

1. **Download**: Click the green **"Code"** button → **"Download ZIP"** → Extract the files
2. **Run**: Open a terminal in the extracted folder and run:
   ```bash
   python discount_app.py
   ```
3. **Done!** The app will display example deals and create a `deals.json` file

_No installation required! Python is the only prerequisite._

**Need detailed download instructions?** See [DOWNLOAD.md](DOWNLOAD.md) for step-by-step guides for all download methods.

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

## How to Download

You can download this project in several ways:

### Option 1: Download as ZIP (Easiest - No Git Required)

1. Go to the [Discount-App repository](https://github.com/seff01/Discount-App) on GitHub
2. Click the green **"Code"** button near the top right
3. Click **"Download ZIP"**
4. Extract the ZIP file to your desired location
5. Open a terminal/command prompt and navigate to the extracted folder:
   ```bash
   cd path/to/Discount-App
   ```

### Option 2: Clone with Git (Recommended for Developers)

If you have Git installed, clone the repository:

```bash
git clone https://github.com/seff01/Discount-App.git
cd Discount-App
```

### Option 3: Use GitHub Desktop

1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Go to **File** → **Clone Repository**
3. Enter the URL: `https://github.com/seff01/Discount-App`
4. Choose where to save it on your computer
5. Click **Clone**

### Option 4: Download Individual Files

If you only need specific files:
1. Navigate to the file on [GitHub](https://github.com/seff01/Discount-App)
2. Click on the file name (e.g., `discount_app.py`)
3. Click the **"Raw"** button
4. Right-click and select **"Save as..."** to download

## Installation

After downloading the files using any method above:

1. (Optional but recommended) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies (currently minimal - only needed for future web scraping):
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
├── examples.py          # Usage examples and configuration templates
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── DOWNLOAD.md         # Detailed download instructions
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