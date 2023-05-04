from django.urls import path, include
from django.contrib.auth import views as auth_views
from document import views


urlpatterns = [
    path('doc_show/', views.show_documents, name='show_documents'),
    path('issuance/<slug:document_slug>', views.issuance_info, name='document_info'),
    path('edit/<slug:slug>', views.edit_issue, name='edit_issue'),
    path('cost/<slug:cost_slug>', views.cost_info, name='cost_info'),
    path('create/', views.add_issuance, name='add_issance'),
    path('create-cost/', views.add_issuance, name='add_cost'),
    # path('add_deliver/<int:count>', views.add_deliver, name='add_deliver'),
]