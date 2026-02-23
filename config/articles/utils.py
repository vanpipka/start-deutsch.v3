def get_exam_rules_url(category, level):
    
    key = f"{category}_{level}"
    
    if key.lower() == "A1_schreiben".lower():
        return "/nemetskiy-a1-testy/schreiben/rules"
    if key.lower() == "A1_lesen".lower():
        return "/nemetskiy-a1-testy/lesen/rules"
    if key.lower() == "A1_hoeren".lower() or key.lower() == "A1_hören".lower():
        return "/nemetskiy-a1-testy/hoeren/rules"
    
    return None