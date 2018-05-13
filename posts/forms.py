from django import forms
from  .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','description','image')
        widgets= {
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
        }