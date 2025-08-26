from rest_framework  import generics,permissions
from .serializers import PostSerializer,PostListSerializer
from rest_framework.views import APIView
from blog_app.models import Post 
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class PostListAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostListCreateAPI(generics.ListCreateAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(published_at__isnull=False).order_by("-published_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostUpdateAPI(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
class PostDeleteAPI(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class DraftListAPI(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, published_at__isnull=True).order_by("-created_at")

class DraftDetailAPI(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, published_at__isnull=True)

class DraftPublishAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request, pk):
        try:
            # Get the draft post that is not yet published
            post = Post.objects.get(pk=pk, published_at__isnull=True)
        except Post.DoesNotExist:
            return Response(
                {"error": "Draft not found or already published."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Ensure only the author can publish their draft
        if post.author != request.user:
            return Response(
                {"error": "You are not allowed to publish this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Publish the draft
        post.published_at = timezone.now()
        post.save()

        return Response(
            {"message": "Post published successfully!"},
            status=status.HTTP_200_OK
        )