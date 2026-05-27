from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from django.http import Http404
from .forms import PostForm, ProfileForm, CommentForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def index(request):
    template = 'blog/index.html'

    posts = Post.objects.select_related('category').filter(
        Q(pub_date__lte=datetime.now())
        & Q(is_published=True)
        & Q(category__is_published=True)
    ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def detail(request, post_id):
    template = 'blog/detail.html'

    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')

    form = CommentForm(request.POST or None,)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        form.save()

    if post is None:
        raise Http404('Error')
    elif post.is_published is False:
        if post.author != request.user:
            raise Http404('Error')
    elif post.category.is_published is False:
        if post.author != request.user:
            raise Http404('Error')
    elif post.pub_date > datetime.now(pytz.utc):
        if post.author != request.user:
            raise Http404('Error')

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, template, context)


def category(request, category_slug):
    template = 'blog/category.html'

    posts = Post.objects.select_related('category').filter(
        Q(is_published=True)
        & Q(pub_date__lte=datetime.now())
        & Q(category__slug=category_slug)
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category = get_object_or_404(Category, slug=category_slug)

    if category is None:
        raise Http404('Категория не существует')
    elif category.is_published is False:
        raise Http404('Категория, снятая с публикации')
    else:
        context = {
            'page_obj': page_obj,
            'category': category,
        }

    return render(request, template, context)


def profile(request, username_slug):

    profile = get_object_or_404(User, username=username_slug)

    if username_slug == request.user.username:
        posts = Post.objects.select_related(
            'author'
        ).filter(author__username=username_slug).order_by('-pub_date')

    else:
        posts = Post.objects.select_related(
            'author'
        ).filter(
            Q(author__username=username_slug)
            & Q(pub_date__lte=datetime.now())
            & Q(is_published=True)
            & Q(category__is_published=True)
        ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj
    }

    return render(request, 'blog/profile.html', context)


@login_required
def create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        form.save()
        return redirect(f'/profile/{request.user.username}/')

    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


def edit(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user.is_anonymous or request.user != post.author:
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('blog:post_detail', post_id)

    form = PostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


@login_required
def delete(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user.is_anonymous or request.user != post.author:
        return redirect('blog:post_detail', post_id)

    if request.method == "POST":
        post.delete()
        return redirect('blog:profile', request.user.username)

    form = PostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id)

    else:
        raise Http404()


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user.is_anonymous or request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.post_id = post_id
            form.id = comment_id
            form.save()
        return redirect('blog:post_detail', post_id)

    form = CommentForm(instance=comment)
    context = {
        'form': form,
        'comment': comment
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user.is_anonymous or request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_id)

    context = {
        'comment': comment
    }

    return render(request, 'blog/comment.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect(f'/profile/{request.user.username}/')

    form = ProfileForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'blog/user.html', context)


def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')
