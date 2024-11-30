from rest_framework import serializers
from .models import Product, Customer, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['total_price']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'status', 'items', 'total_amount']
        read_only_fields = ['order_date', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        # Create OrderItem instances
        for item_data in items_data:
            product = item_data.pop('product')
            OrderItem.objects.create(order=order, product=product, **item_data)

        return order
