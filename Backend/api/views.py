"""
API Views for equipment monitoring system.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Avg, Max, Q
from django.utils import timezone
from datetime import timedelta
import pandas as pd

from equipment.models import (
    EquipmentType, PlantLocation, Equipment,
    EquipmentReading, Alert, UploadHistory
)
from .serializers import (
    EquipmentTypeSerializer, PlantLocationSerializer,
    EquipmentListSerializer, EquipmentDetailSerializer,
    EquipmentReadingSerializer, AlertSerializer,
    UploadHistorySerializer, DashboardStatsSerializer
)
from .charts import (
    generate_flowrate_comparison_chart,
    generate_temperature_pressure_trends,
    generate_equipment_type_distribution,
    generate_pressure_temperature_scatter,
    generate_historical_trends,
    generate_status_distribution,
    generate_plant_location_comparison
)


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for Equipment Types."""
    
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class PlantLocationViewSet(viewsets.ModelViewSet):
    """ViewSet for Plant Locations."""
    
    queryset = PlantLocation.objects.all()
    serializer_class = PlantLocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'capacity', 'created_at']
    ordering = ['name']


class EquipmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Equipment."""
    
    queryset = Equipment.objects.select_related(
        'equipment_type', 'plant_location'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'serial_number', 'equipment_type__name', 'plant_location__name']
    ordering_fields = ['name', 'status', 'flowrate', 'pressure', 'temperature', 'updated_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipmentListSerializer
        return EquipmentDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by equipment type
        equipment_type = self.request.query_params.get('equipment_type', None)
        if equipment_type:
            queryset = queryset.filter(equipment_type_id=equipment_type)
        
        # Filter by plant location
        plant_location = self.request.query_params.get('plant_location', None)
        if plant_location:
            queryset = queryset.filter(plant_location_id=plant_location)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def readings(self, request, pk=None):
        """Get historical readings for equipment."""
        equipment = self.get_object()
        
        # Get date range from query params
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        readings = EquipmentReading.objects.filter(
            equipment=equipment,
            timestamp__gte=start_date
        ).order_by('-timestamp')
        
        page = self.paginate_queryset(readings)
        if page is not None:
            serializer = EquipmentReadingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = EquipmentReadingSerializer(readings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        """Get alerts for equipment."""
        equipment = self.get_object()
        
        alert_status = request.query_params.get('status', None)
        alerts = equipment.alerts.all()
        
        if alert_status:
            alerts = alerts.filter(status=alert_status)
        
        alerts = alerts.order_by('-created_at')
        
        page = self.paginate_queryset(alerts)
        if page is not None:
            serializer = AlertSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update equipment readings."""
        data = request.data.get('equipment', [])
        updated_count = 0
        
        for item in data:
            try:
                equipment = Equipment.objects.get(id=item['id'])
                equipment.flowrate = item.get('flowrate', equipment.flowrate)
                equipment.pressure = item.get('pressure', equipment.pressure)
                equipment.temperature = item.get('temperature', equipment.temperature)
                equipment.save()
                
                # Create reading record
                EquipmentReading.objects.create(
                    equipment=equipment,
                    flowrate=equipment.flowrate,
                    pressure=equipment.pressure,
                    temperature=equipment.temperature,
                    status=equipment.status
                )
                updated_count += 1
            except Equipment.DoesNotExist:
                continue
        
        return Response({
            'message': f'Updated {updated_count} equipment records',
            'updated_count': updated_count
        })


class EquipmentReadingViewSet(viewsets.ModelViewSet):
    """ViewSet for Equipment Readings."""
    
    queryset = EquipmentReading.objects.select_related('equipment').all()
    serializer_class = EquipmentReadingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by equipment
        equipment_id = self.request.query_params.get('equipment', None)
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset


class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet for Alerts."""
    
    queryset = Alert.objects.select_related('equipment', 'acknowledged_by', 'resolved_by').all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'equipment__name']
    ordering_fields = ['severity', 'status', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        alert_status = self.request.query_params.get('status', None)
        if alert_status:
            queryset = queryset.filter(status=alert_status)
        
        # Filter by severity
        severity = self.request.query_params.get('severity', None)
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by equipment
        equipment_id = self.request.query_params.get('equipment', None)
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert."""
        alert = self.get_object()
        
        if alert.status != 'open':
            return Response(
                {'error': 'Alert is not open'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alert.status = 'acknowledged'
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an alert."""
        alert = self.get_object()
        
        if alert.status == 'resolved':
            return Response(
                {'error': 'Alert is already resolved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alert.status = 'resolved'
        alert.resolved_by = request.user
        alert.resolved_at = timezone.now()
        alert.resolution_notes = request.data.get('resolution_notes', '')
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)


class UploadHistoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Upload History."""
    
    queryset = UploadHistory.objects.select_related('uploaded_by').all()
    serializer_class = UploadHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['file_name']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        upload_status = self.request.query_params.get('status', None)
        if upload_status:
            queryset = queryset.filter(status=upload_status)
        
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics."""
    
    # Get filter parameters
    timeframe = request.query_params.get('timeframe', 'all')
    plant_location = request.query_params.get('plant_location', None)
    equipment_type = request.query_params.get('equipment_type', None)
    
    # Base queryset
    queryset = Equipment.objects.filter(is_active=True)
    
    # Apply filters
    if plant_location and plant_location != 'all':
        queryset = queryset.filter(plant_location_id=plant_location)
    
    if equipment_type and equipment_type != 'all':
        queryset = queryset.filter(equipment_type_id=equipment_type)
    
    # Calculate statistics
    total_equipment = queryset.count()
    normal_count = queryset.filter(status='normal').count()
    warning_count = queryset.filter(status='warning').count()
    critical_count = queryset.filter(status='critical').count()
    offline_count = queryset.filter(status='offline').count()
    
    # Aggregations
    aggregations = queryset.aggregate(
        avg_pressure=Avg('pressure'),
        avg_temperature=Avg('temperature'),
        max_flowrate=Max('flowrate')
    )
    
    # Active alerts
    active_alerts = Alert.objects.filter(status='open').count()
    
    stats = {
        'total_equipment': total_equipment,
        'normal_count': normal_count,
        'warning_count': warning_count,
        'critical_count': critical_count,
        'offline_count': offline_count,
        'avg_pressure': round(aggregations['avg_pressure'] or 0, 2),
        'avg_temperature': round(aggregations['avg_temperature'] or 0, 2),
        'max_flowrate': round(aggregations['max_flowrate'] or 0, 2),
        'active_alerts': active_alerts
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def charts(request):
    """Generate and return charts."""
    
    chart_type = request.query_params.get('type', 'flowrate_comparison')
    dark_mode = request.query_params.get('dark_mode', 'false').lower() == 'true'
    
    # Get filtered equipment queryset
    queryset = Equipment.objects.filter(is_active=True)
    
    plant_location = request.query_params.get('plant_location', None)
    equipment_type = request.query_params.get('equipment_type', None)
    
    if plant_location and plant_location != 'all':
        queryset = queryset.filter(plant_location_id=plant_location)
    
    if equipment_type and equipment_type != 'all':
        queryset = queryset.filter(equipment_type_id=equipment_type)
    
    chart_data = None
    
    try:
        if chart_type == 'flowrate_comparison':
            chart_data = generate_flowrate_comparison_chart(queryset, dark_mode)
        elif chart_type == 'temperature_pressure_trends':
            chart_data = generate_temperature_pressure_trends(queryset, dark_mode)
        elif chart_type == 'equipment_type_distribution':
            chart_data = generate_equipment_type_distribution(dark_mode)
        elif chart_type == 'pressure_temperature_scatter':
            chart_data = generate_pressure_temperature_scatter(queryset, dark_mode)
        elif chart_type == 'status_distribution':
            chart_data = generate_status_distribution(dark_mode)
        elif chart_type == 'plant_location_comparison':
            chart_data = generate_plant_location_comparison(dark_mode)
        elif chart_type == 'historical_trends':
            equipment_id = request.query_params.get('equipment_id')
            days = int(request.query_params.get('days', 7))
            if equipment_id:
                chart_data = generate_historical_trends(equipment_id, days, dark_mode)
        else:
            return Response(
                {'error': 'Invalid chart type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if chart_data is None:
            return Response(
                {'error': 'Unable to generate chart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({'chart': chart_data, 'type': chart_type})
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import pandas as pd
import math

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and process CSV / Excel file with equipment data"""

    # ---------- File validation ----------
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    uploaded_file = request.FILES['file']
    filename = uploaded_file.name.lower()

    if not filename.endswith(('.csv', '.xls', '.xlsx')):
        return Response(
            {'error': 'Only CSV, XLS, and XLSX files are supported'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ---------- Create upload history ----------
    upload_history = UploadHistory.objects.create(
        file_name=uploaded_file.name,
        file_path=uploaded_file,
        file_size=uploaded_file.size,
        status='processing',
        uploaded_by=request.user
    )

    try:
        # ---------- IMPORTANT: reset file pointer ----------
        uploaded_file.seek(0)

        # ---------- Read file ----------
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()
        
        column_mapping = {
            'equipment name': 'name',
            'equipment_name': 'name',
            'equipment': 'name',
            'equipment type': 'type',
            'equipment_type': 'type',
            'category': 'type',
            'plant location': 'location',
            'plant_location': 'location',
            'plant': 'location',
            'site': 'location'
        }
        df.rename(columns=column_mapping, inplace=True)

        # ---------- Required columns ----------
        required_columns = {'name', 'type'}
        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing columns. Found: {list(df.columns)}. Expected: {list(required_columns)}"
            )

        # ---------- Safe float helper ----------
        def safe_float(value, default=0):
            try:
                if value is None or (isinstance(value, float) and math.isnan(value)):
                    return default
                return float(value)
            except Exception:
                return default

        # ---------- Processing stats ----------
        records_processed = 0
        records_success = 0
        records_failed = 0
        errors = []

        # ---------- Process rows ----------
        for index, row in df.iterrows():
            records_processed += 1

            try:
                name_val = str(row.get('name', '')).strip()
                type_val = str(row.get('type', '')).strip()
                
                # FIX: Default to 'Main Plant' if location is missing
                loc_val = str(row.get('location', 'Main Plant')).strip()
                if loc_val.lower() == 'nan'or not loc_val: # Handle empty cells in Excel
                    loc_val = 'Main Plant'

                if not name_val or not type_val:
                    raise ValueError("Skipping row: Name or Type is empty")
                
                eq_type, _ = EquipmentType.objects.get_or_create(
                    name=type_val,
                    defaults={
                        'min_flowrate': 0, 'max_flowrate': 200,
                        'min_pressure': 0, 'max_pressure': 15,
                        'min_temperature': 0, 'max_temperature': 200
                    }
                )

                plant_loc, _ = PlantLocation.objects.get_or_create(
                    name=loc_val,
                    defaults={'capacity': 100}
                )

                # Update or Create Equipment
                equipment,_ = Equipment.objects.update_or_create(
                    name=name_val,
                    plant_location=plant_loc,
                    defaults={
                        'equipment_type': eq_type,
                        'flowrate': safe_float(row.get('flowrate') or 0),
                        'pressure': safe_float(row.get('pressure') or 0),
                        'temperature': safe_float(row.get('temperature') or 0),
                        'is_active': True,
                        'status': 'normal'
                    }
                )
                # Reading
                EquipmentReading.objects.create(
                    equipment=equipment,
                    flowrate=equipment.flowrate,
                    pressure=equipment.pressure,
                    temperature=equipment.temperature,
                    status=equipment.status
                )

                records_success += 1

            except Exception as row_error:
                records_failed += 1
                errors.append(f"Row {index + 1}: {str(row_error)}")

        # ---------- Finalize upload ----------
        upload_history.status = 'completed' if records_failed == 0 else 'failed'
        upload_history.records_processed = records_processed
        upload_history.records_success = records_success
        upload_history.records_failed = records_failed
        upload_history.error_log = '\n'.join(errors[:100])
        upload_history.completed_at = timezone.now()
        upload_history.save()

        return Response({
            'message': 'File processed successfully',
            'upload_id': upload_history.id,
            'records_processed': records_processed,
            'records_success': records_success,
            'records_failed': records_failed,
            'errors': errors[:10]
        }, status=status.HTTP_200_OK)

    except Exception as e:
        upload_history.status = 'failed'
        upload_history.error_log = str(e)
        upload_history.completed_at = timezone.now()
        upload_history.save()

        return Response(
            {'error': f'Failed to process file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request):
    """Export equipment data to CSV."""
    
    queryset = Equipment.objects.filter(is_active=True).select_related(
        'equipment_type', 'plant_location'
    )
    
    # Apply filters
    plant_location = request.query_params.get('plant_location', None)
    equipment_type = request.query_params.get('equipment_type', None)
    
    if plant_location and plant_location != 'all':
        queryset = queryset.filter(plant_location_id=plant_location)
    
    if equipment_type and equipment_type != 'all':
        queryset = queryset.filter(equipment_type_id=equipment_type)
    
    # Prepare data for export
    data = []
    for equipment in queryset:
        data.append({
            'Name': equipment.name,
            'Type': equipment.equipment_type.name,
            'Location': equipment.plant_location.name,
            'Flowrate (L/min)': equipment.flowrate,
            'Pressure (bar)': equipment.pressure,
            'Temperature (°C)': equipment.temperature,
            'Status': equipment.status,
            'Serial Number': equipment.serial_number,
            'Last Updated': equipment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(data)
    
    # Convert to CSV
    csv_data = df.to_csv(index=False)
    
    response = Response(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="equipment_data.csv"'
    
    return response
