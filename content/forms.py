from django import forms
from . models import Content, Category, SubCategory, Tag


class ContentUploadForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all().distinct(), empty_label='Select Category', required=False)

    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.all().distinct(), empty_label='Select Subcategory', required=False)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    new_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter new tags separated by commas'}))

    class Meta:
        model = Content
        fields = ['title', 'author', 'content', 'feature_image', 'category', 'sub_category', 'tags']
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

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sub_category'].queryset = SubCategory.objects.filter(category=self.instance.category).order_by(
                'name')
