from rest_framework import generics

class BaseAPIView(generics.GenericAPIView):
    
    def get_queryset(self):
        raise NotImplementedError

    def get_serializer_class(self):
        raise NotImplementedError

