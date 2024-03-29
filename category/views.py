from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from category.models import Category,Sub_Category
from products.models import Product,ProductVariant
from django.contrib import messages


# Create your views here.
def showcategoryproduct(request, cat_id):
    sub_cat=Sub_Category.objects.all()
    products_with_default_variants=Product.objects.filter(category=cat_id).prefetch_related('variants')
    product_queryset = ProductVariant.objects.none()
    for product in products_with_default_variants:
        default_variant=product.variants.filter(is_available=True).first()
        if default_variant:
            product_queryset |=ProductVariant.objects.filter(pk=default_variant.pk)
    paginator = Paginator(product_queryset, 8)
    page_number = request.GET.get('page', 1)
    product_queryset = paginator.get_page(page_number)
    context={
        'cat_products':product_queryset,
        'sub_category':sub_cat,
    }
    return render(request,'products/shop.html',context)

# <---------------------------------------------------Start Sub-Category------------------------------------------------->
# <-------------------View Sub-Category-------------------------->
def viewsubcategory(request):
    cat = Category.objects.filter(is_visible=True)
    sub_cat = Sub_Category.objects.all().order_by('id')
    paginator = Paginator(sub_cat, 3)
    page_number = request.GET.get('page', 1)
    sub_cat = paginator.get_page(page_number)
    context = {
        'categories': cat,
        'sub_cat': sub_cat
    }
    
    return render(request,'admin/viewsubcat.html',context)
# <-------------------View Sub-Category-------------------------->
# <-------------------listunlist Sub-Category-------------------------->

def subunlist(request, subcat_id):
    cat = Sub_Category.objects.get(id=subcat_id)
    if cat.is_visible:
        cat.is_visible = False
        cat.save()
        try:
            products = Product.objects.filter(sub_category=cat)
            for product in products:
                product.is_visible = False
                product.save()
            try:
                variants = ProductVariant.objects.filter(product=product)
                for variant in variants:
                    variant.is_available = False
                    variant.save()
            except:
                pass
        except:
            pass
        cat = Sub_Category.objects.all().order_by('id')
        context = {
            'sub_cat': cat,
        }
        return render(request, 'admin/viewsubcat.html', context)
    else:
        cat.is_visible = True
        cat.save()
        try:
            products = Product.objects.filter(sub_category=cat)
            for product in products:
                product.is_visible = True
                product.save()
            try:
                variants = ProductVariant.objects.filter(product=product)
                for variant in variants:
                    variant.is_available = True
                    variant.save()
            except:
                pass
        except:
            pass
        cat = Sub_Category.objects.all().order_by('id')
        context = {
            'sub_cat': cat
        }
        return render(request, 'admin/viewsubcat.html', context)
    
# <-------------------Add Sub-Category-------------------------->
def addsubcategory(request):
    url=request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        category_id = request.POST.get('category_name')
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('sub_category_name')
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exists():
            messages.error(request, "This subcategory name already exist ")
            return redirect(url)
        slug = sub_category_name.replace(" ", "-")
        description = request.POST.get('description')
        cat_image = request.FILES.get('cat_img')
        cat = Sub_Category(category=category_instance, sub_category_name=sub_category_name, description=description,
                           cat_image=cat_image, is_visible=True,slug=slug)
        cat.save()
        return redirect('/viewsubcategory/')
    return render(request, 'admin/viewsubcat.html')


# <---------------------Edit Sub-Category------------------------>
def editsubcategory(request, subcat_id):
    cat = Sub_Category.objects.get(id=subcat_id)
    if request.method == 'POST':
        category_id = request.POST.get('category_name')
        cat.category = Category.objects.get(pk=category_id)
        cat.sub_category_name = request.POST.get('sub_category_name')
        cat.description = request.POST.get('description')
        img = request.FILES.get('cat_img')
        if img is None:
            cat.cat_image = cat.cat_image
        else:
            cat.cat_image = request.FILES.get('cat_img')
        cat.is_visible = True
        cat.save()
        cat = Category.objects.filter(is_visible=True)
        sub_cat = Sub_Category.objects.all().order_by('id')
        context = {
            'categories': cat,
            'sub_cat': sub_cat
        }
        return render(request, 'admin/viewsubcat.html', context)
# <---End Sub-Category--------------------------------------------->
#<------------------------------Start Category---------------------->
    
# <----------------------View Category------------------------->
def viewcategory(request):
    category = Category.objects.all().order_by('id')
    paginator = Paginator(category, 3)
    page_number = request.GET.get('page', 1)
    category = paginator.get_page(page_number)
    context = {
        'categories': category
    }
    return render(request, 'admin/viewcategory.html',context)
# <----------------------View Category------------------------->
# <--------------List and unlist Category---------------------->
def catunlist(request, cat_id):
    cat = Category.objects.get(id=cat_id)
    if cat.is_visible:
        cat.is_visible = False
        cat.save()
          
        try:
            sub=Sub_Category.objects.filter(category=cat)
            for item in sub:
                item.is_visible = False
                item.save()
            try:
                products =Product.objects.filter(category = cat)
                for product in products:
                        product.is_visible = False
                        product.save()
                        try:
                            variants = ProductVariant.objects.filter(product=product)
                            for variant in variants:
                                variant.is_available = False
                                variant.save()

                        except:
                            pass
            except:
                pass
        except:
            pass
        cat = Category.objects.all().order_by('id')
        context = {
            'categories': cat
        }
        return render(request, 'admin/viewcategory.html', context)
    else:
        cat.is_visible = True
        cat.save()
        try:
            sub=Sub_Category.objects.filter(category=cat)
            for item in sub:
                item.is_visible = True
                item.save()
                try:
                    products =Product.objects.filter(category = cat)
                    for product in products:
                        product.is_visible = True
                        product.save()
                        try:
                            variants = ProductVariant.objects.filter(product=product)
                            for variant in variants:
                                variant.is_available = True
                                variant.save()
                        except:
                            pass
                except:
                    pass
        except:
            pass
        cat = Category.objects.all().order_by('id')
        context = {
            'categories': cat
        }
        return render(request, 'admin/viewcategory.html', context)
# <--------------List and unlist Category---------------------->
# <--------------Add Category---------------------->
def addcategory(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        cat = Category()
        category_name = request.POST.get('category_name')
        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, "This category name already exist ")
            return redirect(url)
        else:
            cat.category_name =category_name
        cat.slug=category_name.replace(" ", "-")
        cat.description = request.POST.get('description')
        cat.cat_image = request.FILES.get('cat_img')
        cat.save()
        return redirect('/viewcategory/')
# <--------------Add Category---------------------->
    
# <---------------------Edit Category-------------------------->
def editcategory(request, category_id):
    url = request.META.get('HTTP_REFERER')
    cat = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if cat.category_name != category_name:
            if Category.objects.filter(category_name=category_name).exists():
                messages.warning(request, "This category name already exist ")
                return redirect(url)
            else:
                cat.category_name = request.POST.get('category_name')
        cat.description = request.POST.get('description')
        img = request.FILES.get('cat_img')
        if img is None:
            cat.cat_image = cat.cat_image
        else:
            cat.cat_image = request.FILES.get('cat_img')
        cat.save()
        cat = Category.objects.all().order_by('id')
        context = {
            'categories': cat
        }
        return redirect('/viewcategory/')
# <---------------------Edit Category-------------------------->

# <----------------------------------------------------End Category------------------------------------------------------>

