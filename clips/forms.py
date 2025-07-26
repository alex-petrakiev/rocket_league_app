from django import forms
from .models import Clip, Rating


class ClipUploadForm(forms.ModelForm):
    class Meta:
        model = Clip
        fields = ('title', 'description', 'video_file', 'thumbnail', 'category')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            if video.size > 100 * 1024 * 1024:  # 100MB limit
                raise forms.ValidationError('Video file too large. Maximum size is 100MB.')
        return video


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('score',)
        widgets = {
            'score': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)])
        }