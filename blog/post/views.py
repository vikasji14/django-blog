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
    post_like= post.postlike_set.all().count()  
    is_liked = False
    if PostLike.objects.filter(post=post,  reader=request.user).exists():
        is_liked = True
    related_posts = Post.objects.order_by('?')[:5]
    context = {'post': post,'post_like': post_like,'is_liked': is_liked,'related_posts':related_posts }
    return render(request, 'post/post_details.html', context)


def author_posts(request,pk):
    user = User.objects.get(pk=pk)
    author_name = user.first_name
    posts = user.post_set.all()
    if not posts:
        messages.info(request, 'This author has no posts.')
        return redirect('all-posts')
    context = {'posts': posts, 'user': user, 'author_name': author_name}
    print("posts",posts)
    return render(request, 'post/author_posts.html', context)

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    context = {'posts': posts}
    return render(request, 'post/my_posts.html', context)


@login_required
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('my-posts')  # Redirect to your posts list
    return redirect('my-posts')


@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    
    if PostLike.objects.filter(post=post,  reader=request.user).exists():
        messages.warning(request, 'You already liked this post!')
        return redirect('post-details',post.pk)

    PostLike.objects.create(reader=request.user, post=post)
    messages.success(request, 'Post liked successfully!')
    return redirect('post-details', post.pk)
       
    

def all_posts(request):
    posts = Post.objects.filter(is_draft=True, sheduled_date__gte=timezone.now().date()).order_by('-date_posted')
    print("posts",posts)
    context = {'posts': posts}
    return render(request, 'post/all_posts.html', context)


def posts_per_category(request,pk):
    category = Category.objects.get(pk=pk)
    posts = category.post_set.all()
    context = {'posts':posts, 'category':category}
    return render(request, 'post/posts_per_category.html', context)


def search_post(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query)
    context={'query':query,'results':results}
    return render(request, 'post/search_posts.html', context)