from django.urls import path

from base.common.constant.view_action import BaseViewAction
from staff.profile.views.viewset import ProfileViewSet

urlpatterns = [
    path("<int:pk>/detail", ProfileViewSet.as_view({"get": BaseViewAction.RETRIEVE})),
    path("<int:pk>/delete", ProfileViewSet.as_view({"delete": BaseViewAction.DESTROY})),
]
