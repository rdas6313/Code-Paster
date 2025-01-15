from rest_framework import permissions


class PastePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        authenticated_actions = ['update', 'partial_update', 'destroy']
        if view.action in authenticated_actions and not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        object_actions = ['update', 'partial_update', 'destroy']
        if view.action in object_actions:
            if obj.user:
                return obj.user.id == request.user.id
            else:
                return False
        elif view.action == 'retrieve':
            if not obj.sharable:
                if request.user.is_authenticated and obj.user:
                    return obj.user.id == request.user.id
                return False
            else:
                if obj.password:
                    return (obj.user and obj.user.id == request.user.id)
                return True
        elif view.action == 'retrieve_password_view':
            if not obj.sharable:
                return (obj.user and obj.user.id == request.user.id)
            return True

        return super().has_object_permission(request, view, obj)
