from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Clip(models.Model):
    CATEGORY_CHOICES = [
        ('goal', 'Amazing Goal'),
        ('save', 'Epic Save'),
        ('aerial', 'Aerial Play'),
        ('freestyle', 'Freestyle'),
        ('teamplay', 'Team Play'),
        ('funny', 'Funny Moment'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='clips/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_approved = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('clips:detail', kwargs={'pk': self.pk})


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'clip')

    def __str__(self):
        return f'{self.user.username} rated {self.clip.title}: {self.score}/5'