def get_exam_rules_url(category, level):
    
    if not category or not level:
        return ""
    
    if category == "all":
        return f"/{level}/rules/"
    
    return f"/{level}/rules/{category}/"