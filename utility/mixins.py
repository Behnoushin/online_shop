class SoftDeleteMixin:
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
