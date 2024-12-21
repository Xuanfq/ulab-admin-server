from rest_framework.routers import SimpleRouter

from power.views.admin.apcpdupower import ApcPduPowerAdminView
from power.views.user.apcpdupower import ApcPduPowerUserView

router = SimpleRouter(False)

router.register("admin/apcpdupower", ApcPduPowerAdminView, basename="admin_apcpdu_power")
router.register("user/apcpdupower", ApcPduPowerUserView, basename="user_apcpdu_power")

urlpatterns = []
urlpatterns += router.urls
