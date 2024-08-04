
from django.shortcuts import render,get_object_or_404,redirect
from .models import Category, Post, Author, Comment, Reply
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
#from .utils import update_views
from .forms import EntryForm,AuthorForm,ReplyForm,CommentForm#,UpAuthorForm
#from somewhere import handle_uploaded_file
#from .models import ModelWithFileField
# Create your views here.

def index(request):
    keyword = request.GET.get("keyword")

    if keyword:
        post = Post.objects.filter(title__contains = keyword)
        return render(request, 'index.html', {'post':post})



    post = Post.objects.all()
    return render(request, 'index.html', {'post':post})

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)


    context = {
        "post":post,
        "title": "OZONE: "+post.title,
    }
    #update_views(request, post)

    return render(request, "detail.html", context)
@login_required(login_url="user:login")
def addEntry(request):

    form = EntryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            print("\n\n its valid")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            #form.save_m2m()

            return redirect("index")
    return render(request, "addentry.html", {"form": form})
@login_required(login_url="user:login")
def addAuthor(request):

    form = AuthorForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            new_author = form.save(commit=False)
            if request.method == 'POST' and request.FILES['upload']:
                upload = request.FILES['upload']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
            new_author.user = request.user
            new_author.profile_pic = file_url
            new_author.save()
            #form.save_m2m()

            return redirect("index")
    return render(request, "addauthor.html", {"form": form})


@login_required(login_url="user:login")
def deletePost(request,slug):
    post = get_object_or_404(Post,slug = slug)
    post.delete()

    return redirect("index")
@login_required(login_url="user:login")
def dashboard(request):
    author = Author.objects.get(user=request.user)
    posts = Post.objects.filter(user = author)
    return render(request, "dashboard.html", {'posts':posts})

@login_required(login_url="user:login")
def editEntry(request,slug):
    post = get_object_or_404(Post,slug = slug)
    form = EntryForm(request.POST or None, request.FILES or None,instance=post)
    if form.is_valid():
            author = Author.objects.get(user=request.user)
            post = form.save(commit=False)
            post.user = author
            post.save()

            return redirect("index")
    return render(request, "edit.html", {"form": form})

def profile(request, slug):
    author = get_object_or_404(Author, slug=slug)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    context = {
        "fullname":fullname,

    }
    #update_views(request, post)

    return render(request, "profile.html", context)
