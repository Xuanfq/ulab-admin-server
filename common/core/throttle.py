

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class RegisterThrottle(AnonRateThrottle):
    scope = "register"


class UploadThrottle(UserRateThrottle):
    """上传速率限制"""
    scope = "upload"


class Download1Throttle(UserRateThrottle):
    """下载速率限制"""
    scope = "download1"


class Download2Throttle(UserRateThrottle):
    """下载速率限制"""
    scope = "download2"
