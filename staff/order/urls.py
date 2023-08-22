from django.urls import path

from base.common.constant.view_action import BaseViewAction, OrderExtraViewAction
from staff.order.views.viewset import OrderViewSet

urlpatterns = [
    path("create", OrderViewSet.as_view({"post": BaseViewAction.CREATE})),
    path("list", OrderViewSet.as_view({"get": BaseViewAction.LIST})),
    path("<int:pk>/detail", OrderViewSet.as_view({"get": BaseViewAction.RETRIEVE})),
    path("<int:pk>/update", OrderViewSet.as_view({"put": BaseViewAction.UPDATE})),
    path("<int:pk>/delete", OrderViewSet.as_view({"delete": BaseViewAction.DESTROY})),
    path("<int:pk>/order", OrderViewSet.as_view({"put": OrderExtraViewAction.ORDER})),
]
