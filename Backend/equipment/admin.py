"""
Admin configuration for Equipment models.
"""
from django.contrib import admin
from .models import (
    EquipmentType, PlantLocation, Equipment,
    EquipmentReading, Alert, UploadHistory
)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_flowrate', 'max_flowrate', 'min_pressure', 'max_pressure', 'min_temperature', 'max_temperature']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(PlantLocation)
class PlantLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'created_at']
    search_fields = ['name', 'address']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'plant_location', 'status', 'flowrate', 'pressure', 'temperature', 'is_active']
    list_filter = ['status', 'is_active', 'equipment_type', 'plant_location']
    search_fields = ['name', 'serial_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'equipment_type', 'plant_location', 'serial_number')
        }),
        ('Current Readings', {
            'fields': ('flowrate', 'pressure', 'temperature', 'status', 'is_active')
        }),
        ('Maintenance', {
            'fields': ('installation_date', 'last_maintenance', 'next_maintenance')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(EquipmentReading)
class EquipmentReadingAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'flowrate', 'pressure', 'temperature', 'status', 'timestamp']
    list_filter = ['status', 'timestamp', 'equipment__equipment_type']
    search_fields = ['equipment__name']
    date_hierarchy = 'timestamp'


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'title', 'severity', 'status', 'parameter', 'value', 'created_at']
    list_filter = ['severity', 'status', 'parameter', 'created_at']
    search_fields = ['equipment__name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Alert Information', {
            'fields': ('equipment', 'title', 'description', 'severity', 'status')
        }),
        ('Data', {
            'fields': ('parameter', 'value', 'threshold')
        }),
        ('Resolution', {
            'fields': ('acknowledged_by', 'acknowledged_at', 'resolved_by', 'resolved_at', 'resolution_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'status', 'records_processed', 'records_success', 'records_failed', 'uploaded_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['file_name', 'uploaded_by__username']
    readonly_fields = ['created_at', 'completed_at']
