"""
Equipment models for chemical processing equipment monitoring.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class EquipmentType(models.Model):
    """Equipment type classification."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Safe operating ranges
    min_flowrate = models.FloatField(help_text="Minimum safe flowrate (L/min)")
    max_flowrate = models.FloatField(help_text="Maximum safe flowrate (L/min)")
    min_pressure = models.FloatField(help_text="Minimum safe pressure (bar)")
    max_pressure = models.FloatField(help_text="Maximum safe pressure (bar)")
    min_temperature = models.FloatField(help_text="Minimum safe temperature (°C)")
    max_temperature = models.FloatField(help_text="Maximum safe temperature (°C)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipment Type"
        verbose_name_plural = "Equipment Types"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PlantLocation(models.Model):
    """Plant location information."""
    
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    capacity = models.IntegerField(default=0, help_text="Maximum equipment capacity")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Plant Location"
        verbose_name_plural = "Plant Locations"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Main equipment model."""
    
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('offline', 'Offline'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name='equipment'
    )
    plant_location = models.ForeignKey(
        PlantLocation,
        on_delete=models.PROTECT,
        related_name='equipment'
    )
    
    # Current readings
    flowrate = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Current flowrate (L/min)"
    )
    pressure = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Current pressure (bar)"
    )
    temperature = models.FloatField(help_text="Current temperature (°C)")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)
    
    # Metadata
    serial_number = models.CharField(max_length=100, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
        ordering = ['name']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['equipment_type', 'plant_location']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.equipment_type.name})"
    
    def check_status(self):
        """Check if equipment is operating within safe ranges."""
        eq_type = self.equipment_type
        
        flowrate_ok = eq_type.min_flowrate <= self.flowrate <= eq_type.max_flowrate
        pressure_ok = eq_type.min_pressure <= self.pressure <= eq_type.max_pressure
        temp_ok = eq_type.min_temperature <= self.temperature <= eq_type.max_temperature
        
        if not (flowrate_ok and pressure_ok and temp_ok):
            return 'warning'
        return 'normal'
    
    def save(self, *args, **kwargs):
        """Override save to auto-update status."""
        if self.is_active:
            self.status = self.check_status()
        else:
            self.status = 'offline'
        super().save(*args, **kwargs)


class EquipmentReading(models.Model):
    """Historical readings for equipment."""
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='readings'
    )
    
    flowrate = models.FloatField(help_text="Flowrate (L/min)")
    pressure = models.FloatField(help_text="Pressure (bar)")
    temperature = models.FloatField(help_text="Temperature (°C)")
    
    status = models.CharField(max_length=20)
    
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Equipment Reading"
        verbose_name_plural = "Equipment Readings"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['equipment', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.equipment.name} - {self.timestamp}"


class Alert(models.Model):
    """Alerts for equipment issues."""
    
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='warning')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Alert data
    parameter = models.CharField(max_length=50)  # flowrate, pressure, temperature
    value = models.FloatField()
    threshold = models.FloatField()
    
    # Resolution tracking
    acknowledged_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acknowledged_alerts'
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'severity']),
            models.Index(fields=['equipment', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.severity.upper()}: {self.title} - {self.equipment.name}"


class UploadHistory(models.Model):
    """Track file uploads."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
    ]
    
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_size = models.BigIntegerField(help_text="File size in bytes")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Processing results
    records_processed = models.IntegerField(default=0)
    records_success = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    error_log = models.TextField(blank=True)
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploads'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Upload History"
        verbose_name_plural = "Upload Histories"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_name} - {self.status}"
