from rest_framework.pagination import CursorPagination as BaseLimitPagination

class DefaultPagination(
    BaseLimitPagination
):
    ordering = ['-created_at']