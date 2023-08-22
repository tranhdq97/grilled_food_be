from django.urls import path

from base.common.constant.view_action import BaseViewAction
from staff.item.views.viewset import ItemViewSet

urlpatterns = [
    path("create", ItemViewSet.as_view({"post": BaseViewAction.CREATE})),
    path("list", ItemViewSet.as_view({"get": BaseViewAction.LIST})),
    path("<int:pk>/detail", ItemViewSet.as_view({"get": BaseViewAction.RETRIEVE})),
    path("<int:pk>/delete", ItemViewSet.as_view({"delete": BaseViewAction.DESTROY})),
    path("<int:pk>/update", ItemViewSet.as_view({"put": BaseViewAction.UPDATE})),
]
