from .models import Article, DetailEntree, DetailInventaire, Emplacement, Origine, Inventaire, Famille, StatusArticle, Designation
from datetime import datetime

class ArticleCreationError(Exception):
    pass

class ArticleCreationService:
    def create_article(self, data):
        designation_id = data.get('designation_id')
        origine_nom = data.get('origine')
        quantite = data.get('quantite')
        famille_id = data.get('famille')
        annee = data.get('annee_inventaire', datetime.now().year)
        
        marque = data.get('marque', "non-spécifié")
        modele = data.get('modele', "non-spécifié")

        if not all([designation_id, origine_nom, quantite, famille_id]) or int(quantite) < 1:
            raise ArticleCreationError('Tous les champs doivent être remplis, et la quantité doit être positive.')

        try:
            designation = Designation.objects.get(id=designation_id)
        except Designation.DoesNotExist:
            raise ArticleCreationError('La désignation spécifiée n\'existe pas.')

        origine, _ = Origine.objects.get_or_create(nom=origine_nom)
        try:
            famille = Famille.objects.get(id=famille_id)
        except Famille.DoesNotExist:
            raise ArticleCreationError('La famille spécifiée n\'existe pas.')   
        inventaire, _ = Inventaire.objects.get_or_create(annee_inventaire=annee)

        return self.create_articles(designation, origine, inventaire, quantite, famille, marque=marque, modele=modele)  # Passer marque et modele

    def create_articles(self, designation, origine, inventaire, quantite, famille, marque="non-spécifié", modele="non-spécifié"):
        articles = []
        articles_existants = Article.objects.filter(designation=designation)
        dernier_numero = self.get_dernier_numero(articles_existants)

        for i in range(1, quantite + 1):
            numero_article = dernier_numero + i
            code_article = self.generate_code_article(designation, "emplacement-pas-defini", origine.nom, numero_article)
            
            article = Article(designation=designation, famille=famille)
            article.save()

            emplacement_service = DetailManagementService()
            emplacement_service.create_detail_entree(article, origine, code_article,marque=marque, modele=modele)
            emplacement_service.create_detail_inventaire(article, inventaire)

            articles.append(article)

        return articles

    def get_dernier_numero(self, articles_existants):
        return articles_existants.count() if articles_existants.exists() else 0

    def generate_code_article(self, designation, emplacement_nom, origine_nom, numero_article):
        return f"{designation.nom[:4].lower()}{numero_article}/{emplacement_nom.lower()}/{origine_nom.lower()}"

class DetailManagementService:
    def create_detail_entree(self, article, origine, code_article,marque="non-spécifié", modele="non-spécifié"):
        emplacement_nom = "emplacement-par-defaut".lower()
        emplacement, _ = Emplacement.objects.get_or_create(nom=emplacement_nom)
        DetailEntree.objects.create(
            article=article,
            quantite_entree=1,
            origine=origine,
            emplacement=emplacement,
            code_article=code_article,
            status=StatusArticle.objects.first(),
            marque=marque,
            modele=modele
        )

    def create_detail_inventaire(self, article, inventaire):
        DetailInventaire.objects.create(
            article=article,
            inventaire=inventaire,
            quantite=1,
            status_article=StatusArticle.objects.first()
        )

class ArticleUpdateService:
    def update_article(self, article, emplacement_nom=None, status_article_id=None):
        detail_entree = DetailEntree.objects.filter(article=article).first()

        if detail_entree is None:
            raise ArticleCreationError('L\'article n\'a pas d\'entrée de détail.')

        if emplacement_nom:
            emplacement_nom = emplacement_nom.lower()
            emplacement, _ = Emplacement.objects.get_or_create(nom=emplacement_nom)
            
            origine_nom = detail_entree.origine.nom
            existing_code_article = detail_entree.code_article.split('/')[0]
            code_article = f"{existing_code_article}/{emplacement_nom}/{origine_nom.lower()}"
            
            detail_entree.code_article = code_article
            detail_entree.emplacement = emplacement 

        if status_article_id:
            detail_entree.status_id = status_article_id

        detail_entree.save()
        return detail_entree.code_article



