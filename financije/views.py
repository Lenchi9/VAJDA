from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Transaction


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
        # spriječi da user vidi tuđu transakciju preko /transaction/<pk>/
        return Transaction.objects.filter(user=self.request.user)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "financije/transaction_form.html"
    fields = ["account", "category", "datum", "iznos", "opis"]
    success_url = reverse_lazy("transaction_list")

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


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "financije/transaction_confirm_delete.html"
    success_url = reverse_lazy("transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)