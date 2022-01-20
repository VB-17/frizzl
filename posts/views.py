from http.client import HTTPResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from ordered_set import OrderedSet


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentForm
    context_object_name = 'post'
    login_url = reverse_lazy('accounts:login')

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user.userprofile
        comment.post = Post.objects.get(id=self.kwargs['pk'])
        comment.save()
        messages.success(self.request, "Comment posted")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "An error occured comment could'nt be posted")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        post_id = self.kwargs['pk']
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = self.form_class()

        user = Post.objects.get(id=post_id).user
        post_has_liked = Post.objects.get(id=post_id).likes.filter(id=self.request.user.id).exists()

        comments = OrderedSet()
        for comment in Comment.objects.filter(post=post_id):
            is_liked = comment.likes.filter(id=self.request.user.id).exists()
            comments.add((comment, is_liked))
    
        context['comments'] = comments
        context['user_profile'] = user
        context['post_is_liked'] = True if post_has_liked else False
        context['form'] = form

    
        return context


@login_required
def post_like_view(request):
    post = Post.objects.get(id=request.POST.get('post_id'))
    user = request.user.userprofile

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('posts:detail', pk=post.id)

@login_required
def comment_like_view(request):
    comment = Comment.objects.get(id=request.POST.get('comment_id'))
    user = request.user.userprofile

    if comment.likes.filter(id=user.id).exists():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)

    return redirect('posts:detail', pk=comment.post.id)


@login_required
def post_delete_view(request, pk):
    post = Post.objects.get(id=pk)

    if post.user.user == request.user:
        post.delete()
        messages.success(request, "Post deleted")
        return redirect('pages:index')
    else: 
        messages.error(request, "You are not authorized to delete this post")
        return redirect('posts:detail', pk=pk)
