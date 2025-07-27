from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import ForumPost, Comment
from .forms import ForumPostForm, CommentForm


class ForumPostListView(ListView):
    model = ForumPost
    template_name = 'forum/list.html'
    context_object_name = 'posts'
    paginate_by = 10


class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'forum/detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


@login_required
def forum_post_create_view(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('forum:detail', pk=post.pk)
    else:
        form = ForumPostForm()
    return render(request, 'forum/create.html', {'form': form})


@login_required
def add_comment_view(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')

    return redirect('forum:detail', pk=pk)