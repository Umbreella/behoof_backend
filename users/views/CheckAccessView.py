from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class CheckAccessView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Serializer

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)
