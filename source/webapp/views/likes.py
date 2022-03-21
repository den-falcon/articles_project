from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from webapp.models import Article, Comment


class ArticleLikeView(TemplateView):

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        article.add_like()
        return JsonResponse(article.make_response())

    def delete(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        article.delete_like()
        return JsonResponse(article.make_response())


class CommentLikeView(TemplateView):

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        comment.add_like()
        return JsonResponse(comment.make_response())

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        comment.delete_like()
        return JsonResponse(comment.make_response())
