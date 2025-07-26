from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Tournament(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    max_participants = models.IntegerField(default=16)
    prize_pool = models.CharField(max_length=100, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    participants = models.ManyToManyField(User, related_name='tournaments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tournaments:detail', kwargs={'pk': self.pk})

    @property
    def participants_count(self):
        return self.participants.count()

    @property
    def is_full(self):
        return self.participants_count >= self.max_participants