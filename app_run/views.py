from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from django.db.models import Count, Q
from django.conf import settings
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RunSerializer, UserSerializer, AthleteInfoSerializer
from .models import Run, User, AthleteInfo



@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(details)



class BasePagination(PageNumberPagination):
    page_size_query_param = 'size'



class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all().select_related('athlete')
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = BasePagination



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.annotate(runs_finished=Count('runs', filter=Q(runs__status='finished')))
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = BasePagination

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            qs = qs.filter(is_staff=True, is_superuser=False)
        elif type == 'athlete':
            qs = qs.filter(is_staff=False, is_superuser=False)
        else:
            qs = qs.filter(is_superuser=False)
        return qs



class StartAPIView(APIView):
    serializer_class = RunSerializer

    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == Run.Status.INIT:
            run.status = Run.Status.IN_PROGRESS
            run.save()
            serializer = self.serializer_class(run)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class StopAPIView(APIView):
    serializer_class = RunSerializer

    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status == Run.Status.IN_PROGRESS:
            run.status = Run.Status.FINISHED
            run.save()
            serializer = self.serializer_class(run)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AthleteInfoAPIView(APIView):
    serializer_class = AthleteInfoSerializer

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        athlete, created = AthleteInfo.objects.get_or_create(user=user, defaults={'goals': '', 'weight': 0})
        serializer = self.serializer_class(athlete)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        athlete, created = AthleteInfo.objects.update_or_create(user=user, defaults=serializer.validated_data)
        response_serializer = self.serializer_class(athlete)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return Response(data=response_serializer.data, status=status_code)