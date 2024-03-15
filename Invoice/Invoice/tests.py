from django.test import TestCase
from rest_framework.test import APIClient
from .models import Invoice

class InvoiceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_invoice_with_details(self):
        data = {
            'date': '2024-03-15',
            'customer_name': 'Test Customer',
            'details': [
                {
                    'description': 'Test Description 1',
                    'quantity': 1,
                    'unit_price': 10.00,
                    'price': 10.00
                },
                {
                    'description': 'Test Description 2',
                    'quantity': 2,
                    'unit_price': 20.00,
                    'price': 40.00
                }
            ]
        }
        response = self.client.post('/invoices/', data, format='json')
        
        # Print request payload
        print("Request payload:", data)
        
        # Print response data
        print("Response data:", response.data)
        
        # Print response status code
        print("Response status code:", response.status_code)

        # Check for validation errors in response data
        if response.status_code == 400:
            print("Validation errors:", response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.first().details.count(), 2)

    def test_get_invoice_list(self):
        response = self.client.get('/invoices/')
        self.assertEqual(response.status_code, 200)

    def test_get_single_invoice(self):
        invoice = Invoice.objects.create(date='2024-03-15', customer_name='Test Customer')
        response = self.client.get(f'/invoices/{invoice.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_update_invoice(self):
        invoice = Invoice.objects.create(date='2024-03-15', customer_name='Test Customer')
        data = {
            'date': '2024-03-16',
            'customer_name': 'Updated Customer'
        }
        response = self.client.put(f'/invoices/{invoice.pk}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        updated_invoice = Invoice.objects.get(pk=invoice.pk)
        self.assertEqual(str(updated_invoice.date), '2024-03-16')  # Modify this line
        self.assertEqual(updated_invoice.customer_name, 'Updated Customer')


    def test_delete_invoice(self):
        invoice = Invoice.objects.create(date='2024-03-15', customer_name='Test Customer')
        response = self.client.delete(f'/invoices/{invoice.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Invoice.objects.count(), 0)
