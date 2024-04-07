from rest_framework import serializers
from .models import Blog


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields= ['title', 'description','image','author']



class UpdateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model= Blog
        fields= ['title','description','image']


class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= Blog
        fields= '__all__'

