from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    """Список опубликованных постов."""
    posts = Post.objects.filter(is_published=True)
    context = {
        "posts": posts,
        "page_title": "Блог",
    }
    return render(request, "posts/post_list.html", context)


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Детальная страница одного поста с комментариями."""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.filter(is_active=True)
    context = {
        "post": post,
        "comments": comments,
        "page_title": post.title,
    }
    return render(request, "posts/post_detail.html", context)
