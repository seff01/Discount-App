#!/usr/bin/env python3
"""
Simple Flask web app for the Discount App.
"""

from typing import Optional

from flask import Flask, render_template_string, request

from discount_app import DealSearcher, ProductCategory

app = Flask(__name__)

DEFAULT_CATEGORY_SELECTION = [
    ProductCategory.CPU.name,
    ProductCategory.GPU.name,
    ProductCategory.CONSOLE.name,
    ProductCategory.TELEVISION.name,
]

INDEX_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Discount App</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; color: #1f2933; }
      h1 { margin-bottom: 0.25rem; }
      p { margin-top: 0; color: #52606d; }
      form { margin-top: 1.5rem; padding: 1rem; border: 1px solid #d9e2ec; border-radius: 8px; }
      fieldset { border: none; margin: 0; padding: 0; }
      legend { font-weight: 600; margin-bottom: 0.5rem; }
      .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.35rem; }
      .filters { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem; }
      label { display: block; font-size: 0.95rem; }
      input[type="number"] { padding: 0.35rem; width: 8rem; }
      input[type="text"] { padding: 0.35rem; width: 18rem; }
      select { padding: 0.35rem; }
      button { margin-top: 1rem; padding: 0.5rem 1rem; background: #2563eb; color: white; border: none; border-radius: 6px; }
      table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
      th, td { border: 1px solid #e4e7eb; padding: 0.5rem; text-align: left; vertical-align: top; }
      th { background: #f5f7fa; }
      .error { margin-top: 1rem; padding: 0.75rem; background: #ffe8e8; border: 1px solid #f5b5b5; color: #7b241c; }
      .muted { color: #7b8794; }
    </style>
  </head>
  <body>
    <h1>Discount App</h1>
    <p>Search live listings from Best Buy and Newegg. Results depend on retailer availability.</p>

    <form method="post">
      <fieldset>
        <legend>Categories</legend>
        <div class="grid">
          {% for cat in categories %}
            <label>
              <input type="checkbox" name="categories" value="{{ cat.name }}"
                {% if cat.name in selected_categories %}checked{% endif %} />
              {{ cat.value }}
            </label>
          {% endfor %}
        </div>
      </fieldset>

      <div class="filters">
        <label>
          Search term
          <input type="text" name="query" placeholder="e.g. RTX 4070" value="{{ query }}" />
        </label>
        <label>
          Min discount %
          <input type="number" name="min_discount" min="0" step="1" value="{{ min_discount }}" />
        </label>
        <label>
          Max price
          <input type="number" name="max_price" min="0" step="1" value="{{ max_price }}" />
        </label>
        <label>
          Sort by
          <select name="sort_by">
            <option value="discount" {% if sort_by == "discount" %}selected{% endif %}>
              Discount
            </option>
            <option value="price" {% if sort_by == "price" %}selected{% endif %}>
              Price
            </option>
          </select>
        </label>
      </div>

      <button type="submit">Search deals</button>
    </form>

    {% if error %}
      <div class="error">Error: {{ error }}</div>
    {% endif %}

    {% if deals %}
      <h2>Found {{ deals|length }} deals</h2>
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Retailer</th>
            <th>Sale price</th>
            <th>Original price</th>
            <th>Discount</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {% for deal in deals %}
            <tr>
              <td>
                <strong>{{ deal.product_name }}</strong><br />
                <span class="muted">{{ deal.description }}</span>
              </td>
              <td>{{ deal.category.value }}</td>
              <td>{{ deal.retailer }}</td>
              <td>${{ "%.2f"|format(deal.sale_price) }}</td>
              <td>${{ "%.2f"|format(deal.original_price) }}</td>
              <td>{{ "%.2f"|format(deal.discount_percentage) }}%</td>
              <td>
                {% if deal.url %}
                  <a href="{{ deal.url }}" target="_blank" rel="noopener">Open</a>
                {% else %}
                  <span class="muted">N/A</span>
                {% endif %}
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% elif searched %}
      <p class="muted">No deals found. Try different categories or remove filters.</p>
    {% endif %}
  </body>
</html>
"""


def _parse_float(value: Optional[str]) -> Optional[float]:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    selected_categories = list(DEFAULT_CATEGORY_SELECTION)
    query = ""
    min_discount = ""
    max_price = ""
    sort_by = "discount"
    deals = []
    searched = False
    error = None

    if request.method == "POST":
        searched = True
        selected_categories = request.form.getlist("categories") or list(DEFAULT_CATEGORY_SELECTION)
        query = request.form.get("query", "").strip()
        min_discount = request.form.get("min_discount", "")
        max_price = request.form.get("max_price", "")
        sort_by = request.form.get("sort_by", "discount")

        try:
            categories = [ProductCategory[name] for name in selected_categories]
            searcher = DealSearcher()
            deals = searcher.search_deals(categories=categories, search_term=query or None)

            min_discount_value = _parse_float(min_discount)
            if min_discount_value is not None:
                deals = [deal for deal in deals if deal.discount_percentage >= min_discount_value]

            max_price_value = _parse_float(max_price)
            if max_price_value is not None:
                deals = [deal for deal in deals if deal.sale_price <= max_price_value]

            if sort_by == "price":
                deals = sorted(deals, key=lambda deal: deal.sale_price)
            else:
                deals = sorted(deals, key=lambda deal: deal.discount_percentage, reverse=True)
        except Exception as exc:
            error = str(exc)

    return render_template_string(
        INDEX_TEMPLATE,
        categories=list(ProductCategory),
        selected_categories=selected_categories,
        query=query,
        min_discount=min_discount,
        max_price=max_price,
        sort_by=sort_by,
        deals=deals,
        searched=searched,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
