from articles.models import SiteSettings


def get_site_settings():
    
    try:
        return SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        return None