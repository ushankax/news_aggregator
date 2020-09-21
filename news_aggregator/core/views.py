from rest_framework import viewsets, permissions
from .serializers import ArticleSerializer, ArticleListSerializer
from .models import Article


class ArticleViewSet(viewsets.ModelViewSet):
    """list of news by subscription for authorised users only"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """filter news by current user subscriptions"""
        subs = self.request.user.profile.subscriptions
        return Article.objects.filter(source__in=subs).order_by('-import_date')

    def get_serializer_class(self):
        """news with preview text when listing"""
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer
