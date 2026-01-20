from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import BlogPost
import json

@csrf_exempt
def posts_list(request):

    # GET → Listar posts
    if request.method == "GET":
        posts = BlogPost.objects.all().values()
        return JsonResponse(list(posts), safe=False)

    # POST → Crear un post
    if request.method == "POST":

        # Manejo seguro del JSON
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        # VALIDACIÓN DE DATOS SIMPLE
        if "title" not in data or not data["title"].strip():
            return JsonResponse({"error": "El título es obligatorio"}, status=400)

        if "content" not in data or not data["content"].strip():
            return JsonResponse({"error": "El contenido es obligatorio"}, status=400)

        # Crear el post
        post = BlogPost.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            author=data.get("author", "Desconocido")
        )

        return JsonResponse({"message": "Post creado", "id": post.id}, status=201)



@csrf_exempt
def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)

    # GET → Obtener un post
    if request.method == "GET":
        return JsonResponse({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "date_posted": post.date_posted,
            "published": post.published,
        })

    # PUT/PATCH → Actualizar el post
    if request.method in ["PUT", "PATCH"]:

        # Manejo seguro del JSON
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        # Actualizar campos
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.author = data.get("author", post.author)
        post.published = data.get("published", post.published)

        post.save()
        return JsonResponse({"message": "Post actualizado"})

    # DELETE → Eliminar el post
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post eliminado"})