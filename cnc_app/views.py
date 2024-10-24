from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Designation,Famille
from .serializers import ArticleSerializer, DesignationSerializer, FamilleSerializer
from .services import ArticleCreationService, ArticleUpdateService

class FamilleViewSet(viewsets.ModelViewSet):
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer
    
    def create(self, request, *args, **kwargs):
        creation_service = ArticleCreationService()
        
        try:
            marque = request.data.get('marque', "non-spécifié")
            modele = request.data.get('modele', "non-spécifié")
            
            request.data['marque'] = marque
            request.data['modele'] = modele
            
            articles = creation_service.create_article(request.data)
            
            return Response({'message': f'{len(articles)} articles créés', 'articles': ArticleSerializer(articles, many=True).data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        article_update_service = ArticleUpdateService()
        
        article = self.get_object()
        emplacement_nom = request.data.get('emplacement') 
        status_article_id = request.data.get('status_article')

        if emplacement_nom is not None:
            emplacement_nom = emplacement_nom.replace(' ', '-')
        
        try:
            code_article = article_update_service.update_article(article, emplacement_nom, status_article_id)
            return Response({
                'message': 'Article mis à jour avec succès.',
                'article': ArticleSerializer(article).data,
                'code_article': code_article
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



        
        