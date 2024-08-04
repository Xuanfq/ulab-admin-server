from rest_framework.routers import SimpleRouter

from nettraversal.views import NetForwardView

router = SimpleRouter(False)  # Set to False to remove the slash after the URL

router.register("netforward", NetForwardView, basename="netforward")

urlpatterns = []
urlpatterns += router.urls
