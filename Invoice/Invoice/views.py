# views.py

# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer

    def create(self, request, *args, **kwargs):
        invoice_id = request.data.get('invoice')  
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        request.data['invoice'] = invoice.id 
        return super().create(request, *args, **kwargs)

