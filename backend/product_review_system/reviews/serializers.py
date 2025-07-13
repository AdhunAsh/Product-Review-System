from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'feedback', 'created_at']
        read_only_fields = ['user', 'created_at', 'product']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        product_id = self.context.get('view').kwargs.get('product_id')
        user = request.user

        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise serializers.ValidationError("You have already reviewed this product.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['product_id'] = self.context.get('view').kwargs.get('product_id')
        return super().create(validated_data)
