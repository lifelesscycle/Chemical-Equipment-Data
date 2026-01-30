"""
Serializers for API endpoints.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from equipment.models import (
    EquipmentType, PlantLocation, Equipment,
    EquipmentReading, Alert, UploadHistory
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class EquipmentTypeSerializer(serializers.ModelSerializer):
    """Equipment Type serializer."""
    
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentType
        fields = [
            'id', 'name', 'description',
            'min_flowrate', 'max_flowrate',
            'min_pressure', 'max_pressure',
            'min_temperature', 'max_temperature',
            'equipment_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_equipment_count(self, obj):
        return obj.equipment.filter(is_active=True).count()


class PlantLocationSerializer(serializers.ModelSerializer):
    """Plant Location serializer."""
    
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantLocation
        fields = ['id', 'name', 'address', 'capacity', 'equipment_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_equipment_count(self, obj):
        return obj.equipment.filter(is_active=True).count()


class EquipmentListSerializer(serializers.ModelSerializer):
    """Simplified Equipment serializer for list views."""
    
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)
    plant_location_name = serializers.CharField(source='plant_location.name', read_only=True)
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'equipment_type', 'equipment_type_name',
            'plant_location', 'plant_location_name',
            'flowrate', 'pressure', 'temperature',
            'status', 'is_active', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'updated_at']


class EquipmentDetailSerializer(serializers.ModelSerializer):
    """Detailed Equipment serializer."""
    
    equipment_type_details = EquipmentTypeSerializer(source='equipment_type', read_only=True)
    plant_location_details = PlantLocationSerializer(source='plant_location', read_only=True)
    recent_readings_count = serializers.SerializerMethodField()
    active_alerts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'equipment_type', 'equipment_type_details',
            'plant_location', 'plant_location_details',
            'flowrate', 'pressure', 'temperature',
            'status', 'is_active',
            'serial_number', 'installation_date',
            'last_maintenance', 'next_maintenance',
            'notes', 'recent_readings_count', 'active_alerts_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def get_recent_readings_count(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        last_24h = timezone.now() - timedelta(hours=24)
        return obj.readings.filter(timestamp__gte=last_24h).count()
    
    def get_active_alerts_count(self, obj):
        return obj.alerts.filter(status='open').count()


class EquipmentReadingSerializer(serializers.ModelSerializer):
    """Equipment Reading serializer."""
    
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    
    class Meta:
        model = EquipmentReading
        fields = [
            'id', 'equipment', 'equipment_name',
            'flowrate', 'pressure', 'temperature',
            'status', 'timestamp', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AlertSerializer(serializers.ModelSerializer):
    """Alert serializer."""
    
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    acknowledged_by_name = serializers.CharField(source='acknowledged_by.username', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.username', read_only=True)
    
    class Meta:
        model = Alert
        fields = [
            'id', 'equipment', 'equipment_name',
            'title', 'description', 'severity', 'status',
            'parameter', 'value', 'threshold',
            'acknowledged_by', 'acknowledged_by_name', 'acknowledged_at',
            'resolved_by', 'resolved_by_name', 'resolved_at',
            'resolution_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UploadHistorySerializer(serializers.ModelSerializer):
    """Upload History serializer."""
    
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = UploadHistory
        fields = [
            'id', 'file_name', 'file_path', 'file_size',
            'status', 'records_processed', 'records_success', 'records_failed',
            'error_log', 'uploaded_by', 'uploaded_by_name',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Dashboard statistics serializer."""
    
    total_equipment = serializers.IntegerField()
    normal_count = serializers.IntegerField()
    warning_count = serializers.IntegerField()
    critical_count = serializers.IntegerField()
    offline_count = serializers.IntegerField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    max_flowrate = serializers.FloatField()
    active_alerts = serializers.IntegerField()
