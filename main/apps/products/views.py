from rest_framework import viewsets, permissions

from apps.users.permissions import IsAdmin, IsSalesman
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]  
        return [permissions.AllowAny()]  

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [
                permissions.IsAuthenticated(), 
                permissions.OR(
                    IsSalesman(),
                    IsAdmin()
                )
            ]  
        return [permissions.AllowAny()]
