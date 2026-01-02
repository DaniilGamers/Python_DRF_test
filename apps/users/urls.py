from django.urls import path

from apps.users.views import UserListCreateView, UserBlockView, UserUnBlockView, BuyPremiumView, UserDeleteView, UserToClientView, UserToSellerView, UserStaffCreateView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('/<int:pk>/block', UserBlockView.as_view()),
    path('/<int:pk>/unblock', UserUnBlockView.as_view()),

    path('/createManager', UserStaffCreateView.as_view()),

    path('/<int:pk>/client', UserToClientView.as_view()),

    path('/<int:pk>/seller', UserToSellerView.as_view()),

    path('/<int:pk>/delete', UserDeleteView.as_view()),

    path('/buy_premium', BuyPremiumView.as_view())
]
