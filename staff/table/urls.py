from django.urls import path

from base.common.constant.view_action import BaseViewAction, TableExtraViewAction
from staff.table.views.viewset import TableViewSet

urlpatterns = [
    path("create", TableViewSet.as_view({"post": BaseViewAction.CREATE})),
    path("list", TableViewSet.as_view({"get": BaseViewAction.LIST})),
    path("<int:pk>/detail", TableViewSet.as_view({"get": BaseViewAction.RETRIEVE})),
    path("<int:pk>/delete", TableViewSet.as_view({"delete": BaseViewAction.DESTROY})),
    path("<int:pk>/update", TableViewSet.as_view({"put": BaseViewAction.UPDATE})),
    path(
        "<int:pk>/staff_in",
        TableViewSet.as_view({"put": TableExtraViewAction.STAFF_IN}),
    ),
    path(
        "<int:pk>/staff_out",
        TableViewSet.as_view({"put": TableExtraViewAction.STAFF_OUT}),
    ),
]
