from rest_framework.routers import SimpleRouter

from nettraversal.views.admin.netforward import NetForwardAdminView
from nettraversal.views.user.netforward import NetForwardUserView

router = SimpleRouter(False)  # Set to False to remove the slash after the URL

router.register("admin/netforward", NetForwardAdminView, basename="admin_netforward")
router.register("user/netforward", NetForwardUserView, basename="user_netforward")

urlpatterns = []
urlpatterns += router.urls
