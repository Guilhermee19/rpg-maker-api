from rest_framework import permissions


class IsSessionMaster(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.master == request.user


class IsSessionMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.members.filter(user=request.user).exists()