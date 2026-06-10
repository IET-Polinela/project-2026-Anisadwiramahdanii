from rest_framework import permissions


class IsCitizen(permissions.BasePermission):
    message = 'Hanya Citizen yang dapat membuat laporan.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_member
        )


class IsOwnerAndDraft(permissions.BasePermission):
    message = 'Laporan hanya dapat diubah atau dihapus oleh pemilik saat status masih DRAFT.'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.reporter == request.user
            and obj.status == 'DRAFT'
        )

class IsAdminStatusOnlyOrOwnerAndDraft(permissions.BasePermission):
    message = 'Admin hanya dapat mengubah status. Citizen hanya dapat mengubah atau menghapus draft miliknya.'

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_admin:
            return (
                view.action == 'partial_update'
                and set(request.data.keys()) == {'status'}
            )

        return bool(
            request.user.is_member
            and obj.reporter == request.user
            and obj.status == 'DRAFT'
        )
