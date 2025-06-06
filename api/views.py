from django.shortcuts import get_object_or_404
from .serializers import EventSerializer , ArticleSerializer, JobPostSerializer, ALumniSerializer, RelatedALumniSerializer

from django.utils.timezone import now
from events.models import Event
from articles.models import Article
from careers.models import JobPost
from authentication.models import User
from .permissions import IsStaffUser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q
from django.db.models import Count

# Create your views here.
class FilteredEventsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        event_filter = request.GET.get('event_filter', 'all')
        month = request.GET.get('month')
        year = request.GET.get('year')
        is_active = request.GET.get('is_active', 'all')
        page_size = request.GET.get('page_size') or 10
        search_query = request.GET.get('q')

        events = Event.objects.all().annotate(like_count=Count('liked_by'))

        if search_query:
            events = events.filter(Q(title__icontains=search_query))

        if is_active.lower() in ['true', '1']:
            events = events.filter(is_active=True)
        elif is_active.lower() in ['false', '0']:
            events = events.filter(is_active=False)

        if event_filter == 'upcoming':
            events = events.filter(date__gte=now()).order_by('-date')
        elif event_filter == 'past':
            events = events.filter(date__lt=now()).order_by('-date')
        else:
            events = events.order_by('-date')
        
        if month and month != 0:
            events = events.filter(date__month=month)

        if year:
            events = events.filter(date__year=year)

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(result_page, many=True, context={"request": request})
        
        return paginator.get_paginated_response(serializer.data)
    

class FilteredArticlesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        article_filter = request.GET.get('article_filter', 'all')
        month = request.GET.get('month')
        year = request.GET.get('year')
        is_active = request.GET.get('is_active', 'all')
        page_size = request.GET.get('page_size') or 10
        search_query = request.GET.get('q')
        
        articles = Article.objects.all().annotate(like_count=Count('liked_by'))

        if search_query:
            articles = articles.filter(Q(title__icontains=search_query))

        if is_active.lower() in ['true', '1']:
            articles = articles.filter(is_active=True)
        elif is_active.lower() in ['false', '0']:
            articles = articles.filter(is_active=False)

        if article_filter == 'news':
            articles = articles.filter(category='news').order_by('-date')
        elif article_filter == 'Ann':
            articles = articles.filter(category='Ann').order_by('-date')
        else:
            articles = articles.order_by('-date')
        
        if month and month != 0:
            articles = articles.filter(date__month=month)

        if year:
            articles = articles.filter(date__year=year)

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(result_page, many=True, context={"request": request})
        
        return paginator.get_paginated_response(serializer.data)
    

@api_view(['GET'])
def get_user_info(request):
    """
    API View to get the user's first name and last name.
    """
    if request.user.is_authenticated:

        user = request.user

        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'suffix': user.suffix,
            'profile_image': user.profile_image.url if user.profile_image else None,
            'email': user.email,
            'student_number': user.student_number,
            'middle_name': user.middle_name,
            'birthday': user.birthday,
            'address': user.address,
            'telephone': user.telephone,
            'mobile': user.mobile,
            'civil_status': user.civil_status,
            'sex': user.sex,
            'events': user.events,
            'jobs': user.jobs,
            'work_experience': user.work_experience,
            'education': user.education,  # ✅ Add this line
            'licenses': user.licenses,
            'certifications': user.certifications,
            'course': {
                'id': user.course.id if user.course else None,
                'course_code': user.course.course_code if user.course else None,
                'course_name': user.course.course_name if user.course else None,
            },
            'section': {
                'id': user.section.id if user.section else None,
                'section_code': user.section.section_code if user.section else None,
            },
            'school_year': user.school_year,
        }

        return Response(user_info, status=200)
    else:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
class FilteredJobPostsAPIView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword', '')
        location = request.GET.get('location', '')
        job_type = request.GET.get('job_type', '')
        is_active = request.GET.get('is_active', 'all')
        page_size = request.GET.get('page_size') or 10
        search_query = request.GET.get('q')

        job_posts = JobPost.objects.all().annotate(like_count=Count('liked_by')).order_by('-created_at')
        
        if search_query:
            job_posts = job_posts.filter(Q(title__icontains=search_query))

        if is_active.lower() in ['true', '1']:
            job_posts = job_posts.filter(is_active=True)
        elif is_active.lower() in ['false', '0']:
            job_posts = job_posts.filter(is_active=False)

        #search by keyword and location
        if keyword:
            job_posts = job_posts.filter(Q(title__icontains=keyword)).order_by('-created_at')
        if location:
            job_posts = job_posts.filter(location__icontains=location).order_by('-created_at')

        #filter by jobtype
        if job_type:
            job_posts = job_posts.filter(job_type=job_type).order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(job_posts, request)
        serializer = JobPostSerializer(result_page, many=True, context={"request": request})
        
        
        return paginator.get_paginated_response(serializer.data)
    
class JobPostDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    lookup_field = 'id'
class EventsDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
class AlumniListView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, *args, **kwargs):

        users = User.objects.all().order_by("last_name", "first_name")

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)

        # Paginate queryset
        result_page = paginator.paginate_queryset(users, request)

        # Serialize paginated results
        serializer = ALumniSerializer(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    
class RelatedAlumniListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        course_code = request.GET.get('course_code', None)

        base_queryset = User.objects.exclude(Q(first_name="") | Q(last_name=""))

        if course_code:
            users = base_queryset.filter(course__course_code=course_code)\
                .select_related('course')\
                .order_by("?")
        else:
            users = base_queryset.select_related('course')\
            .order_by("?")

        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)

        result_page = paginator.paginate_queryset(users, request)
        serializer = RelatedALumniSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class ToggleLikeMixin(APIView):
    permission_classes = [IsAuthenticated]
    model = None

    def post(self, request, pk):
        obj   = get_object_or_404(self.model, pk=pk)
        user  = request.user

        if obj.liked_by.filter(pk=user.pk).exists():
            obj.liked_by.remove(user)
            liked = False
        else:
            obj.liked_by.add(user)
            liked = True

        return Response({
            "liked":       liked,
            "like_count":  obj.liked_by.count()
        })
    
class ToggleArticleLikeAPIView(ToggleLikeMixin):
    model = Article

class ToggleEventLikeAPIView(ToggleLikeMixin):
    model = Event

class ToggleJobLikeAPIView(ToggleLikeMixin):
    model = JobPost
