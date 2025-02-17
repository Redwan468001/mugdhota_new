from django import forms
from ArtAndLiterature.models import ArtAndLiterature
from config.models import Tag
from ArtAndLiterature.models import Category


class EditUserUploadedContent(forms.ModelForm):
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

    revised_comment = forms.CharField(max_length=355, required=False)

    new_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter new tags separated by commas'}))

    class Meta:
        model = ArtAndLiterature
        fields = ['title', 'author', 'content', 'feature_image', 'category', 'tags', 'status', 'reviewed_comments']
        widgets = {
            'feature_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

        def clean_new_tags(self):
            new_tags = self.cleaned_data.get('new_tags', '').split(',')
            return [tag.strip() for tag in new_tags if tag.strip()]

