# #Routers provide an easy way of automatically determining the URL conf.
#
# from django.urls import path, include
# from rest_framework import routers
#
# from api2.views import UserViewSet, PostViewSet, CommentViewSet
#
# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet) # router 까지 url 이 가려면 경로가 'api2/user/'
# router.register(r'post', PostViewSet) # router 까지 url 이 가려면 경로가 'api2/post/'
# router.register(r'comment', CommentViewSet) # router 까지 url 이 가려면 경로가 'api2/post/'


from django.urls import path

from api2 import views


#app_name = 'api'
urlpatterns = [
#     path('', include(router.urls)),
    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),
    path('comment/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('post/<int:pk>/like', views.PostLikeAPIView.as_view(), name='post-like'),
    path('catetag/', views.CateTagAPIView.as_view(), name='catetag'),

]


#viewset 활용시(router 활용 안한 경우)
# urlpatterns = [
# #     path('', include(router.urls)),
#     path('post/', views.PostViewSet.as_view(action={'get':'list}), name='post-list'),
#     path('post/<int:pk>/', views.PostViewSet.as_view(action={'get':'retrieve'}), name='post-detail'),
#     path('post/<int:pk>/like', views.PostViewSet.as_view(action={'get':'like'}), name='post-like')
#     path('comment/', views.CommentCreateAPIView.as_view(), name='comment-create'),
#     path('catetag/', views.CateTagAPIView.as_view(), name='catetag'),
#
# ]

