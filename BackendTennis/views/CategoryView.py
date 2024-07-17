# BackendTennis/views/CategoryView.py

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from BackendTennis.models import Category
from BackendTennis.serializers import CategorySerializer


class CategoryListCreateView(ListCreateAPIView):
    """
    View to handle creating and listing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    View to handle retrieving, updating, and deleting a single category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
