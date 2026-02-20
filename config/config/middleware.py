from django.urls import resolve
from .breadcrumbs import BREADCRUMB_MAP


class BreadcrumbMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.breadcrumbs = self.build_breadcrumbs(request)

        response = self.get_response(request)
        return response

    def build_breadcrumbs(self, request):

        try:
            match = resolve(request.path_info)
            url_name = match.url_name
        except Exception:
            return []

        # сопоставление url → breadcrumb node
        mapping = {
            "exam_detail": "exams",
            "money_page": "a1",
            "home": "home",
            "exam_list": "exams",
            "lesen_test": "lesen",
            "hoeren_test": "hoeren",
            "grammatik_test": "grammatik",
            "sprachen_test": "sprachen",
            # Articles
            "article_list": "articles",
            "article_detail": "article_detail",
        }

        node_key = mapping.get(url_name)

        if not node_key:
            return []

        crumbs = []

        while node_key:
            node = BREADCRUMB_MAP[node_key]

            title = node["title"]
            url = node.get("url")
            
            if not url:
                title = request.path.split('/')[-2].replace('-', ' ').capitalize()

            crumbs.append({
                "title": title,
                "url": url,
            })

            node_key = node["parent"]

        return list(reversed(crumbs))