from django.urls import path
from .views import (
    list_employes, create_employe, get_employe,
    update_employe, delete_employe, generer_qrcode_employe
)

urlpatterns = [
    path('employes/', list_employes),
    path('employes/create/', create_employe),
    path('employes/<int:id>/', get_employe),
    path('employes/<int:id>/update/', update_employe),
    path('employes/<int:id>/delete/', delete_employe),
    path('employes/<int:id>/qrcode/', generer_qrcode_employe),
]
