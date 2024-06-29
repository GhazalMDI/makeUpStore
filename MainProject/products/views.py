from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.db.models import Q

from products.models import Product, Comment, SeenProduct, UserProductView, LikeProduct,Variant
from products.filters import ProductsFilter
from products.forms import CommentForm


class Products(View):
    template_name = 'products.html'
    def get(self, request, cat_id=None, cat_slug=None):
        products = Product.objects.all()
        variants = Variant.objects.all()
        if filters := ProductsFilter(data=request.GET, queryset=products):
            products = filters.qs

        if cat_id and not cat_slug:
            products = products.filter(secondCategory__id=cat_id, discount__gt=0)

        if cat_id and cat_slug:
            products = products.filter(
                Q(firstCategory__id=cat_id, firstCategory__slug=cat_slug) | Q(secondCategory__id=cat_id,
                                                                              secondCategory__slug=cat_slug))

        if filter_text := request.GET.get('search'):
            products = products.filter(name__contains=filter_text)

        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        url_data = request.GET.copy()
        if 'page' in url_data:
            del url_data['page']
        ctx = {
            'variants':variants,
            'filters': filters,
            'products': products,
            'url_data': urlencode(url_data),
            'len_products': len(products),
        }

        return render(request, self.template_name, ctx)


class detailView(View):
    template_name = 'details.html'
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs['id'], slug=kwargs['slug'])
        for t in self.product.tag.all():
            self.products_same = Product.objects.filter(tag__name__icontains=t.name)

        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        selected_var = None
        product = self.product
        user = request.user
        if product.status == 'Color':
            selected_var = product.variant_product.all().first()
        if color_user := request.GET.get('select-color'):
            selected_var = product.variant_product.filter(id=color_user).first()

        if request.user.is_authenticated:
            obj, created = SeenProduct.objects.get_or_create(product_id=product.id, user=request.user)
            if user.seen_product_user.count() > 50:
                if created:
                    user.seen_product_user.first().delete()

            objec, create = UserProductView.objects.get_or_create(product_id=product.id, user=request.user)
            if not create:
                objec.view_count += 1
                objec.save()

        ctx = {
            'selected_var': selected_var,
            'form': self.form_class(),
            'product': product,
            'products_same': self.products_same,
            'comments': Comment.objects.filter(accepted=True,product_id=product.id),
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.product
            comment.save()

            return redirect('products:details', self.product.id, self.product.slug)

        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class AddLikeView(View):
    def get(self, request, productId=None, varproduct_id=None):
        if productId and not varproduct_id:
            obj, created = LikeProduct.objects.get_or_create(product_id=productId, user=request.user)
            print('add')
            if not created:
                print('object is here')
                obj.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not productId and varproduct_id:
            obj, created = LikeProduct.objects.get_or_create(variant_id=varproduct_id, user=request.user)
            if not created:
                obj.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class removeProductView(View):
    def get(self, request, id):
        if id:
            if obj := get_object_or_404(LikeProduct, id=id):
                obj.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('404.html')
