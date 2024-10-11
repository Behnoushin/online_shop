from rest_framework import generics

class BaseAPIView(generics.GenericAPIView):
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False)

    def get_serializer_class(self):
        raise NotImplementedError

