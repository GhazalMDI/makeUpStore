from products.models import SecondCategory,FirstCategory,SeenProduct

def category(request):
    return {
        'FirstCategory':FirstCategory.objects.all(),
        'seen_product':SeenProduct.objects.filter(user=request.user) if request.user.is_authenticated else None
    }
