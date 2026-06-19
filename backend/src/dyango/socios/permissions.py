from rest_framework.permissions import SAFE_METHODS, BasePermission

from .roles import ROLE_ADMIN, ROLE_SUPERADMIN, resolver_rol_usuario


class IsAuthenticatedAndRoleBasedWritePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        rol = resolver_rol_usuario(user)
        return rol in {ROLE_SUPERADMIN, ROLE_ADMIN}
