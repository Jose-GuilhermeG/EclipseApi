#Imports
from django.urls import path , re_path
from rest_framework.routers import SimpleRouter
from product import views

router  = SimpleRouter()

router.register(
    prefix='product',
    viewset=views.ProductViewSet,
    basename='product'
)

router.register(
    prefix='category',
    viewset=views.CategoryViewSet,
    basename='category'
)

router.register(
    prefix=r'product/(?P<slug>[-\w]+)/evaluations',
    viewset=views.ProductEvaluationViewSet,
    basename='evaluations'
)

urlpatterns=router.urls

urlpatterns += [

    path(
        'product/feature/',
        views.ProductFeatureView.as_view(),
        name='product_feature'
    ),
    re_path(
        r'^product/search/(?P<query>[- \w]+)/$',
        views.ProductSearchView.as_view(),
        name='product_search'
    ),
    re_path(
        r'^product/(?P<slug>[-\w]+)/doubts/$',
        views.ProducDoubtListCreateView.as_view(),
        name="product_doubt_list"
    ),
    re_path(
        r'^product/(?P<slug>[-\w]+)/doubt/(?P<id>[\w]+)/$',
        views.ProductDoubtUpdateDeleteView.as_view(),
        name="product_doubt_edit"
    ),
]
