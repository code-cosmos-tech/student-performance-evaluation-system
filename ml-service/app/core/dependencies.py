from app.core.config import settings


def get_api_service_name():
    return settings.app_name


def get_api_version():
    return settings.app_version
