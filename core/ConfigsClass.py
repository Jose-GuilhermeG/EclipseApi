from rest_framework.pagination import LimitOffsetPagination as BaseLimitPagination

class LimitOffsetPagination(
    BaseLimitPagination
):
    max_limit = 100