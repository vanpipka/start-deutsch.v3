from ..models import Exam, TestCategory, TestsCountByLevelTypePart
from django.db.models import Count, Q
         
    
def get_rules():
    return [
        {
            "title": "Правила экзамена Goethe Start Deutsch A1",
            "url": "a1/rules/",
            "description": "Полные правила проведения экзамена Goethe Start Deutsch A1. Что нужно знать и как подготовиться к экзамену A1."
        },
        {
            "title": "Правила экзамена Goethe Start Deutsch A2",
            "url": "a2/rules/",
            "description": "Полные правила проведения экзамена Goethe Start Deutsch A2. Что нужно знать и как подготовиться к экзамену A2."
        },
        {
            "title": "Правила экзамена Goethe Start Deutsch B1",
            "url": "b1/rules/",
            "description": "Полные правила проведения экзамена Goethe Start Deutsch B1. Что нужно знать и как подготовиться к экзамену B1."
        },
        {
            "title": "Правила экзамена Goethe Start Deutsch B2",
            "url": "b2/rules/",
            "description": "Полные правила проведения экзамена Goethe Start Deutsch B2. Что нужно знать и как подготовиться к экзамену B2."
        }
    ]    
    ff = [
        {
            "title": "Правила письма A1 (Schreiben)",
            "url": "nemetskiy-a1-testy/schreiben/rules",
            "description": "Правила проведения письменной части экзамена Goethe Start Deutsch A1 (Schreiben)."
        },
        {
            "title": "Правила читения A1 (Lesen)",
            "url": "nemetskiy-a1-testy/lesen/rules",
            "description": "Правила проведения чтения экзамена Goethe Start Deutsch A1 (Lesen)." 
        },
        {
            "title": "Правила аудирования A1 (Hören)",
            "url": "nemetskiy-a1-testy/hoeren/rules",
            "description": "Правила проведения аудирования экзамена Goethe Start Deutsch A1 (Hören)."
        },
        {
            "title": "Правила письма A2 (Schreiben)",
            "url": "nemetskiy-a2-testy/schreiben/rules",
            "description": "Правила проведения письменной части экзамена Goethe Start Deutsch A2 (Schreiben)."
        },
        {
            "title": "Правила читения A2 (Lesen)",
            "url": "nemetskiy-a2-testy/lesen/rules",
            "description": "Правила проведения чтения экзамена Goethe Start Deutsch A2 (Lesen)." 
        },
        {
            "title": "Правила аудирования A2 (Hören)",
            "url": "nemetskiy-a2-testy/hoeren/rules",
            "description": "Правила проведения аудирования экзамена Goethe Start Deutsch A2 (Hören)."
        }
    ]


def get_test_groups():

    return [
        {
            "name": "A1",
            "url": "a1/",
            "count": Exam.objects.filter(level__slug="a1").count(),
            "num_exams": 22,
            "description": "Тесты для уровня A1 — начальный уровень владения немецким языком.",
            "description_full": "Они предназначены для тех, кто только начинает изучать язык и имеет базовые знания. На этом уровне проверяются навыки понимания и использования простых фраз и выражений, связанных с повседневными ситуациями, такими как представление себя, общение о семье, работе, покупках и т.д. Тесты A1 включают задания на чтение, аудирование, письмо и говорение, которые помогают оценить базовый уровень владения немецким языком."
        },
        {
            "name": "A2",
            "url": "a2/",
            "count": Exam.objects.filter(level__slug="a2").count(),
            "num_exams": 18,
            "description": "Тесты для уровня A2 — элементарный уровень владения немецким языком.",
            "description_full": "Они предназначены для тех, кто уже имеет базовые знания и может общаться в простых ситуациях. На этом уровне проверяются навыки понимания и использования более сложных фраз и выражений, связанных с повседневными ситуациями, такими как путешествия, работа, учеба и т.д. Тесты A2 включают задания на чтение, аудирование, письмо и говорение, которые помогают оценить уровень владения немецким языком на уровне A2."
        },
        {
            "name": "B1",
            "url": "b1/",
            "count": Exam.objects.filter(level__slug="b1").count(),
            "num_exams": 15,
            "description": "Тесты для уровня B1 — средний уровень владения немецким языком.",
            "description_full": "Они предназначены для тех, кто уже может общаться в различных ситуациях и имеет более широкий словарный запас. На этом уровне проверяются навыки понимания и использования сложных фраз и выражений, связанных с различными темами, такими как культура, общество, работа и т.д. Тесты B1 включают задания на чтение, аудирование, письмо и говорение, которые помогают оценить уровень владения немецким языком на уровне B1."
        },
        {
            "name": "B2",
            "url": "b2/",
            "count": Exam.objects.filter(level__slug="b2").count(),
            "num_exams": 10,
            "description": "Тесты для уровня B2 — продвинутый уровень владения немецким языком.",
            "description_full": "Они предназначены для тех, кто уже может общаться свободно и уверенно в различных ситуациях. На этом уровне проверяются навыки понимания и использования сложных фраз и выражений, связанных с различными темами, такими как политика, экономика, культура и т.д. Тесты B2 включают задания на чтение, аудирование, письмо и говорение, которые помогают оценить уровень владения немецким языком на уровне B2."
        }
    ]
    
    
def get_context_for_rule_page(type=None, level=None):
    
    if type is None or level is None:
        return {}
    
    level = level.upper()
    type = type.upper()
    
    if level == "A1":
        if type == "ALL":
            return {
                "level": "a1",
                "type": "all",
                "url": "a1/rules/all/",
                "template": "tests/a1/nemetskiy_a1_main_rules.html",
                "title": "Правила экзамена Goethe Start Deutsch A1 | Start Deutsch",
                "seo_title": "Правила экзамена Goethe Start Deutsch A1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Полные правила проведения экзамена Goethe Start Deutsch A1. Что нужно знать и как подготовиться к экзамену A1."
            }
        
        elif type == "SCHREIBEN":
            return {
                "level": "a1",
                "type": "schreiben",
                "url": "a1/rules/Schreiben/",
                "template": "tests/a1/nemetskiy_a1_pismo_rules.html",
                "title": "Правила письма A1 (Schreiben) — экзамен Start Deutsch A1 | Start Deutsch",
                "seo_title": "Правила письма A1 (Schreiben) — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно написать письмо на экзамене Start Deutsch A1? Полные правила Schreiben, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "LESEN":
            return {
                "level": "a1",
                "type": "lesen",
                "url": "a1/rules/Lesen/",
                "template": "tests/a1/nemetskiy_a1_chtenie_rules.html",
                "title": "Правила чтения A1 (Lesen) — экзамен Start Deutsch A1 | Start Deutsch",
                "seo_title": "Правила чтения A1 (Lesen) — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно прочитать текст на экзамене Start Deutsch A1? Полные правила Lesen, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "HÖREN" or type == "HOEREN":
            return {
                "level": "a1",
                "type": "hoeren",
                "url": "a1/rules/Hoeren/",
                "template": "tests/a1/nemetskiy_a1_audirovanie_rules.html",
                "title": "Правила аудирования A1 (Hören) — экзамен Start Deutsch A1 | Start Deutsch",
                "seo_title": "Правила аудирования A1 (Hören) — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно выполнить аудирование на экзамене Start Deutsch A1? Полные правила Hören, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#SPRECHEN":
            return {
                "level": "a1",
                "type": "sprechen",
                "url": "a1/rules/Sprechen/",
                "template": "tests/a1/nemetskiy_a1_govorit_rules.html",
                "title": "Правила говорения A1 (Sprechen) — экзамен Start Deutsch A1 | Start Deutsch",
                "seo_title": "Правила говорения A1 (Sprechen) — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно говорить на экзамене Start Deutsch A1? Полные правила Sprechen, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
    elif level == "A2":
        if type == "ALL":
            return {
                "level": "a2",
                "type": "all",
                "url": "a2/rules/all/",
                "template": "tests/a2/nemetskiy_a2_main_rules.html",
                "title": "Правила экзамена Goethe Start Deutsch A2 | Start Deutsch",
                "seo_title": "Правила экзамена Goethe Start Deutsch A2 | Start Deutsch (Примеры и советы)",
                "seo_description": "Полные правила проведения экзамена Goethe Start Deutsch A2. Что нужно знать и как подготовиться к экзамену A2."
            }
        elif type == "#SCHREIBEN":
            return {
                "level": "a2",
                "type": "schreiben",
                "url": "a2/rules/Schreiben/",
                "template": "tests/a2/nemetskiy_a2_pismo_rules.html",
                "title": "Правила письма A2 (Schreiben) — экзамен Start Deutsch A2 | Start Deutsch",
                "seo_title": "Правила письма A2 (Schreiben) — экзамен Start Deutsch A2 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно написать письмо на экзамене Start Deutsch A2? Полные правила Schreiben, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#LESEN":
            return {
                "level": "a2",
                "type": "lesen",
                "url": "a2/rules/Lesen/",
                "template": "tests/a2/nemetskiy_a2_chtenie_rules.html",
                "title": "Правила читения A2 (Lesen) — экзамен Start Deutsch A2 | Start Deutsch",
                "seo_title": "Правила читения A2 (Lesen) — экзамен Start Deutsch A2 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно прочитать текст на экзамене Start Deutsch A2? Полные правила Lesen, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#HÖREN" or type == "#HOEREN":
            return {
                "level": "a2",
                "type": "hoeren",
                "url": "a2/rules/Hoeren/",
                "template": "tests/a2/nemetskiy_a2_audirovanie_rules.html",
                "title": "Правила аудирования A2 (Hören) — экзамен Start Deutsch A2 | Start Deutsch",
                "seo_title": "Правила аудирования A2 (Hören) — экзамен Start Deutsch A2 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно выполнить аудирование на экзамене Start Deutsch A2? Полные правила Hören, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#SPRECHEN":
            return {
                "level": "a2",
                "type": "sprechen",
                "url": "a2/rules/Sprechen/",
                "template": "tests/a2/nemetskiy_a2_govorit_rules.html",
                "title": "Правила говорения A2 (Sprechen) — экзамен Start Deutsch A2 | Start Deutsch",
                "seo_title": "Правила говорения A2 (Sprechen) — экзамен Start Deutsch A2 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно говорить на экзамене Start Deutsch A2? Полные правила Sprechen, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
    elif level == "B1":
        if type == "ALL":
            return {
                "level": "b1",
                "type": "all",
                "url": "b1/rules/all/",
                "template": "tests/b1/nemetskiy_b1_main_rules.html",
                "title": "Правила экзамена Goethe Start Deutsch B1 | Start Deutsch",
                "seo_title": "Правила экзамена Goethe Start Deutsch B1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Полные правила проведения экзамена Goethe Start Deutsch B1. Что нужно знать и как подготовиться к экзамену B1."
            }
        elif type == "#SCHREIBEN":
            return {
                "level": "b1",
                "type": "schreiben",
                "url": "b1/rules/Schreiben/",
                "template": "tests/b1/nemetskiy_b1_pismo_rules.html",
                "title": "Правила письма B1 (Schreiben) — экзамен Start Deutsch B1 | Start Deutsch",
                "seo_title": "Правила письма B1 (Schreiben) — экзамен Start Deutsch B1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно написать письмо на экзамене Start Deutsch B1? Полные правила Schreiben, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#LESEN":
            return {
                "level": "b1",
                "type": "lesen",
                "url": "b1/rules/Lesen/",
                "template": "tests/b1/nemetskiy_b1_chtenie_rules.html",
                "title": "Правила читения B1 (Lesen) — экзамен Start Deutsch B1 | Start Deutsch",
                "seo_title": "Правила читения B1 (Lesen) — экзамен Start Deutsch B1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно прочитать текст на экзамене Start Deutsch B1? Полные правила Lesen, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#HÖREN" or type == "#HOEREN":
            return {
                "level": "b1",
                "type": "hoeren",
                "url": "b1/rules/Hoeren/",
                "template": "tests/b1/nemetskiy_b1_audirovanie_rules.html",
                "title": "Правила аудирования B1 (Hören) — экзамен Start Deutsch B1 | Start Deutsch",
                "seo_title": "Правила аудирования B1 (Hören) — экзамен Start Deutsch B1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно выполнить аудирование на экзамене Start Deutsch B1? Полные правила Hören, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
        elif type == "#SPRECHEN":
            return {
                "level": "b1",
                "type": "sprechen",
                "url": "b1/rules/Sprechen/",
                "template": "tests/b1/nemetskiy_b1_govorit_rules.html",
                "title": "Правила говорения B1 (Sprechen) — экзамен Start Deutsch B1 | Start Deutsch",
                "seo_title": "Правила говорения B1 (Sprechen) — экзамен Start Deutsch B1 | Start Deutsch (Примеры и советы)",
                "seo_description": "Как правильно говорить на экзамене Start Deutsch B1? Полные правила Sprechen, структура ответа, примеры и ошибки, из-за которых теряют баллы."
            }
            
    return {
        "level": level.lower(),
        "type": type.lower(),
        "url": f"{level.lower()}/rules/{type.lower()}/",
        "template": "tests/page_dont_ready.html",
        "title": f"Правила экзамена {level} ({type}) | Start Deutsch",
        "seo_title": f"Правила экзамена {level} ({type}) | Start Deutsch (Примеры и советы)",
        "seo_description": "Полные правила проведения экзамена {level} ({type}). Что нужно знать и как подготовиться к экзамену {level} ({type})."
    }
    
    
def get_seo_data_for_tests(level=None, type=None):
    
    if level is None: level = ""
    if type is None: type = ""
    
    level = level.upper()
    type = type.upper()
    
    if type == "ALL":
        return {
            "title": f"Бесплатные тесты по немецкому {level} онлайн — экзамен Start Deutsch A1 | Start Deutsch",
            "seo_title": f"Бесплатные тесты по немецкому {level} онлайн — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
            "seo_description": f"Пройдите бесплатные тесты по немецкому языку уровня A1 онлайн. Подготовка к экзамену Goethe Start Deutsch A1."
        } 
        
    if type == "LESEN":
        return {
            "title": f"Тесты на понимание текста (Lesen) для уровня {level}.",
            "seo_title": f"Бесплатные тесты на понимание текста по немецкому {level} онлайн — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
            "seo_description": f"Пройдите бесплатные тесты на понимание текста по немецкому языку уровня A1 онлайн. Подготовка к экзамену Goethe Start Deutsch A1."
        }
        
    if type == "HOEREN" or type == "HÖREN":
        return {
            "title": f"Тесты для аудирования (Hören) для уровня {level}.",
            "seo_title": f"Бесплатные тесты на понимание на слух по немецкому {level} онлайн — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
            "seo_description": f"Пройдите бесплатные тесты на понимание на слух по немецкому языку уровня A1 онлайн. Подготовка к экзамену Goethe Start Deutsch A1."    
        } 
    
    if type == "SCHREIBEN":
        return {
            "title": f"Письменные тесты (Schreiben) для уровня {level}.",
            "seo_title": f"Бесплатные письменные тесты по немецкому {level} онлайн — экзамен Start Deutsch A1 | Start Deutsch (Примеры и советы)",
            "seo_description": f"Пройдите бесплатные письменные тесты на понимание текста по немецкому языку уровня A1 онлайн. Подготовка к экзамену Goethe Start Deutsch A1."
         
        } 
       
    return {
        "title": f"Тесты для уровня {level} {type} — экзамен Start Deutsch {level} | Start Deutsch",
        "seo_title": f"Тесты для уровня {level} {type} — экзамен Start Deutsch {level} | Start Deutsch (Примеры и советы)",
        "seo_description": f"Тесты для уровня {level} {type} — экзамен Start Deutsch {level}. Подготовка к экзамену Start Deutsch {level} с помощью тестов на понимание текста, аудирования, грамматики и словарного запаса."
    }
    
    
def get_context_for_money_page(level = None):
    
    if level is None:
        return {
            "url": f"/all/",
            "categories": [],
            "template": "tests/page_dont_ready.html",
            "title": f"Тесты для уровня {level} — экзамен Start Deutsch {level} | Start Deutsch",
            "seo_title": f"Тесты для уровня {level} — экзамен Start Deutsch {level} | Start Deutsch (Примеры и советы)",
            "seo_description": f"Тесты для уровня {level} — экзамен Start Deutsch {level}. Подготовка к экзамену Start Deutsch {level} с помощью тестов на понимание текста, аудирования, грамматики и словарного запаса."
        }
    
    categories = TestCategory.objects.annotate(tests_count=Count("exams", filter=Q(exams__level=level)))
    TestCategory.add_absolute_url(categories, level.slug)
    TestCategory.add_tests_count(categories, level)
    
    level_slug = level.slug.upper()
    
    if level_slug == "A1":
        return {
            "level": level_slug,
            "url": f"/{level_slug.lower()}/",
            "categories": categories,
            "template": "tests/a1/nemetskiy_a1_testy.html",
            "title": f"Бесплатные Тесты для уровня {level_slug} — экзамен Start Deutsch {level_slug} | Start Deutsch",
            "seo_title": f"Бесплатные тесты по немецкому {level_slug} онлайн",
            "seo_description": f"Пройдите бесплатные тесты по немецкому языку уровня {level_slug} онлайн. (Goethe Start Deutsch {level_slug}, Telc {level_slug}, ÖSD {level_slug})",
        }
    if level_slug == "A2":
        return {
            "level": level_slug,
            "url": f"/{level_slug.lower()}/",
            "categories": categories,
            "template": "tests/a1/nemetskiy_a1_testy.html",
            "title": f"Бесплатные Тесты для уровня {level_slug} — экзамен Start Deutsch {level_slug} | Start Deutsch",
            "seo_title": f"Бесплатные тесты по немецкому {level_slug} онлайн",
            "seo_description": f"Пройдите бесплатные тесты по немецкому языку уровня {level_slug} онлайн. (Goethe Start Deutsch {level_slug}, Telc {level_slug}, ÖSD {level_slug})",
        }
    if level_slug == "B1":
        return {
            "level": level_slug,
            "url": f"/{level_slug.lower()}/",
            "categories": categories,
            "template": "tests/a1/nemetskiy_a1_testy.html",
            "title": f"Бесплатные Тесты для уровня {level_slug} — экзамен Start Deutsch {level_slug} | Start Deutsch",
            "seo_title": f"Бесплатные тесты по немецкому {level_slug} онлайн",
            "seo_description": f"Пройдите бесплатные тесты по немецкому языку уровня {level_slug} онлайн. (Goethe Start Deutsch {level_slug}, Telc {level_slug}, ÖSD {level_slug})",
        }
    if level_slug == "B2":
        return {
            "level": level_slug,
            "url": f"/{level_slug.lower()}/",
            "categories": categories,
            "template": "tests/a1/nemetskiy_a1_testy.html",
            "title": f"Бесплатные Тесты для уровня {level_slug} — экзамен Start Deutsch {level_slug} | Start Deutsch",
            "seo_title": f"Бесплатные тесты по немецкому {level_slug} онлайн",
            "seo_description": f"Пройдите бесплатные тесты по немецкому языку уровня {level_slug} онлайн. (Goethe Start Deutsch {level_slug}, Telc {level_slug}, ÖSD {level_slug})",
        }    
    
    
    