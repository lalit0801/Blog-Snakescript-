from rest_framework import generics
from . import serializers
from .models import Blog
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

class CreateBlogView( generics.CreateAPIView):
    queryset= Blog.objects.all()
    serializer_class= serializers.CreateBlogSerializer
    permission_classes= [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(request_body=serializers.UpdateBlogSerializer)
    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
       


class  BlogDetailView(generics.RetrieveAPIView):
    queryset= Blog.objects.all() 
    serializer_class= serializers.BlogDetailSerializer
    lookup_field= 'id'

class  BlogListView(generics.ListAPIView):
    serializer_class= serializers.BlogDetailSerializer
    def get_queryset(self):

        return Blog.objects.all().order_by('-updated_at')


class  CurrentUserBlogListView(generics.ListAPIView): 
    serializer_class= serializers.BlogDetailSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):

        return Blog.objects.filter(author=self.request.user.id).order_by('-updated_at')

class UpdateBlogView( generics.UpdateAPIView):
    serializer_class= serializers.UpdateBlogSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field= 'id'
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(request_body=serializers.UpdateBlogSerializer)
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user.id)

class DeleteBlogView( generics.DestroyAPIView):
    serializer_class= serializers.UpdateBlogSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field= 'id'
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user.id)
