from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from comments.models import Comment
from .forms import PostForm, CommentForm
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    """Список опубликованных постов."""
    posts = Post.objects.filter(is_published=True)
    context = {
        "posts": posts,
        "page_title": "Блог",
    }
    return render(request, "posts/post_list.html", context)


def post_detail(request, pk):
    """Детальная страница одного поста с комментариями."""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.filter(is_active=True)
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST' and comment_form.is_valid():
        author, _ = User.objects.get_or_create(username=comment_form.cleaned_data['username'])
        Comment.objects.create(
            post=post,
            author=author,
            text=comment_form.cleaned_data['text'],
        )
        return redirect('posts:post_detail', pk=pk)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'page_title': post.title,
    }
    return render(request, 'posts/post_detail.html', context)

def post_create(request):
    form = PostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        author, _ = User.objects.get_or_create(username=form.cleaned_data['username'])
        post = form.save(commit=False)
        post.author = author
        post.save()
        return redirect('posts:post_detail', pk=post.pk)

    return render(request, 'posts/post_form.html', {'form': form})