"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipmentTypeViewSet, PlantLocationViewSet, EquipmentViewSet,
    EquipmentReadingViewSet, AlertViewSet, UploadHistoryViewSet,
    dashboard_stats, charts, upload_csv, export_data
)

# Create router
router = DefaultRouter()
router.register(r'equipment-types', EquipmentTypeViewSet, basename='equipment-type')
router.register(r'plant-locations', PlantLocationViewSet, basename='plant-location')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'readings', EquipmentReadingViewSet, basename='reading')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'uploads', UploadHistoryViewSet, basename='upload')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('charts/', charts, name='charts'),
    path('upload/', upload_csv, name='upload-csv'),
    path('export/', export_data, name='export-data'),
]
