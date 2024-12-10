from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
import json
import qrcode
from django.urls import reverse
import datetime
from .models import *
from .models import Product
from rest_framework.decorators import api_view
# import requests
# import threading
from io import BytesIO
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
# from PIL import Image
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render
from django.http import Http404


aaa = []
status = False
def checkout_view(request):
    random_number = random.randint(1, 10000)
    return render(request, 'cart.html', {'random_number': random_number})

context = {}
status_checkout= False
def delete_item(request):
    global status, context
    product_id = request.GET.get('id')
    print("Deleting product ID:", product_id)
    global aaa
    try:
        for item in aaa:
            if item['id'] == product_id:
                aaa.remove(item)
    except Exception as e:
        print(e)
    
    total_bill = sum(item['total'] for item in aaa)
    request.session['total_bill'] = total_bill
    print("Updated cart:", aaa)
    print("Total bill:", total_bill)
    status = True
    context = {'lists': aaa, 'total_bill':total_bill}
    return render(request, 'store/cart.html', context)

def cart(request):
	global context, status, status_checkout
	if not status:
		context = {}
	status_checkout = False
	
	return render(request, 'store/cart.html', context)

def checkout(request):
    total_bill = request.session.get('total_bill')
    print(total_bill)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    global status_checkout
    status_checkout =True
    qr.add_data(str(total_bill))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render(request, 'store/checkout.html',{'qr_code':img_str,'total_bill': total_bill}) 

aaa = []
status_checkout = False
def my_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    print("request", request)

    product_id = request.GET.get('id')
    loadcell_value = request.GET.get('loadcellValue')

    if not product_id or not loadcell_value:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    global status, context, aaa, status_checkout

    if status_checkout:
        context = {}
        aaa = []
        return JsonResponse({'message': 'Checkout in progress'}, status=409)

    try:
        product = get_object_or_404(Product, ID=product_id)

        data = {
            "id": product_id,
            "image": product.image,
            "name": product.name,
            "price": product.price,
            "loadcell_value": float(loadcell_value),
            "total": product.price * float(loadcell_value)
        }

        aaa.append(data)
        total_bill = sum(item['total'] for item in aaa)
        request.session['total_bill'] = total_bill

        status = True
        context = {'lists': aaa, 'total_bill': total_bill}

        return JsonResponse({
            'success': True,
            'message': 'Product added successfully',
            'data': data,
            'total_bill': total_bill
        })

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Invalid loadcell value'}, status=400)
def success(request):
	global status
	status = False
	return render(request, 'store/payment_success.html' )


