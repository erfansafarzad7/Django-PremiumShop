from django.db.models import Q
from django.views.generic import ListView, FormView, DetailView, TemplateView
from .models import Item
from .forms import SearchForm


# self.kwargs.get('urls.py')
# self.request.GET.get('query parameter')


class HomeView(TemplateView):
    template_name = 'index.html'


class ItemsView(FormView, ListView):
    form_class = SearchForm
    model = Item
    template_name = 'items/all_items.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        items = Item.objects.all()
        if q := self.request.GET.get('q'):
            return items.filter(title__contains=q)
        return items


class CategoryFilterView(FormView, ListView):
    form_class = SearchForm
    model = Item
    template_name = 'items/all_items.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        title = self.kwargs.get('title')
        items = Item.objects.filter(category__title__contains=title)
        return items


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        item = Item.objects.get(title__exact=self.kwargs.get('title'))
        return item
