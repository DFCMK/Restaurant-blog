from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import ListView
from .forms import CreateNewPostForm, PostUpdateForm, CommentForm
from django.contrib import messages
from .models import Post, Comment

from django.http import JsonResponse

#Tutorial based
def home(request):
    context = { 'posts': Post.objects.all() }
    return render(request, 'blog/home.html', context)

# Tutorial video 10 - 9:00min.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


# Based on simple.rocks: https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/ to create slugs
# Based on djangocentral: https://djangocentral.com/creating-comments-system-with-django/ for implementing comments
# Based on CI Walkthrew view
def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.
        
    **Context**
        
    ``post``
    An instance of :model:`blog.Post`.
        
    **Template:**
        
    :template:`blog/post_detail.html`
    """

    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by("-date_posted")
    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
    
    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form
        },
    )


# Based users/views.py profile
@login_required
def create_new_post(request):
    if request.method == 'POST':
        post_form = CreateNewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post was successfully submitted!')
            return redirect('blog-home')
        else:
            messages.error(request, 'There was an error submitting your post. Please check the form and try again.')
    else:
        post_form = CreateNewPostForm()
    
    context = {'post_form': post_form}
    return render(request, 'blog/create.html', context)


# Based on create_new_post view
@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post-detail', slug=slug)

    if request.method == 'POST':
        post_form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            post.update_slug()  # Update slug after saving the form
            post_form.save()  # Save the updated slug
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', slug=post.slug) 
        else:
            messages.error(request, 'There was an error updating your post. Please check the form and try again.')
    else:
        post_form = PostUpdateForm(instance=post)
    
    context = {'post_form': post_form, 'slug':slug}
    return render(request, 'blog/update_post.html', context)

# Based on update_post view
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, 'You are not authorized to delete this post!')
    else:
        post.delete()
        messages.success(request, 'Post deleted successfully!')

    return redirect('blog-home')

# Based on CI walk threw
@login_required
def edit_comment(request, comment_id, slug):
    post = get_object_or_404(Post, slug=slug)
    #comment_form = CommentForm(data=request.POST, instance=comment)
    comments = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment Updated!')
    else:
        messages.add_message(request, messages.ERROR, 'Error updating comment')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


# Based on CI walk threw
def delete_comment(request, slug, comment_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!')
        else:
            messages.error(request, 'You can only delete your own comments!')
    else: 
        messages.error(request, 'Invalid request method!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


#def vote(request, slug):
#    if request.method == 'GET':
#        return HttpResponseBadRequest("Voting requires POST request")
#
#    if request.method == 'POST':
#        post = get_object_or_404(Post, slug=slug)
#        vote_type = request.POST.get('vote_type')
#
#        if vote_type == 'upvote':
#            post.upvotes += 1
#        elif vote_type == 'downvote':
#            post.downvotes += 1
#        else:
#            return JsonResponse({'success': False, 'error': 'Invalid vote type.'})
#
#        # Directly save the model to update database counts
#        post.save()
#        return JsonResponse({'success': True})


#def vote_up(request, slug):
#    post = Post.objects.get(Post, slug)
#    post.vote_up_or_down(True)
#    return JsonResponse({'success': True})

#def vote_down(request, slug):
#    post = Post.objects.get(Post, slug)
#    post.vote_up_or_down(False)
#    return JsonResponse({'success': True})

#def total_votes(request, post_id):
#    post = Post.object.get(id=post_id)
#    post.total_votes(True)
#    return JsonResponse(int=votes_total)

def likes(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return redirect('blog-home')


def about(request):
        return render(request, 'blog/about.html', {'title': 'About'})