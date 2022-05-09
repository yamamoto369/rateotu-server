from rateotu.employees.selectors import (
    get_order_item_quantity_totals_per_category,
    get_order_item_quantity_totals_per_day,
    get_total_orders_count,
    get_total_orders_revenue,
    get_total_orders_quantity,
    get_total_distinct_customers,
    get_best_sellers,
)
from rateotu.utils.employees import generate_category_quantity_totals_chart_data


def generate_employee_dashboard_chart_data():
    data = {}
    data["order_item_totals"] = {
        "quantity_per_category": generate_category_quantity_totals_chart_data(
            get_order_item_quantity_totals_per_category()
        ),
        "quantity_per_day": get_order_item_quantity_totals_per_day(),
    }
    data["totals"] = {
        "orders": get_total_orders_count(),
        "revenue": get_total_orders_revenue(),
        "quantity": get_total_orders_quantity(),
        "customers": get_total_distinct_customers(),
    }
    data["tables"] = {"best_sellers": get_best_sellers()}
    return data
