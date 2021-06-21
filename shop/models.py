from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
        # product_id=models.AutoField()
        product_id = models.AutoField
        product_name = models.CharField(max_length=50)
        category = models.CharField(max_length=50, default="")
        sub_category = models.CharField(max_length=50, default="")
        price = models.IntegerField(default=0)
        product_descri  = models.TextField(max_length=800)
        product_rating = models.CharField(max_length=5, default="5")
        product_brand = models.CharField(max_length=50, default="unKnown")
        product_status = models.CharField(max_length=50, default="Avaliable")
        product_date  = models.DateField()
        image = models.ImageField(upload_to="A_shop/images", default="")
        # stock_quantity = models.PositiveIntegerField()
        # on_sale = models.BooleanField(default=False)
        def __str__(self):
            return self.product_name



class contect_form(models.Model):
        contect_id=models.AutoField(primary_key=True)
        c_name = models.CharField(max_length=80,default="")
        c_email = models.CharField(max_length=80,default="")
        c_phone = models.CharField(max_length=80, default="")
        c_descri  = models.CharField(max_length=500,default="")
        # product_date  = models.DateField()
        def __str__(self):
            return self.c_name



class orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    order_items_json= models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    order_name=models.CharField(max_length=90)
    order_email=models.CharField(max_length=111)
    order_address=models.CharField(max_length=111)
    order_city=models.CharField(max_length=111)
    order_state=models.CharField(max_length=111)
    order_zip_code=models.CharField(max_length=111)
    order_phone= models.CharField(max_length=111,default="")
    # status=models.BooleanField(default=False)


class order_update(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

#_____________________________________________________________________________________

# class User(models.Model):
#     username = models.CharField(max_length=30)
#     password = models.CharField(max_length=50)
#     def __str__(self):
#         return self.username





RATE_CHOICES = [
	(1, '1 - Trash'),
	# (2, '2 - Horrible'),
	# (3, '3 - Terrible'),
	# (4, '4 - Bad'),
	# (5, '5 - OK'),
	(2, '2 - Normal'),
	(3, '3 - Good'),
	(4, '4 - Very Good'),
	(5, '5 - Perfect'),
	# (10, '10 - Master Piece'),
]

class Review(models.Model):
	review_user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	product = models.ForeignKey(product,on_delete=models.CASCADE,default=None)
	date = models.DateTimeField(auto_now_add=True)
	title_text = models.TextField(max_length=50, blank=True)
	review_text = models.TextField(max_length=300, blank=True)
	rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
	likes = models.PositiveIntegerField(default=0)
	unlikes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.review_user.username


class Comment(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)