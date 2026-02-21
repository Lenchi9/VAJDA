from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Transaction, Account, Category


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "financije/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user).order_by("-datum", "-created_at")

        # (bonus) jednostavna pretraga po opisu
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(opis__icontains=q)
        return qs


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "financije/transaction_detail.html"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "financije/transaction_form.html"
    fields = ["account", "category", "datum", "iznos", "opis"]
    success_url = reverse_lazy("transaction_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["account"].queryset = form.fields["account"].queryset.filter(user=self.request.user)
        form.fields["category"].queryset = form.fields["category"].queryset.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = "financije/transaction_form.html"
    fields = ["account", "category", "datum", "iznos", "opis"]
    success_url = reverse_lazy("transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["account"].queryset = form.fields["account"].queryset.filter(user=self.request.user)
        form.fields["category"].queryset = form.fields["category"].queryset.filter(user=self.request.user)
        return form


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "financije/transaction_confirm_delete.html"
    success_url = reverse_lazy("transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "financije/account_list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("naziv")


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = "financije/account_form.html"
    fields = ["naziv", "tip", "pocetno_stanje"]
    success_url = reverse_lazy("account_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = "financije/account_form.html"
    fields = ["naziv", "tip", "pocetno_stanje"]
    success_url = reverse_lazy("account_list")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = "financije/account_confirm_delete.html"
    success_url = reverse_lazy("account_list")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "financije/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by("naziv")


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "financije/category_form.html"
    fields = ["naziv", "tip"]
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "financije/category_form.html"
    fields = ["naziv", "tip"]
    success_url = reverse_lazy("category_list")

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "financije/category_confirm_delete.html"
    success_url = reverse_lazy("category_list")

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)