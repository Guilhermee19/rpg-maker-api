from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.filter(
            session__members__user=self.request.user
        ).select_related('session').distinct()

        session_id = self.request.query_params.get('session')
        if session_id:
            queryset = queryset.filter(session_id=session_id)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)

        rarity = self.request.query_params.get('rarity')
        if rarity:
            queryset = queryset.filter(rarity__iexact=rarity)

        return queryset.order_by('name')

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.session.master != self.request.user:
            raise PermissionDenied("Apenas o mestre pode editar itens.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.session.master != self.request.user:
            raise PermissionDenied("Apenas o mestre pode remover itens.")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Item removido com sucesso"}, status=200)