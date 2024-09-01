from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .permissions import IsCustomerOrAdmin
from .mixins import PlatformApiCallMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class OrderViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['products']
    search_fields = ['products__name']
    ordering_fields = ['amount']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset.select_related('customer', 'seller').prefetch_related('products')
        return queryset.filter(customer__user=self.request.user).select_related('customer', 'seller').prefetch_related('products')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ordering = request.query_params.get('ordering', 'amount')
        if ordering.startswith('-'):
            queryset = queryset.order_by(ordering)[:5]
        else:
            queryset = queryset.order_by(f'-{ordering}')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Delete the token
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)    


