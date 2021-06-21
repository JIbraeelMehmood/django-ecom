from django.contrib import admin

# Register your models here.

from .models import product,contect_form,orders,order_update,Review,Comment
admin.site.register(product)
admin.site.register(contect_form)
admin.site.register(orders)
admin.site.register(order_update)
admin.site.register(Review)
admin.site.register(Comment)
