import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import EditProductForm, ProductForm, RegisterForm, ShoppingListForm
from .models import Notification, Product, ShoppingList
import json
from unittest.mock import patch
# Create your tests here.

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        print(response['Location']) 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login')

class RegisterViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_register_with_valid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('register.html'))

    def test_register_with_invalid_data(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'password1': 'newpassword123',
            'password2': 'differentpassword123',
            'email': 'invalidemail'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

class AddToShoppingListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_to_shopping_list_url = reverse('add_to_shopping_list')

    def test_add_valid_item_to_shopping_list(self):
        response = self.client.post(self.add_to_shopping_list_url, {
            'product_name': 'Milk',
            'quantity': 2,
            'unit_of_measure': 'L'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(ShoppingList.objects.filter(product_name='Milk', user=self.user).exists())

    def test_add_invalid_item_to_shopping_list(self):
        response = self.client.post(self.add_to_shopping_list_url, {
            'product_name': '',
            'quantity': 2,
            'unit_of_measure': 'L'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShoppingList.objects.filter(quantity=2).exists())

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.home_url = reverse('home')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milk')
        self.assertTemplateUsed(response, 'home.html')

class AddToPantryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_to_pantry_url = reverse('add_to_pantry')

    def test_add_valid_product_to_pantry(self):
        response = self.client.post(self.add_to_pantry_url, {
            'product_name': 'Milk',
            'expiration_date': '2023-12-31',
            'quantity': 2,
            'unit_of_measure': 'L',
            'always_in_stock': False,
            'storage_location': 'Fridge'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Product.objects.filter(name='Milk', user=self.user).exists())

    def test_add_invalid_product_to_pantry(self):
        response = self.client.post(self.add_to_pantry_url, {
            'product_name': '',
            'expiration_date': 'invalid-date',
            'quantity': 2,
            'unit_of_measure': 'L',
            'always_in_stock': False,
            'storage_location': 'Fridge'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(quantity=2).exists())

class AddToPantryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_to_pantry_url = reverse('add_to_pantry')

    def test_add_valid_product_to_pantry(self):
        response = self.client.post(self.add_to_pantry_url, {
            'product_name': 'Milk',
            'expiration_date': '2023-12-31',
            'quantity': 2,
            'unit_of_measure': 'L',
            'always_in_stock': False,
            'storage_location': 'Fridge'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Product.objects.filter(name='Milk', user=self.user).exists())

    def test_add_invalid_product_to_pantry(self):
        response = self.client.post(self.add_to_pantry_url, {
            'product_name': '',
            'expiration_date': 'invalid-date',
            'quantity': 2,
            'unit_of_measure': 'L',
            'always_in_stock': False,
            'storage_location': 'Fridge'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(quantity=2).exists())

class RemoveFromPantryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)
        self.remove_from_pantry_url = reverse('remove_from_pantry', args=[self.product.id])

    def test_remove_product_from_pantry(self):
        response = self.client.post(self.remove_from_pantry_url)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Product.objects.filter(name='Milk', user=self.user).exists())

class PantryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.pantry_url = reverse('pantry')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2, category='Dairy')

    def test_pantry_view(self):
        response = self.client.get(self.pantry_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milk')
        self.assertContains(response, 'Dairy')
        self.assertTemplateUsed(response, 'pantry.html')

    def test_pantry_view_with_filters(self):
        response = self.client.get(self.pantry_url, {'category': 'Dairy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milk')
        self.assertTemplateUsed(response, 'pantry.html')


class NotificationsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.notifications_url = reverse('notifications')

    def test_notifications_view(self):
        response = self.client.get(self.notifications_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications.html')


class AddProductBarcodeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_product_barcode_url = reverse('add_product_barcode')

    @patch('requests.get')
    def test_add_product_barcode_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'status': 1,
            'product': {
                'product_name': 'Milk',
                'categories': 'Dairy',
                'ingredients_text': 'Milk'
            }
        }

        response = self.client.post(self.add_product_barcode_url, json.dumps({
            'barcode': '123456789'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Product.objects.filter(name='Milk', user=self.user).exists())

    @patch('requests.get')
    def test_add_product_barcode_failure(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 0}

        response = self.client.post(self.add_product_barcode_url, json.dumps({
            'barcode': '123456789'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Product.objects.filter(user=self.user).exists())

class RegisterFormTests(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        form = RegisterForm(data={
            'username': '',
            'email': 'invalidemail',
            'password1': 'newpassword123',
            'password2': 'differentpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

    def test_register_form_email_already_exists(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='testpassword')
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], "Questo indirizzo email è già in uso. Si prega di utilizzarne un altro.")

class ShoppingListFormTests(TestCase):
    def test_shopping_list_form_valid_data(self):
        form = ShoppingListForm(data={
            'product_name': 'Milk',
            'quantity': 2,
            'unit_of_measure': 'L',
            'always_in_stock': False
        })
        self.assertTrue(form.is_valid())

    def test_shopping_list_form_invalid_data(self):
        form = ShoppingListForm(data={
            'product_name': '',
            'quantity': 'invalid',
            'unit_of_measure': 'L',
            'always_in_stock': False
        })
        self.assertFalse(form.is_valid())
        self.assertIn('product_name', form.errors)
        self.assertIn('quantity', form.errors)

class ProductFormTests(TestCase):
    def test_product_form_valid_data(self):
        form = ProductForm(data={
            'name': 'Milk',
            'quantity': 2,
            'unit_of_measure': 'L',
            'expiration_date': '2023-12-31',
            'always_in_stock': False
        })
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_data(self):
        form = ProductForm(data={
            'name': '',
            'quantity': 'invalid',
            'unit_of_measure': 'L',
            'expiration_date': 'invalid-date',
            'always_in_stock': False
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('quantity', form.errors)
        self.assertIn('expiration_date', form.errors)

    def test_product_form_expiration_date_not_required(self):
        form = ProductForm(data={
            'name': 'Milk',
            'quantity': 2,
            'unit_of_measure': 'L',
            'expiration_date': '',
            'always_in_stock': False
        })
        self.assertTrue(form.is_valid())

class EditProductFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            user=self.user,
            name='Milk',
            quantity=2,
            unit_of_measure='L',
            expiration_date='2023-12-31',
            always_in_stock=False,
            category='Dairy',
            storage_location='Fridge',
            status='New',
            notes='Test note'
        )

    def test_edit_product_form_valid_data(self):
        form = EditProductForm(instance=self.product, data={
            'name': 'Milk',
            'quantity': 3,
            'unit_of_measure': 'L',
            'expiration_date': '2023-12-31',
            'always_in_stock': False,
            'category': 'Dairy',
            'storage_location': 'Fridge',
            'status': 'Opened',
            'notes': 'Updated note'
        })
        self.assertTrue(form.is_valid())

    def test_edit_product_form_invalid_data(self):
        form = EditProductForm(instance=self.product, data={
            'name': '',
            'quantity': 'invalid',
            'unit_of_measure': 'L',
            'expiration_date': 'invalid-date',
            'always_in_stock': False,
            'category': 'Dairy',
            'storage_location': 'Fridge',
            'status': 'Updated',
            'notes': 'Updated note'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('quantity', form.errors)
        self.assertIn('expiration_date', form.errors)

class ProductModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_product(self):
        expiration_date = datetime.date(2023, 12, 31)
        product = Product.objects.create(
            user=self.user,
            name='Milk',
            quantity=2,
            unit_of_measure='L',
            expiration_date=expiration_date,
            status='New',
            category='Dairy',
            storage_location='Fridge'
        )
        self.assertEqual(product.name, 'Milk')
        self.assertEqual(product.quantity, 2)
        self.assertEqual(product.unit_of_measure, 'L')
        self.assertEqual(product.expiration_date, expiration_date)
        self.assertEqual(product.status, 'New')
        self.assertEqual(product.category, 'Dairy')
        self.assertEqual(product.storage_location, 'Fridge')
        self.assertFalse(product.always_in_stock)
        self.assertIsNotNone(product.insertion_date)

class ShoppingListModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_shopping_list_item(self):
        shopping_list_item = ShoppingList.objects.create(
            user=self.user,
            product_name='Milk',
            quantity=2,
            unit_of_measure='L',
            purchased=False
        )
        self.assertEqual(shopping_list_item.product_name, 'Milk')
        self.assertEqual(shopping_list_item.quantity, 2)
        self.assertEqual(shopping_list_item.unit_of_measure, 'L')
        self.assertFalse(shopping_list_item.purchased)
        self.assertIsNotNone(shopping_list_item.added_date)


class NotificationModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_notification(self):
        notification = Notification.objects.create(
            user=self.user,
            message='Test notification'
        )
        self.assertEqual(notification.message, 'Test notification')
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.timestamp)
        self.assertEqual(str(notification), f'Notification for {self.user.username}: Test notification')

class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class AboutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.about_url = reverse('about')

    def test_about_view(self):
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.logout_url = reverse('logout')

    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

class RemoveFromPantryPageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)
        self.remove_from_pantry_page_url = reverse('remove_from_pantry_page', args=[self.product.id])

    def test_remove_from_pantry_page_view(self):
        response = self.client.post(self.remove_from_pantry_page_url)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Product.objects.filter(name='Milk', user=self.user).exists())

class RemoveFromPantryPageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)
        self.remove_from_pantry_page_url = reverse('remove_from_pantry_page', args=[self.product.id])

    def test_remove_from_pantry_page_view(self):
        response = self.client.post(self.remove_from_pantry_page_url)
        self.assertRedirects(response, reverse('pantry'))
        self.assertFalse(Product.objects.filter(name='Milk', user=self.user).exists())

class MarkAsPurchasedViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)
        self.mark_as_purchased_url = reverse('mark_as_purchased', args=[self.product.id])

    def test_mark_as_purchased_view(self):
        response = self.client.post(self.mark_as_purchased_url)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Product.objects.filter(name='Milk', user=self.user, status='Purchased').exists())

class MarkAsNotPurchasedViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2, status='Purchased')
        self.mark_as_not_purchased_url = reverse('mark_as_not_purchased', args=[self.product.id])

    def test_mark_as_not_purchased_view(self):
        response = self.client.post(self.mark_as_not_purchased_url)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(ShoppingList.objects.filter(name='Milk', user=self.user).exists())

class MoveToShoppingListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2, status='Purchased')
        self.move_to_shopping_list_url = reverse('move_to_shopping_list', args=[self.product.id])

    def test_move_to_shopping_list_view(self):
        response = self.client.post(self.move_to_shopping_list_url)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(ShoppingList.objects.filter(name='Milk', user=self.user).exists())

class PantryProductDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)
        self.pantry_product_detail_url = reverse('pantry_product_detail', args=[self.product.id])

    def test_pantry_product_detail_view(self):
        response = self.client.get(self.pantry_product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milk')

class ShoppingListItemDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.shopping_list_item = ShoppingList.objects.create(user=self.user, product_name='Milk', quantity=2)
        self.shopping_list_item_detail_url = reverse('shopping_list_item_detail', args=[self.shopping_list_item.id])

    def test_shopping_list_item_detail_view(self):
        response = self.client.get(self.shopping_list_item_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Milk')
        self.assertTemplateUsed(response, 'shopping_list_item_detail.html')

class EditShoppingListItemViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.shopping_list_item = ShoppingList.objects.create(user=self.user, product_name='Milk', quantity=2)
        self.edit_shopping_list_item_url = reverse('edit_shopping_list_item', args=[self.shopping_list_item.id])

    def test_edit_shopping_list_item_view(self):
        response = self.client.post(self.edit_shopping_list_item_url, {
            'product_name': 'Milk',
            'quantity': 3,
            'unit_of_measure': 'L',
            'always_in_stock': False
        })
        self.assertRedirects(response, reverse('shopping_list_item_detail', args=[self.shopping_list_item.id]))
        self.assertTrue(ShoppingList.objects.filter(product_name='Milk', user=self.user, quantity=3).exists())

class UpdateProductViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(user=self.user, name='Milk', quantity=2)
        self.update_product_url = reverse('update_product', args=[self.product.id])

    def test_update_product_view(self):
        response = self.client.post(self.update_product_url, {
            'name': 'Milk',
            'quantity': 3,
            'unit_of_measure': 'L',
            'expiration_date': '2023-12-31',
            'always_in_stock': False,
            'category': 'Dairy',
            'storage_location': 'Fridge',
            'status': 'New',
            'notes': 'Test note'
        })
        self.assertRedirects(response, reverse('pantry_product_detail'))
        self.assertTrue(Product.objects.filter(name='Milk', user=self.user, quantity=3).exists())

class ScannerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.scanner_url = reverse('scanner')

    def test_scanner_view(self):
        response = self.client.get(self.scanner_url)
        self.assertEqual(response.status_code, 302)

class RemoveFromShoppingListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.shopping_item = ShoppingList.objects.create(user=self.user, product_name='Milk', quantity=2)
        self.remove_from_shopping_list_url = reverse('remove_from_shopping_list', args=[self.shopping_item.id])

    def test_remove_item_from_shopping_list(self):
        response = self.client.post(self.remove_from_shopping_list_url)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(ShoppingList.objects.filter(id=self.shopping_item.id).exists())

class RemoveAndAddToPantryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.shopping_item = ShoppingList.objects.create(user=self.user, product_name='Milk', quantity=2, purchased=True)
        self.remove_and_add_to_pantry_url = reverse('remove_and_add_to_pantry')

    def test_remove_and_add_to_pantry(self):
        response = self.client.post(self.remove_and_add_to_pantry_url)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(ShoppingList.objects.filter(id=self.shopping_item.id).exists())
        self.assertTrue(Product.objects.filter(name='Milk', user=self.user).exists())

        
