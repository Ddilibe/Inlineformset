from django.urls import path

from .views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView

app_name = 'article'
urlpatterns = [
        path('', ArticleCreateView.as_view(), name="iamtrying"),
        path('house', ArticleListView.as_view(), name='Article_list'),
        path('<int:pk>/', ArticleDetailView.as_view(), name="Article"),
        path('<int:pk>/update', ArticleUpdateView.as_view(), name="update"),
]