from rest_framework import generics
from . import serializers
from .models import Blog
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser


class CreateBlogView( generics.CreateAPIView):
    queryset= Blog.objects.all()
    serializer_class= serializers.CreateBlogSerializer
    permission_classes= [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(request_body=serializers.UpdateBlogSerializer)
    def post(self, request):
        
        request.data['author']= request.user.id

        return super().post(request)


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

        return Blog.objects.filter(user=self.request.user.id).order_by('-updated_at')

class UpdateBlogView( generics.UpdateAPIView):
    serializer_class= serializers.UpdateBlogSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field= 'id'
    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user.id)

class DeleteBlogView( generics.DestroyAPIView):
    serializer_class= serializers.UpdateBlogSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field= 'id'
    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user.id)
