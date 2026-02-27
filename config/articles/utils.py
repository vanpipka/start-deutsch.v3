def get_exam_rules_url(category, level):
    
    if not category or not level:
        return ""
    
    return f"/{level}/rules/{category}/"