from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import Now
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Post, User, Comment, Category
from .forms import PostForm, CommentForm, UserForm
from blogicum.settings import POSTS_PER_PAGE


def get_paginated_objects(objects, page_number, per_page=POSTS_PER_PAGE):
    paginator = Paginator(objects, per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template_name = 'blog/index.html'
    post_list = (
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=Now(),
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    return render(request, template_name,
                  {'page_obj': get_paginated_objects(post_list, request)})


def user_profile(request, username):
    template_name = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    if request.user.username == username:
        post_list = (
            Post.objects.filter(author__username=username)
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )
    else:
        post_list = (
            Post.objects.filter(
                author__username=username,
                is_published=True,
                category__is_published=True,
                pub_date__lte=Now(),
            )
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )
    page_number = request.GET.get('page')
    context = {
        'profile': profile,
        'page_obj': get_paginated_objects(post_list, page_number,
                                          per_page=POSTS_PER_PAGE),
    }
    return render(request, template_name, context)


class EditUserProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class CategoryPost(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        self.category = category
        return (
            category.posts.filter(
                is_published=True,
                pub_date__lte=Now(),
            )
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_object(self):
        obj = super(PostDetail, self).get_object()
        if (self.request.user != obj.author
                and (not obj.is_published or not obj.category.is_published)):
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments
            .select_related('author')
            .order_by('created_at')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', post_pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit_post'] = True
        return context


@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_pk=post_pk)


@login_required
def edit_comment(request, post_pk, comment_id):
    comment = get_object_or_404(
        Comment,
        post_id=post_pk,
        id=comment_id,
        author__username=request.user,
    )
    if request.method == 'GET':
        form = CommentForm(instance=comment)
        context = {
            'form': form,
            'comment': comment,
        }
        return render(request, 'blog/comment.html', context)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('blog:post_detail', post_pk=post_pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_pk, comment_id):
    delete_comment = get_object_or_404(
        Comment, post_id=post_pk, id=comment_id, author__username=request.user
    )
    if request.method == "POST":
        delete_comment.delete()
        return redirect('blog:post_detail', post_pk=post_pk)
    context = {
        'form': None,
        'comment': delete_comment,
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_post(request, post_id):
    template_name = 'blog/post_form.html'
    delete_post = get_object_or_404(
        Post, pk=post_id, author__username=request.user
    )
    if request.method == "POST":
        delete_post.delete()
        return redirect('blog:profile', request.user)
    else:
        context = {
            'post': delete_post,
        }
    return render(request, template_name, context)
