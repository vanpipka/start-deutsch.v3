def get_exam_rules_url(category, level):
    
    key = f"{category}_{level}"
    
    if key.lower() == "A1_schreiben".lower():
        return "/nemetskiy-a1-testy/schreiben/rules"
    
    return None