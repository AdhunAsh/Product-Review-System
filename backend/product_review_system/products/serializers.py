from rest_framework import serializers
from .models import Product
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'average_rating', 'reviews']
        
    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product = obj)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None
    
    