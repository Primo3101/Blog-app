from django.shortcuts import render,redirect
from blog_app.models import Post
from blog_app.forms import PostForm

from django.contrib.auth.decorators import login_required
from django.utils import timezone


def post_list(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    return render (
        request,
        "post_list.html",
        {"posts": posts}, # context
     )


def view_more(request, id):
    if request.method == "GET":
        post = Post.objects.get(id=id)
        return render(request,
                    "view_more.html",
                    {"post": post}
                )
    

def post_details(request,pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        "post_details.html",
        {"post" : post}
    )

@login_required
def draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True)
    return render(
        request,
        "draft_list.html",
        {"posts": posts },
    )

@login_required
def draft_detail(request,pk):
    draft = Post.objects.get(pk=pk, published_at__isnull=True)
    return render(
        request,
        "draft_detail.html",
        {"post": draft},
    )
@login_required
def post_create(request):
    if request.method == "GET":
        form = PostForm()
        return render(
            request,
            "post_create.html",
            {"form":form},

    )
    else:
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # logged in user will be the author
            post.save()
            return redirect ("draft-list")
        else:
            return render(
                request,
                "post_create.html",
                {"form": form},
            )

@login_required
def post_update(request,pk):
    if request.method == "GET":
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(
            request,
            "post_create.html",
            {"form" :form},
        )
    else:
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post= form.save()
            if post.published_at:
                return redirect("post-detail",post.pk)
            else:
                return redirect("draft-detail",post.pk)
        else:
            return render(
                request,
                "post_create.html",
                {"form":form},
            )

@login_required
def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    if post.published_at:
        return redirect("post_list")
    else:
        return redirect("draft-list")
    
@login_required
def draft_publish(request,pk):
    post = Post.objects.get(pk=pk, published_at__isnull=True) 
    post.published_at = timezone.now()
    post.save()
    return redirect("post-list")