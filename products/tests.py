from django.test import TestCase
from django.urls import reverse
from products.models import Product, Cart, CartItem
from decimal import Decimal

class CartViewsTest(TestCase):
    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=Decimal("50.00"),
            stock=10
        )

    def test_cart_detail_empty(self):
        # Access cart detail when cart is empty
        response = self.client.get(reverse('products:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Cart is Empty")

    def test_cart_detail_with_items(self):
        # Add item to cart
        self.client.post(reverse('products:add_to_cart', args=[self.product.pk]))
        
        response = self.client.get(reverse('products:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        # Subtotal should be $50.00, Shipping should be $10.00 (since 50 < 150), Total $60.00
        # Check that shipping is calculated correctly
        self.assertEqual(response.context['subtotal'], Decimal('50.00'))
        self.assertEqual(response.context['shipping'], Decimal('10.00'))
        self.assertEqual(response.context['total'], Decimal('60.00'))
        self.assertEqual(response.context['amount_to_free_shipping'], Decimal('100.00'))

    def test_checkout_view(self):
        # Add item to cart
        self.client.post(reverse('products:add_to_cart', args=[self.product.pk]))
        
        response = self.client.get(reverse('products:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['subtotal'], Decimal('50.00'))
        self.assertEqual(response.context['shipping'], Decimal('10.00'))
        self.assertEqual(response.context['total'], Decimal('60.00'))
