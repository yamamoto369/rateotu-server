def generate_category_quantity_totals_chart_data(data):
    # Should be wrapped in str (but the chart lib won't accept)
    food_prc = round(100 * float(data["food"]) / float(data["food"] + data["drink"]), 2)
    drink_prc = round(
        100 * float(data["drink"]) / float(data["drink"] + data["food"]), 2
    )

    return [
        {"category": "food", "count": data["food"], "percent": food_prc},
        {"category": "drink", "count": data["drink"], "percent": drink_prc},
    ]
