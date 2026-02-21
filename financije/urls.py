from django.urls import path
from .views import (
    TransactionListView, TransactionDetailView,
    TransactionCreateView, TransactionUpdateView, TransactionDeleteView,
    AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    register,
)

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_list"),
    path("transaction/<int:pk>/", TransactionDetailView.as_view(), name="transaction_detail"),
    path("transaction/new/", TransactionCreateView.as_view(), name="transaction_create"),
    path("transaction/<int:pk>/edit/", TransactionUpdateView.as_view(), name="transaction_update"),
    path("transaction/<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),

    path("accounts/", AccountListView.as_view(), name="account_list"),
    path("accounts/new/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/<int:pk>/edit/", AccountUpdateView.as_view(), name="account_update"),
    path("accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),

    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/new/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),

    path("register/", register, name="register"),
]