BREADCRUMB_MAP = {
    "home": {
        "title": "Главная",
        "parent": None,
        "url": "/",
    },
    
    "articles": {
        "title": "Статьи",
        "parent": "home",
        "url": "/articles/",
    },
        "article_detail": {
            "title": "Статья",
            "parent": "articles",
        },

    "exams": {
        "title": "Тесты",
        "parent": "home",
        "url": "/exams/",
    },

        "a1": {
            "title": "Немецкий A1",
            "parent": "exams",
            "url": "/nemetskiy-a1-testy/",
        },

            "lesen": {
                "title": "Lesen",
                "parent": "a1",
            },

            "hoeren": {
                "title": "Hören",
                "parent": "a1",
            },

            "grammatik": {
                "title": "Grammatik",
                "parent": "a1",
            },

            "sprachen": {
                "title": "Sprachenschatz",
                "parent": "a1",
            },
}