from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File


class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    slug = models.SlugField()
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('title',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/{self.slug}/'


STATUS_CHOICES=[
    ('sold out','sold out'),
    ('reserved','reserved'),
    ('available','available')
]


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    vendor = models.CharField(max_length=255, default="vendor1")
    # vendor = models.ForeignKey(vendor, related_name='vendor', on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=1)
    status = models.CharField(max_length=255,choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def remove_on_image_update(self):
        try:
            obj = Product.objects.get(id=self.id)
        except Product.DoesNotExist:
            return
        if self.image and obj.image and self.image and obj.image != self.image:
            storage, path = obj.image.storage, obj.image.path
            obj.image.delete()
            storage.delete(path)
            

    def delete(self, *args, **kwargs):
        try:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)
            self.image.delete()
            return super(Product, self).delete(*args, **kwargs)
        except Product.DoesNotExist:
            return super(Product, self).delete(*args, **kwargs)
        

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Product, self).save(*args, **kwargs)
