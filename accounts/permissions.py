from rest_framework.permissions import BasePermission


def get_user_role(request):
    if not request.user or not request.user.is_authenticated:
        return None

    if not hasattr(request.user, "profile"):
        return None

    return request.user.profile.role


class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request) == "COMPANY_ADMIN"


class IsDistributorManager(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request) == "DISTRIBUTOR_MANAGER"


class IsStoreManager(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request) == "STORE_MANAGER"