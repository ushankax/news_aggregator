from .models import Article
from rest_framework import serializers


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['url', 'source', 'title', 'text', 'link']


class ArticleListSerializer(ArticleSerializer):
    text = serializers.SerializerMethodField()

    def get_text(self, article):
        return article.text[:700]
