from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post, User
from .permissions import AuthorChangeOrUserReadOnly
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorChangeOrUserReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AuthorChangeOrUserReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AuthorChangeOrUserReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(post=kwargs.get('post_id'))
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs.get('post_id'))
        print(request.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            following = User.objects.get(
                username=serializer.validated_data.get('following')
            )
            obj, result = Follow.objects.get_or_create(
                user=user,
                following=following
            )
            if user != following and result:
                serializer=FollowSerializer(obj)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )