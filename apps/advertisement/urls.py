from django.urls import path

from apps.advertisement.views import AdvertisementCreateListView,AdvertisementAddPhotoView, AdvertisementListView, AdvertisementRetrieveUpdateDestroyView, AdvertisementViewerView

urlpatterns = [
    path('', AdvertisementListView.as_view()),
    path('/create', AdvertisementCreateListView.as_view()),
    path('/<int:pk>', AdvertisementRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/photo', AdvertisementAddPhotoView.as_view()),

    path('/<int:pk>/view', AdvertisementViewerView.as_view()),

    path('/<int:pk>/ad_stats', AdvertisementRetrieveUpdateDestroyView.as_view()),

    path('/<int:pk>/edit_ad', AdvertisementRetrieveUpdateDestroyView.as_view())
]