def fallback_recommendations(category, data):
    budget = float(data["budget"])

    if category == "home":
        return [
            {"title": "LED Ceiling Light", "platform": "Amazon", "price": round(budget * .12, 2),
             "reason": "Budget-friendly lighting option"},
            {"title": "Compact Study/Side Table", "platform": "IKEA", "price": round(budget * .28, 2),
             "reason": "Useful furniture within the planned budget"},
            {"title": "Decorative Wall Art", "platform": "Amazon", "price": round(budget * .10, 2),
             "reason": "Adds style without using a large part of the budget"},
        ]

    if category == "party":
        return [
            {"title": "Food & Catering Package", "platform": "Swiggy / Zomato", "price": round(budget * .50, 2),
             "reason": "Largest allocation for guest food"},
            {"title": "Decoration Package", "platform": "Local Vendor / Online", "price": round(budget * .25, 2),
             "reason": "Balanced event decoration"},
            {"title": "Venue / Stay Option", "platform": "OYO / Local Venue", "price": round(budget * .20, 2),
             "reason": "Keeps venue spending controlled"},
        ]

    return [
        {"title": "Minimal Necklace Set", "platform": "Amazon", "price": round(budget * .35, 2),
         "reason": "Versatile option for the selected occasion"},
        {"title": "Matching Earrings", "platform": "Flipkart", "price": round(budget * .20, 2),
         "reason": "Complements the main jewelry piece"},
        {"title": "Bracelet / Bangle Set", "platform": "Amazon", "price": round(budget * .15, 2),
         "reason": "Optional accessory within the remaining budget"},
    ]
