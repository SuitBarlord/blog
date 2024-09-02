from django.forms import ModelForm
from .models import Post
from django import forms


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('topic', 'content', 'author')
        
        
class EditPostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ('id', 'topic', 'content', 'author')
        
    id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': False}))
