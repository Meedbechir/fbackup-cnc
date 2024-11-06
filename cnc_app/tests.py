from django.test import TestCase
from .models import Article, Designation, Origine, Famille, StatusArticle
from .services import ArticleCreationService, ArticleCreationError

class ArticleCreationServiceTest(TestCase):
    
    def setUp(self):
        self.famille = Famille.objects.create(nom='Test Famille')
        self.status_article = StatusArticle.objects.create(status_article='Test Status')
        self.designation = Designation.objects.create(nom='Test Designation', famille=self.famille)

    def test_create_article_success(self):
        service = ArticleCreationService()
        data = {
            'designation_id': self.designation.id,
            'origine': 'Test Origine',
            'quantite': 5,
            'annee_inventaire': 2024
        }
        articles = service.create_article(data)
        self.assertEqual(len(articles), 5)

    def test_create_article_invalid_designation(self):
        service = ArticleCreationService()
        data = {
            'designation_id': 9999, 
            'origine': 'Test Origine',
            'quantite': 5,
            'annee_inventaire': 2024
        }
        with self.assertRaises(ArticleCreationError):
            service.create_article(data)

    def test_create_article_zero_quantity(self):
        service = ArticleCreationService()
        data = {
            'designation_id': self.designation.id,
            'origine': 'Test Origine',
            'quantite': 0,  # Quantité zéro
            'annee_inventaire': 2024
        }
        with self.assertRaises(ArticleCreationError):
            service.create_article(data)

    def test_create_article_missing_origin(self):
        service = ArticleCreationService()
        data = {
            'designation_id': self.designation.id,
            'quantite': 5,
            'annee_inventaire': 2024
        }  
        with self.assertRaises(ArticleCreationError):
            service.create_article(data)
