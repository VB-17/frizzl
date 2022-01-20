from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from accounts.models import UserProfile


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['caption'].widget.attrs = {
            'class': 'textarea', 'placeholder': 'Write a caption....'}
        self.fields['img'].widget.attrs = {'placeholder': 'Upload photo'}

    class Meta:
        model = Post
        fields = ['caption', 'img']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'comment-box', 'placeholder': 'Write a comment....'})
        }


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['email'].widget.attrs['class'] = 'form-input'
    
    class Meta:
        model = User
        fields = ['username', 'email' ]


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['class'] = 'image-picker'
        self.fields['bio'].widget.attrs = {'class': 'textarea', 'placeholder': 'Your Bio....'}
    
    photo = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['photo', 'bio']
