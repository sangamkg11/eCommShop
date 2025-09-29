from django.db import models
from django.urls import reverse

# Create your models here.
#model for the category of product 
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)

    #to fix the typo error od s in ends of django admin panel we use the meta
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    #this enable the search functionality by  category by  fetching tghe data from the  views.py fo sttore 
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])

    def __str__(self):
        return self.category_name


#