from django.urls import path

from apps.users.views import UserListCreateView, UserBlockView, UserUnBlockView, UserToSellerView, UserToStaffView, UserToSuperuserView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('/<int:pk>/block', UserBlockView.as_view()),
    path('/<int:pk>/unblock', UserUnBlockView.as_view()),
    path('/<int:pk>/seller', UserToSellerView.as_view()),
    path('/<int:pk>/staff', UserToStaffView.as_view()),
    path('/<int:pk>/superuser', UserToSuperuserView.as_view())
]