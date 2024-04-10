from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('create/', views.CreateBlogView.as_view(), name='Create-Blog'),
    path('list/',views.BlogListView.as_view(), name='ListAll-Blogs'),
    path('<str:id>/', views.BlogDetailView.as_view(), name='Single-Blog-Details'),
    path('list/author/', views.CurrentUserBlogListView.as_view(), name='Current_user_BlogListView'),
    path('update/<str:id>/', views.UpdateBlogView.as_view(), name='Update-Blog'),
    path('delete/<str:id>/', views.DeleteBlogView.as_view(), name='Delete-Blog'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)