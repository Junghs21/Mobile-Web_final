from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from rest_framework import viewsets
from .serializers import PostSerializer
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.views import APIView




# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


class DeletePostAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        title = request.GET.get('title', None)  # URL에서 title 가져오기
        if not title:
            return JsonResponse({"error": "Title parameter is required"}, status=400)

        try:
            post = Post.objects.get(title=title)  # title로 Post 검색
            post.delete()  # Post 삭제
            return JsonResponse({"success": "Image deleted successfully"}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Image with the given title does not exist"}, status=404)


class blogImage(viewsets.ModelViewSet):
     queryset = Post.objects.all()
     serializer_class = PostSerializer


class PostTitleImageAPIView(APIView):
    """
    모든 게시글의 타이틀과 이미지 URL만 반환하는 APIView
    """
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().values("title", "image")  # 타이틀과 이미지 URL만 가져오기
        return JsonResponse(list(posts), safe=False, status=200)
