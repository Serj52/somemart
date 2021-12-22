from django.conf.urls import url
from .views import AddItemView, GetItemView, PostReviewView

urlpatterns = [
    url(r'api/v1/goods/$', AddItemView.as_view()),
    url(r'api/v1/goods/(?P<item_id>[0-9]+)/$', GetItemView.as_view()),
    url(r'api/v1/goods/(?P<item_id>[0-9]+)/reviews/$', PostReviewView.as_view()),
]
