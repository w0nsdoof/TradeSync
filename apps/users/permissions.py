from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsTrader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "trader"

class IsSalesman(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "salesman"

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"
