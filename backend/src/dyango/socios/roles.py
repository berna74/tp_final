ROLE_SUPERADMIN = 'superadmin'
ROLE_ADMIN = 'admin'
ROLE_SOCIO = 'socio'


def resolver_rol_usuario(user):
    if user.is_superuser:
        return ROLE_SUPERADMIN

    group_names = {group.name.lower() for group in user.groups.all()}
    if 'superadmin' in group_names:
        return ROLE_SUPERADMIN

    if user.is_staff or 'admin' in group_names:
        return ROLE_ADMIN

    return ROLE_SOCIO
