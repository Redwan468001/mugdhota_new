from django import forms
from .models import ArtAndLiterature, Category


class AaLUploadForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        widget = forms.RadioSelect,
        empty_label = None
    )

    class Meta:
        model = ArtAndLiterature
        fields = ['title', 'author', 'content', 'feature_image', 'category']
        widgets = {
            'feature_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Write title'
        self.fields['content'].widget.attrs['placeholder'] = 'Write content part here...'
        self.fields['author'].widget.attrs['placeholder'] = 'Author name'
            