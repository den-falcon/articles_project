from rest_framework import serializers
from webapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "title", "content", "author_id")
        read_only_fields = ("id", "author_id")
