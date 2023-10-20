from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer, TopicSerializer
from .models import Article, Comment, Topic
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
import json

# Create your views here.
@api_view(["GET", "POST"])
def article(request):
    if request.method == "GET":
        article = get_list_or_404(Article)
        serializer = ArticleListSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        topics_string = request.data.get('topics')
        topics_data = json.loads(topics_string)

        topics = []
        for topic in topics_data:
            # topic은 문자열
            topic_data = {"name": topic}
            topic_serializer = TopicSerializer(data=topic_data)
            # 존재하면 exist_topic 변수에 담긴다.
            exist_topic = Topic.objects.filter(name=topic).first()

            if exist_topic:
                # 관계 설정을 위해 비어있는 리스트에 추가.
                topics.append(exist_topic)
            else:
                # 없다면 생성
                if topic_serializer.is_valid(raise_exception=True):
                    topic_serializer.save()
                    # 생성한 인스턴스를 리스트에 추가
                    topics.append(topic_serializer.instance)

        serializer = ArticleListSerializer(data = request.data)
        if serializer.is_valid():
            article = serializer.save()

            # article - topics 관계 설정
            # set : 여러 개의 데이터를 한 번에 받아줌
            article.topics.set(topics)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    # 없는 데이터를 넣으면 오류난다!
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == "GET":
        # 조회수 추가 코드
        article.views += 1
        article.save()
        #
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    elif request.method == "PUT":
        # partial = 특정 필드만 입력받고 싶을 때
        serializer = ArticleSerializer(article, data = request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def comment_list(request, comment_pk):
    article = get_object_or_404(Article, pk=comment_pk)
    comments = article.comment_set.all()
    
    if request.method == 'GET':
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)