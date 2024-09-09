from django.urls import path

from apps.advertisement.views import AdvertisementCreateListView,AdvertisementAddPhotoView, AdvertisementListView, AdvertisementRetrieveUpdateDestroyView

urlpatterns = [
    path('', AdvertisementListView.as_view()),
    path('/create', AdvertisementCreateListView.as_view()),
    path('/<int:pk>', AdvertisementRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/photo', AdvertisementAddPhotoView.as_view())
]