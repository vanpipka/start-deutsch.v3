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
            
            "home": "home",
            "exam_list": "exams",
            # SEO A1 pages
            "money_page": "a1",
            "lesen_test_a1": "lesen_a1",
            "hoeren_test_a1": "hoeren_a1",
            "grammatik_test_a1": "grammatik_a1",
            "sprachen_test_a1": "sprachen_a1",
            # SEO A2 pages
            "money_page_A2": "a2",
            "lesen_test_a2": "lesen_a2",
            "hoeren_test_a2": "hoeren_a2",
            "grammatik_test_a2": "grammatik_a2",
            "sprachen_test_a2": "sprachen_a2",
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