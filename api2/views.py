from collections import OrderedDict

from django.contrib.auth.models import User

# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api2.serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer, CateTagSerializer, \
    PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer

# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostRetrieveSerializer

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
#
# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer
#
#     #필요 기능이 없을 때 overriding
#     #PATCH method 활용
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = {'like':instance.like + 1}
#         serializer = self.get_serializer(instance, data= data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response(data['like'])

class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()
    #serializer_class = PostLikeSerializer

    #필요 기능이 없을 때 overriding
    #Get method
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()

        data = {
            'cateList': cateList,
            'tagList': tagList,
        }

        serializer = CateTagSerializer(instance = data)
        return Response(serializer.data)

class PostPageNumberPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page_size'
    # max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number)
        ]))


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    # fields.py 에서 class FileField(Field) 내에 Url Generate 하는 부분이 to_representation().
    # 여기서 serializer의 context의 request 부분이 None이면 그냥 url 반환
    # 따라서 Serializer에서 context를 return 하는 부분을 None으로 리턴하도록 overriding 하여 수정
    #-> 해당 함수는 ListAPIVIEW->GenericAPIView->get_serializer_context 함수임
    # def to_representation(self, value):
    #     if not value:
    #         return None
    #
    #     use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
    #     if use_url:
    #         try:
    #             url = value.url
    #         except AttributeError:
    #             return None
    #         request = self.context.get('request', None)
    #         if request is not None:
    #             return request.build_absolute_uri(url)
    #         return url


    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,# self.request,
            'format': self.format_kwarg,
            'view': self
        }
#instance.get_previous_by_update_dt() 사용할 경우 다음 객체 없을 때 doesnotexist 에러. -> exception 처리 필요
#https://docs.djangoproject.com/en/4.1/ref/models/instances/ 확인 필요
def get_prev_next(instance):
    try :
        prev = instance.get_previous_by_update_dt()
    except instance.DoesNotExist:
        prev = None
    try:
        next_ = instance.get_next_by_update_dt()
    except instance.DoesNotExist:
        next_ = None
    return prev, next_




class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # prevInstance = instance.get_previous_by_update_dt()
        # nextInstance = instance.get_next_by_update_dt()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()
        data = {
            'post' : instance,
            'prevPost' : prevInstance,
            'nextPost' : nextInstance,
            'commentList' : commentList,

        }
        serializer = self.get_serializer(instance= data)
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,# self.request,
            'format': self.format_kwarg,
            'view': self
        }



###viewset 활용시 - Overiding 할 함수 코드 다 가져옴
# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     pagination_class = PostPageNumberPagination
#
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             'request': None,# self.request,
#             'format': self.format_kwarg,
#             'view': self
#         }
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         # prevInstance = instance.get_previous_by_update_dt()
#         # nextInstance = instance.get_next_by_update_dt()
#         prevInstance, nextInstance = get_prev_next(instance)
#         commentList = instance.comment_set.all()
#         data = {
#             'post' : instance,
#             'prevPost' : prevInstance,
#             'nextPost' : nextInstance,
#             'commentList' : commentList,
#
#         }
#         serializer = self.get_serializer(instance= data)
#         return Response(serializer.data)
#
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             'request': None,# self.request,
#             'format': self.format_kwarg,
#             'view': self
#         }
#
#     def like(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.like += 1
#         instance.save()
#
#         return Response(instance.like)
