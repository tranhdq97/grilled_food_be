from rest_framework.permissions import IsAuthenticated

from base.common.constant.master import MasterStaffTypeID


class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.is_staff


class IsEmployee(IsStaff):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.type_id == MasterStaffTypeID.EMPLOYEE
        )


class IsManager(IsStaff):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.type_id == MasterStaffTypeID.MANAGER
        )


class IsSuperStaff(IsStaff):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.type_id == MasterStaffTypeID.SUPER_STAFF
        )


class IsApproved(IsStaff):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.type_id != MasterStaffTypeID.UNAPPROVED
        )
