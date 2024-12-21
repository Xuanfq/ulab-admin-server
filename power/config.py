from django.urls import path, include

# Routing configuration, when the APP is added, it will automatically inject routing to the overall service
URLPATTERNS = [
    path("api/power/", include("power.urls")),
]

# Request whitelist, supports regular expressions, can refer to PERMission-WeihITE-URL in settings. py
PERMISSION_WHITE_REURL = [
    "^/api/power/.*choices$",
    "^/api/power/.*search-fields$",
]
