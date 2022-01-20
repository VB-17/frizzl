from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserProfile
from posts.models import Post
from django.views.generic import View
from posts.forms import PostForm, UserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here


class HomeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def get(self, request):
        form = PostForm()
        users = UserProfile.objects.all().order_by('-created_at').exclude(
            user=request.user
        )[:10]
        posts = Post.objects.all().order_by('-created_at')

        if not request.user.is_authenticated:
            return redirect('accounts:login')

        return render(request, 'pages/index.html', {
            'form': form,
            'posts': posts,
            'users': users
        })

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        users = UserProfile.objects.all().order_by('-created_at')
        posts = Post.objects.all().order_by('-created_at')

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.userprofile
            post.save()
            return render(request, 'pages/index.html', {
                'form': form,
                'posts': posts,
                'users': users
            })
        else:
            form = PostForm()
            return render(request, 'pages/index.html',  {'form': form, 'posts': posts})


@login_required
def user_profile_view(request, username,  *args, **kwargs):
    user_profile = UserProfile.objects.get(user__username=username)
    posts = user_profile.profile_posts()

    is_followed = False

    if (user_profile.followers.filter(id=request.user.userprofile.id).exists()):
        is_followed = True

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('pages:profile', username=request.user.username)
        else:
            messages.error(request, 'Invalid form inputs')

    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'pages/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'posts': posts,
        'user_profile': user_profile,
        'is_followed': is_followed
    })


@login_required
def follow_user_view(request):
    username = request.POST.get('username')
    source_user = request.user.userprofile
    user = UserProfile.objects.get(user__username=username)

    if user.followers.filter(id=source_user.id).exists():
        user.followers.remove(source_user)
        source_user.following.remove(user)
        messages.success(request, f'Unfollowed {user.user.username}')
    else:
        user.followers.add(source_user)
        source_user.following.add(user)
        messages.success(request, f'Followed {user.user.username}')

    return redirect('pages:profile', username=username)
