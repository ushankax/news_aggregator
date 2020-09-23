from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        """define permissions for list of users"""
        if self.request.user.is_anonymous:
            queryset = User.objects.none()
        elif self.request.user.is_superuser:
            queryset = User.objects.all()
        elif self.request.user.is_authenticated:
            queryset = User.objects.filter(pk=self.request.user.pk)

        serializer = UserSerializer(queryset,
                                    context={'request': request},
                                    many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        define permissions for detail user view
        (users can only edit their own profiles)
        """
        content = {'status': 'request was permitted'}

        if self.request.user.is_anonymous:
            queryset = User.objects.none()
            return Response(content)
        elif self.request.user.is_superuser:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        elif self.request.user.is_authenticated:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            if user.pk == self.request.user.pk:
                serializer = UserSerializer(user, context={'request': request})
                return Response(serializer.data)
            else:
                return Response(content)
