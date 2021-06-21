#=====================================================================
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import product,contect_form,orders,order_update,Review,Comment
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from math import ceil
from django.contrib import messages

# <-
from django.core.mail import EmailMessage
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string
# from django.core.validators import email_re
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Rating
from django.template import loader
from django.urls import reverse
from .forms import RateForm,CommentForm
from django.db.models import Avg




import json
import re


# #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create your views here.
#=============================================================================
def home(request):
    return render(request, 'shop/base.html')

#-----------------------------------------------------------------------------------------


#=============================================================================
def about(request):
    # return HttpResponse("about SHOP")
     return render(request, 'shop/BASIC_about page.html')

#-----------------------------------------------------------------------------------------


#=============================================================================
def index(request):
    products= product.objects.all()
    allProds=[]
    catprods= product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
        params={'allProds':allProds }
    return render(request,"shop/index.html", params)

#-----------------------------------------------------------------------------------------


#=============================================================================
def contect(request):
    # return HttpResponse("contect SHOP")
    thank = False
    if request.method == "POST":
         # print(request)
         name = request.POST.get('name', '')
         # print(name);
         email = request.POST.get('email', '')
         # print(email);
         phone = request.POST.get('phone', '')
         # print(phone);
         desc = request.POST.get('desc', '')
         # print(desc);
         shop_contect = contect_form(c_name=name, c_email=email, c_phone=phone, c_descri=desc)
         shop_contect.save()
         thank = True
    return render(request, 'shop/BASIC_contect_us page.html', {'thank':thank})

#-----------------------------------------------------------------------------------------


#=============================================================================
def track(request):
        if request.method == "POST":
            orderId = request.POST.get('orderId', '')
            email = request.POST.get('email', '')
            try:
                order = orders.objects.filter(order_id=orderId, order_email=email)
                if len(order) > 0:
                    update = order_update.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        # response = json.dumps([updates,order[0].order_items_json], default=str)
                        response = json.dumps(
                            {"status": "success", "updates": updates, "itemsJson": order[0].order_items_json},
                            default=str)
                    return HttpResponse(response)
                else:
                    # return HttpResponse('{}')
                    return HttpResponse('{"status":"noitem"}')
            except Exception as e:
                # return HttpResponse('{}')
                return HttpResponse('{"status":"error"}')

        return render(request, 'shop/BASIC_track page.html')

#-----------------------------------------------------------------------------------------

#=============================================================================
def cheakout(request):
    # return HttpResponse("cheakout SHOP")
        if request.method == "POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            amount = request.POST.get('amount', '0000')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')
            order_shop = orders(order_items_json=items_json, order_name=name,
                                order_email=email, order_address=address, order_city=city,
                                order_state=state,order_zip_code=zip_code, order_phone=phone,amount=amount)
            order_shop.save()
            update = order_update(order_id=order_shop.order_id, update_desc="The order has been placed")
            update.save()
            # ----------------------------------------------
            send_mail('New Order Place',
                      'Order Details:\n'+
                      'Customer:'+ name +'\n'+
                      'Customer_ContectNo:' + phone + '\n'+
                      'Order-Items:'+ items_json +'\n'+
                      'Customer_Address:' + address + '\n'+
                      'Customer_city:' + city + '\n' +
                      'Customer_state:' + state + '\n'+
                      'Order_Total_amount:' + amount+ '\n',
                      # message.attach('design.png', img_data, 'image/png')
                      settings.EMAIL_HOST_USER,
                      [settings.EMAIL_HOST_USER],
                      fail_silently = False)

            # message1 = (
            #             'mass-Subject here',
            #             'Here is the message',
            #             settings.EMAIL_HOST_USER,
            #             [ settings.EMAIL_HOST_USER])
            # message2 = ('mass-Another Subject',
            #             'Here is another message',
            #              settings.EMAIL_HOST_USER,
            #             [ settings.EMAIL_HOST_USER])
            # send_mass_mail((message1, message2), fail_silently=False)


            # -------------------------------------------
            thank = True
            id = order_shop.order_id
            return render(request, 'shop/BASIC_checkout form.html', {'thank': thank, 'id': id})
        return render(request, 'shop/BASIC_checkout form.html')

#-----------------------------------------------------------------------------------------

#=============================================================================
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # check for errorneous input
        if len(username) < 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('shophome')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('shophome')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('shophome')
            # ___________________________________________________________
            # Make a regular expression
            # for validating an Email
        if (re.search(regex, email)):
                print("Valid Email")
        else:
            messages.error(request, " Invalid Email")
            return redirect('shophome')
        if User.objects.filter(username=username).exists():
            messages.error(request, " User name is not unique ")
        if User.objects.filter(email=email).exists():
            messages.error(request, " Email is not unique ")
            return redirect('shophome')
            # ---------------------------------------------------------------
            # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        # -----------------------------------------------------------------------
        # myuser.is_active = True
        myuser.save()
        # template = render_to_string('shop/email.html',{'name':myuser.first_name})
        email_sbj='Active Your Account'
        email_body='This Is Activation Email'
        email = EmailMessage(
            email_sbj,
            email_body,
            'noreply@ecom.com',
            [email],
        )
        email.send(fail_silently=False)
        # -----------------------------------------------------------------------
        messages.success(request, " Your E-COM has been successfully created")
        return redirect('shophome')

    else:
        return HttpResponse("404 - Not found")

#-----------------------------------------------------------------------------------------

#=============================================================================
def handeLogin(request):
    # if "user_id" in request.COOKIES:
    #     uid = request.COOKIES["user_id"]
    #     usr = get_object_or_404(User, id=uid)
    #     login(request, usr)
    #     if usr.is_superuser:
    #         return HttpResponseRedirect("/admin")
    #     if usr.is_active:
    #         return HttpResponseRedirect("shophome")
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("shophome")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("shophome")

    return HttpResponse("404- Not found")

#-----------------------------------------------------------------------------------------

#=============================================================================
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('shophome')

#-----------------------------------------------------------------------------------------

#=============================================================================
def search(request):
        query = request.GET['query']
        if len(query) > 78:
            allPosts = product.objects.none()
        else:
            allPostsTitle = product.objects.filter(category__icontains=query)
            allPostsAuthor = product.objects.filter(product_name__icontains=query)
            allPostsContent = product.objects.filter(product_descri__icontains=query)
            allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
        if allPosts.count() == 0:
            messages.warning(request, "No search results found. Please refine your query.")
        params = {'allPosts': allPosts, 'query': query}
        return render(request, 'shop/search_page.html', params)

#-----------------------------------------------------------------------------------------

#=============================================================================
def ReviewDetail(request, username, prod_id):
	user_comment = request.user
	user = get_object_or_404(User, username = username)
	r_product = product.objects.get(id = prod_id)
	review = Review.objects.get(user = user,product = r_product)

	#Comment stuff:
	comments = Comment.objects.filter(review = review).order_by('date')

	#Comment Form stuff:
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.review = review
			comment.user = user_comment
			comment.save()
			return HttpResponseRedirect(reverse('products', args=[username, prod_id]))
	else:
		form = CommentForm()
	context = {
		'review': review,
		'product': product,
		'comments': comments,
		'form': form,
	}

	template = loader.get_template('shop/prod_review.html')
	return HttpResponse(template.render(context, request))

#-----------------------------------------------------------------------------------------

#=============================================================================
def product_fn(request,myid):
    # return HttpResponse("product SHOP")
    #   #Fetch the product using the id
    products = product.objects.filter(id = myid)
    reviews = Review.objects.filter(product__in = products)
    reviews_avg = reviews.aggregate(Avg('rate'))
    reviews_count = reviews.count()
    # ,{'products':products[0]}
    context = {
        'for_rate_products': products,
        'reviews': reviews,
        # 'product_data': products,
        'reviews_avg': reviews_avg,
        'reviews_count': reviews_count,
        # 'our_db': our_db,
    }
    template = loader.get_template('shop/BASIC_product page.html')
    return HttpResponse(template.render(context, request))
    # params = {'for_rate_products': products,'reviews': reviews}
    # return render(request, 'shop/BASIC_product page.html',params)
    #

#-----------------------------------------------------------------------------------------

#=============================================================================
def Rate(request, prod_id):
	prod = product.objects.get(id = prod_id)
	login_user = request.user
	if request.method == 'POST':
		form = RateForm(request.POST)
		if form.is_valid():
			rate = form.save(commit = False)
			rate.review_user = login_user
			rate.product = prod
			rate.save()
			return HttpResponseRedirect(reverse('products', args=[prod_id]))
	else:
		form = RateForm()

	template = loader.get_template('shop/prod_rate.html')

	context = {
		'form': form,
		'product': prod,
	}

	return HttpResponse(template.render(context, request))

#-----------------------------------------------------------------------------------------

#==============================================================================
def category(request, catid):
    # data = (request.GET).dict()
    # message = request.GET.get('message')
    data = catid
    print(data)
    if len(data) > 20:
        allPosts = product.objects.none()
        # return HttpResponse("about ")
    else:
        # allPostsTitle = product.objects.filter(product_name__icontains=data)
        allPostcategory = product.objects.filter(category__icontains=data)
        # allPostsContent = product.objects.filter(product_descri__icontains=data)
        # allPosts = allPostsTitle.union( allPostcategory)
        allPosts = allPostcategory
    if allPosts.count() == 0:
        messages.warning(request, "Sorry No Product .")
    params = {'allPosts': allPosts, 'query': data}
    return render(request, 'shop/category_page.html', params)
    return HttpResponse("about SHOP")

#---------------------------------------------------------------------------------------------