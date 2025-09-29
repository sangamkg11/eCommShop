#this ffile take the  request as an argument and return the dictionary of data as context
from .models import Category
def menu_links(request):
    link=Category.objects.all()
    return dict(links=link)