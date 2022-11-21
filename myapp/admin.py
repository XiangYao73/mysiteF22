from django.contrib import admin
from myapp.models import Product, Category, Client, Order


def add_stock(modeladmin, request, queryset):
    queryset.update(available=True)
    for obj in queryset:
        obj.stock += 50
        obj.save()
#    add_stock.short_description = "Update available status and add 50 in stock"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'available')
    actions = [add_stock]


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)