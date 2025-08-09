from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Tournament
from .forms import TournamentCreateForm


class TournamentListView(ListView):
    model = Tournament
    template_name = 'tournaments/list.html'
    context_object_name = 'tournaments'

    def get_queryset(self):
        return Tournament.objects.exclude(status='cancelled')


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'


@login_required
def tournament_create_view(request):
    if request.method == 'POST':
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.organizer = request.user
            tournament.save()
            messages.success(request, 'Tournament created successfully!')
            return redirect('tournaments:detail', pk=tournament.pk)
    else:
        form = TournamentCreateForm()
    return render(request, 'tournaments/create.html', {'form': form})


@login_required
def join_tournament_view(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)

    if tournament.is_full:
        messages.error(request, 'This tournament is full!')
    elif request.user in tournament.participants.all():
        messages.info(request, 'You are already registered for this tournament.')
    else:
        tournament.participants.add(request.user)
        messages.success(request, f'Successfully joined {tournament.name}!')

    return redirect('tournaments:detail', pk=pk)