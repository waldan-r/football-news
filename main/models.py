from django.db import models
import uuid

# Create your models here.
class News(models.Model):
    CATEGORY_CHOICES = [
        # pilihan kategori berita yang tersedia
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length=255) # Panjang judul maks 255 karakter
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def is_news_hot(self):
        return self.news_views > 20
    
    # menambah jumlah view berita dan menyimpan perubahan ke database
    def increment_views(self):
        self.news_views += 1
        self.save()