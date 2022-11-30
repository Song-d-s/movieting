from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:movie_id>/', views.detail),
    path('popular/', views.popular),
    path('random/', views.random),
    path('keyword/<int:keyword_id>/', views.keyword),
    path('<int:movie_id>/likes/',views.likes, name='likes'),
    path('<int:movie_id>/comments/',views.comment_create,),
    path('comments/<int:comment_id>/', views.comment_edit,),
    path('surveydone/', views.surveyPickDone,),
    # path('survey/', views.survey),
    path('test/', views.test, name='test'),
]