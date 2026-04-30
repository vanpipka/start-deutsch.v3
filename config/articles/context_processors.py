from articles.services import get_site_settings


def company_contacts(request):

    settings = get_site_settings()
    return {
        'company_phone': settings.phone if settings else '',
        'company_email': settings.email if settings else '',
        'company_address': settings.address if settings else '',
        'company_mobile_phone': settings.mobile_phone if settings else '',
    }