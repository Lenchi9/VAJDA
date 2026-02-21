from django.urls import path
from .views import (
    TransactionListView,
    TransactionDetailView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
    register,
)

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_list"),
    path("transaction/<int:pk>/", TransactionDetailView.as_view(), name="transaction_detail"),

    path("transaction/new/", TransactionCreateView.as_view(), name="transaction_create"),
    path("transaction/<int:pk>/edit/", TransactionUpdateView.as_view(), name="transaction_update"),
    path("transaction/<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),

    path("register/", register, name="register"),
]