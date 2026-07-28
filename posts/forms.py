from django import forms
from .models import Post, Category, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "featured_image",
            "category",
            "tags",
            "status",
        ]

        widgets = {
            "content": forms.Textarea(attrs={"rows": 8}),
            "tags": forms.CheckboxSelectMultiple(),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["tag_name"]