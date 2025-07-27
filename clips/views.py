from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Avg
from .models import Clip, Rating
from .forms import ClipUploadForm, RatingForm


class ClipListView(ListView):
    model = Clip
    template_name = 'clips/list.html'
    context_object_name = 'clips'
    paginate_by = 12

    def get_queryset(self):
        return Clip.objects.filter(is_approved=True)


class ClipDetailView(DetailView):
    model = Clip
    template_name = 'clips/detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clip = self.get_object()

        # Calculate average rating
        avg_rating = clip.ratings.aggregate(avg=Avg('score'))['avg']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['total_ratings'] = clip.ratings.count()

        # Check if user has rated
        if self.request.user.is_authenticated:
            context['user_rating'] = clip.ratings.filter(user=self.request.user).first()
            context['rating_form'] = RatingForm()

        return context


@login_required
def clip_upload_view(request):
    if request.method == 'POST':
        form = ClipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            clip = form.save(commit=False)
            clip.author = request.user
            clip.save()
            messages.success(request, 'Clip uploaded successfully! It will be reviewed before going live.')
            return redirect('clips:detail', pk=clip.pk)
    else:
        form = ClipUploadForm()
    return render(request, 'clips/upload.html', {'form': form})


@login_required
def rate_clip_view(request, pk):
    clip = get_object_or_404(Clip, pk=pk)

    if request.method == 'POST':
        # Check if user already rated this clip
        rating, created = Rating.objects.get_or_create(
            user=request.user,
            clip=clip,
            defaults={'score': request.POST.get('score')}
        )

        if not created:
            rating.score = request.POST.get('score')
            rating.save()
            messages.success(request, 'Your rating has been updated!')
        else:
            messages.success(request, 'Thank you for rating this clip!')

    return redirect('clips:detail', pk=pk)