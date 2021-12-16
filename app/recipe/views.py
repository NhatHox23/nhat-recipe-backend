from django.shortcuts import render

from rest_framework import generics, permissions, authentication

from rest_framework import status

from rest_framework.response import Response

from recipe.serializers import TagSerializer

from recipe.models import Tag


# Create your views here.

class TagListAPI(generics.ListAPIView):
    """List Tag API"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        tag = Tag.objects.filter(user=request.user).order_by('-name')
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
