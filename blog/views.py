from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BlogPost
import json

def home(request):
    posts = BlogPost.objects.all().order_by("-date_posted")
    return render(request, "blog/home.html", {"posts": posts})

def article_det(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog/detail.html", {"post": post})

@csrf_exempt
def posts_list(request):
    if request.method == "GET":
        posts = BlogPost.objects.all().values()
        return JsonResponse(list(posts), safe=False)

    if request.method == "POST":
        data = json.loads(request.body)
        post = BlogPost.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author", "Desconocido"),
        )
        return JsonResponse({"message": "Post creado", "id": post.id})


@csrf_exempt
def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)

    if request.method == "GET":
        return JsonResponse({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "date_posted": post.date_posted,
            "published": post.published,
        })

    if request.method in ["PUT", "PATCH"]:
        data = json.loads(request.body)
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.author = data.get("author", post.author)
        post.published = data.get("published", post.published)
        post.save()
        return JsonResponse({"message": "Post actualizado"})

    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post eliminado"})


@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Credenciales incorrectas"}, status=401)

        import secrets
        token = secrets.token_hex(16)

        return JsonResponse({"token": token})

def deploy_test(request):
    return JsonResponse({
        "status": "ok",
        "message": "Deploy automatico funcionando.",
    })