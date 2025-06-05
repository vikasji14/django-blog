from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import form as fm
from .models import Post, PostLike, Category
from django.contrib.auth import get_user_model
from django.utils  import timezone
User = get_user_model()

@login_required
def add_post(request):
    if request.method == 'POST':
        form = fm.AddPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post added successfully!')
            return redirect('post-details', post.pk)
        else:
            messages.warning(request, 'Error adding post. Please correct the errors below.')
            return redirect('add-post')
    else:
        form = fm.AddPostForm()
        context = {'form': form}
    return render(request, 'post/add_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.author == request.user:
        messages.error(request, 'You are not authorized to update this post.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = fm.UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post-details', post.pk)
        else:
            messages.warning(request, 'Error updating post. Please correct the errors below.')
            return redirect('update-post', pk=pk)
    else:
        form = fm.UpdatePostForm(instance=post)
        context = {'form': form, 'post': post}
    return render(request, 'post/update_post.html', context)


def post_details(request, pk):
    post = Post.objects.get(pk=pk)
    context = {'post': post}
    return render(request, 'post/post_details.html', context)


def author_posts(request,pk):
    user = User.objects.get(pk=pk)
    posts = Post.post_set.all()
    context = {'posts': posts, 'user': user}
    return render(request, 'post/author_posts.html', context)

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    context = {'posts': posts}
    return render(request, 'post/my_posts.html', context)


@login_required
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.author == request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('dashboard')
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('my-posts')


@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    post_like = PostLike.objects.filter(post=post).first()
    
    
    if post_like.exists():
        if post_like.reader == request.user:
            messages.success(request, 'You already liked this post!')
            return redirect('post-details',post.pk)
        post_like.like_count += 1
        post_like.save()
        messages.success(request, 'you just liked this post')
        return redirect('post-details', post.pk)
    else:
        PostLike.objects.create(reader=request.user, like_count=1, post=post)
        messages.success(request, 'you just liked this post')
        return redirect('post-details', post.pk)
    

def all_posts(request):
    posts = Post.objects.filter(is_draft=False, sheduled_date__gte=timezone.now().date()).order_by('-date_posted')
    context = {'posts': posts}
    return render(request, 'post/all_posts.html', context)