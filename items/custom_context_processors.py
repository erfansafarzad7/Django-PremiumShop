from items.models import Category, Item


def home(request):
    return {
        'categories': Category.objects.all(),
        'new_items': Item.objects.all().order_by('-created_date')[:10],
        'special_items': Item.objects.filter(discount__range=(40, 99))
    }
