from django.shortcuts import get_object_or_404, redirect
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from .forms import MainForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse


class OnlyPostAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            post = self.get_object()
            return self.request.user == post.author
        return False


class OnlyCommentAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            comment = self.get_object()
            return self.request.user == comment.author
        return False


class EndpointPostListView(ListView):
    model = Post
    queryset = Post.objects.published_posts()
    template_name = 'blog/endpoint.html'
    paginate_by = 10
    context_object_name = 'post_list'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'

    def get_queryset(self):
        user = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if user.is_authenticated and user == post.author:
            return Post.objects.all()
        return Post.objects.published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.all().order_by('created_at')
        context['comments'] = comments
        context['form'] = CommentForm()
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return category.posts.published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return context


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user_obj = get_object_or_404(User, username=username)
        is_authenticated = self.request.user.is_authenticated
        is_correct_user = self.request.user == user_obj

        if is_authenticated and is_correct_user:
            posts = user_obj.posts.all()
        else:
            posts = user_obj.posts.published_posts()

        for post in posts:
            post.comment_count = post.comments.count()

        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        'username', 'first_name', 'last_name', 'email'
    )
    template_name = 'blog/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = MainForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(OnlyPostAuthorMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    form_class = MainForm

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class PostDeleteView(OnlyPostAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:endpoint')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MainForm(instance=self.object)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post,
                                               id=self.kwargs.get('post_id'))
        response = super().form_valid(form)
        post = form.instance.post
        post = Post.objects.published_posts().get(pk=post.pk)
        return response

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentUpdateView(OnlyCommentAuthorMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    slug_field = 'id'
    slug_url_kwarg = 'comment_id'
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentDeleteView(OnlyCommentAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    slug_field = 'id'
    slug_url_kwarg = 'comment_id'
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object().post
        response = super().delete(request, *args, **kwargs)
        post = Post.objects.published_posts().get(pk=post.pk)
        return response
