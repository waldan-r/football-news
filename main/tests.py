from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from .models import News

class MainTest(TestCase):
    # cek server memberikan respon 200 (OK) ketika client mengakses endpoint (halaman utama)
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    # cek apakah halaman utama mengembalikan kode status 200 atau dirender menggunakan template "main.html"
    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    # cek jika client mengakses URL yang tidak ada, aplikasi Django mengembalikan kode status 404 (Not Found)
    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    # test pembuatan objek News baru dan pengujian properti
    def test_news_creation(self):
        news = News.objects.create(
          title="BURHAN FC MENANG",
          content="BURHAN FC 1-0 PANDA BC",
          category="match",
          news_views=1001,
          is_featured=True
        )
        self.assertTrue(news.is_news_hot) # True (views: 1001)
        self.assertEqual(news.category, "match") # True
        self.assertTrue(news.is_featured) # True
    
        
    def test_news_default_values(self):
        news = News.objects.create(
          title="Test News",
          content="Test content"
        )
        self.assertEqual(news.category, "update")
        self.assertEqual(news.news_views, 0)
        self.assertFalse(news.is_featured)
        self.assertFalse(news.is_news_hot)
        
    def test_increment_views(self):
        news = News.objects.create(
          title="Test News",
          content="Test content"
        )
        initial_views = news.news_views
        news.increment_views()
        self.assertEqual(news.news_views, initial_views + 1)
        
    def test_is_news_hot_threshold(self):
        # Test news with exactly 20 views (should not be hot)
        news_20 = News.objects.create(
          title="News with 20 views",
          content="Test content",
          news_views=20
        )
        self.assertFalse(news_20.is_news_hot)
        
        # Test news with 21 views (should be hot)
        news_21 = News.objects.create(
          title="News with 21 views", 
          content="Test content",
          news_views=21
        )
        self.assertTrue(news_21.is_news_hot)