import json as json
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import *
from rest_framework.filters import SearchFilter, OrderingFilter
# from url_filter.integrations.drf import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend

from .models import *


class BaseModelViewSet(ModelViewSet):
    """BaseModelViewSet

    By default has all fields enabled for filtering, searching and ordering
    Pagination enabled

    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination

    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        self.setup_viewset()
        super().__init__(**kwargs)

    def setup_viewset(self):
        all_model_fields = self.queryset.model.get_all_fields()
        self.filter_fields = all_model_fields
        self.search_fields = self.queryset.model.get_all_search_fields()
        self.ordering_fields = all_model_fields
        self.pagination_class.page_size = 100
        self.queryset = self.queryset.order_by("-created_on")
