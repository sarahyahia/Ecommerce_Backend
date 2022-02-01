from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File



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
