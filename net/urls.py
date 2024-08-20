from rest_framework.routers import SimpleRouter

from net.views.admin.portforward import PortForwardAdminView
from net.views.user.portforward import PortForwardUserView

router = SimpleRouter(False)  # Set to False to remove the slash after the URL

router.register("admin/portforward", PortForwardAdminView, basename="admin_portforward")
router.register("user/portforward", PortForwardUserView, basename="user_portforward")

urlpatterns = []
urlpatterns += router.urls
