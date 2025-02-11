from django import forms
from .models import ArtAndLiterature, Category
from config.models import Tag

class AaLUploadForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    new_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter new tags separated by commas'}))

    class Meta:
        model = ArtAndLiterature
        fields = ['title', 'author', 'content', 'feature_image', 'category', 'tags']
        widgets = {
            'feature_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean_new_tags(self):
        new_tags = self.cleaned_data.get('new_tags', '').split(',')
        return [tag.strip() for tag in new_tags if tag.strip()]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Write title'
        self.fields['content'].widget.attrs['placeholder'] = 'Write content part here...'
        self.fields['author'].widget.attrs['placeholder'] = 'Author name'
            