"""
Chart generation utilities using matplotlib.
"""
import os
import io
import base64
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from django.conf import settings
from django.db import models
from equipment.models import Equipment, EquipmentReading, PlantLocation


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def save_figure_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"


def generate_flowrate_comparison_chart(equipment_queryset=None, dark_mode=False):
    """Generate flowrate comparison bar chart."""
    if equipment_queryset is None:
        equipment_queryset = Equipment.objects.filter(is_active=True)
    
    # Prepare data
    names = [eq.name for eq in equipment_queryset[:15]]  # Limit to 15 for readability
    flowrates = [eq.flowrate for eq in equipment_queryset[:15]]
    
    # Set colors based on theme
    if dark_mode:
        plt.style.use('dark_background')
        bar_color = '#3b82f6'
    else:
        plt.style.use('default')
        bar_color = '#3b82f6'
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    bars = ax.bar(range(len(names)), flowrates, color=bar_color, alpha=0.8)
    
    ax.set_xlabel('Equipment', fontsize=12, fontweight='bold')
    ax.set_ylabel('Flowrate (L/min)', fontsize=12, fontweight='bold')
    ax.set_title('Equipment Flowrate Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    return save_figure_to_base64(fig)


def generate_temperature_pressure_trends(equipment_queryset=None, dark_mode=False):
    """Generate temperature and pressure trend line chart."""
    if equipment_queryset is None:
        equipment_queryset = Equipment.objects.filter(is_active=True)
    
    # Prepare data
    names = [eq.name for eq in equipment_queryset[:15]]
    temperatures = [eq.temperature for eq in equipment_queryset[:15]]
    pressures = [eq.pressure for eq in equipment_queryset[:15]]
    
    if dark_mode:
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    # Create figure
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    x = range(len(names))
    
    # Temperature line
    ax1.plot(x, temperatures, color='#ef4444', marker='o', linewidth=2, 
             markersize=6, label='Temperature (°C)')
    ax1.set_xlabel('Equipment', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold', color='#ef4444')
    ax1.tick_params(axis='y', labelcolor='#ef4444')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right')
    
    # Pressure line on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(x, pressures, color='#10b981', marker='s', linewidth=2, 
             markersize=6, label='Pressure (bar)')
    ax2.set_ylabel('Pressure (bar)', fontsize=12, fontweight='bold', color='#10b981')
    ax2.tick_params(axis='y', labelcolor='#10b981')
    
    plt.title('Temperature & Pressure Trends', fontsize=14, fontweight='bold', pad=20)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    return save_figure_to_base64(fig)


def generate_equipment_type_distribution(dark_mode=False):
    """Generate equipment type distribution pie chart."""
    equipment_types = Equipment.objects.filter(is_active=True).values(
        'equipment_type__name'
    ).annotate(count=models.Count('id'))
    
    if not equipment_types:
        return None
    
    names = [item['equipment_type__name'] for item in equipment_types]
    counts = [item['count'] for item in equipment_types]
    
    if dark_mode:
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    wedges, texts, autotexts = ax.pie(
        counts, labels=names, autopct='%1.1f%%',
        colors=colors[:len(names)], startangle=90,
        textprops={'fontsize': 11}
    )
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return save_figure_to_base64(fig)


def generate_pressure_temperature_scatter(equipment_queryset=None, dark_mode=False):
    """Generate pressure vs temperature scatter plot."""
    if equipment_queryset is None:
        equipment_queryset = Equipment.objects.filter(is_active=True)
    
    pressures = [eq.pressure for eq in equipment_queryset]
    temperatures = [eq.temperature for eq in equipment_queryset]
    names = [eq.name for eq in equipment_queryset]
    
    if dark_mode:
        plt.style.use('dark_background')
        scatter_color = '#8b5cf6'
    else:
        plt.style.use('default')
        scatter_color = '#8b5cf6'
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter = ax.scatter(pressures, temperatures, c=scatter_color, 
                        s=100, alpha=0.6, edgecolors='white', linewidth=1.5)
    
    ax.set_xlabel('Pressure (bar)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_title('Pressure vs Temperature Correlation', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    # Add trend line
    if len(pressures) > 1:
        z = np.polyfit(pressures, temperatures, 1)
        p = np.poly1d(z)
        ax.plot(pressures, p(pressures), "r--", alpha=0.8, linewidth=2, label='Trend')
        ax.legend()
    
    plt.tight_layout()
    return save_figure_to_base64(fig)


def generate_historical_trends(equipment_id, days=7, dark_mode=False):
    """Generate historical trends for a specific equipment."""
    from django.utils import timezone
    from django.db.models import Count
    
    equipment = Equipment.objects.get(id=equipment_id)
    start_date = timezone.now() - timedelta(days=days)
    
    readings = EquipmentReading.objects.filter(
        equipment=equipment,
        timestamp__gte=start_date
    ).order_by('timestamp')
    
    if not readings.exists():
        return None
    
    timestamps = [r.timestamp for r in readings]
    flowrates = [r.flowrate for r in readings]
    pressures = [r.pressure for r in readings]
    temperatures = [r.temperature for r in readings]
    
    if dark_mode:
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
    
    # Flowrate
    ax1.plot(timestamps, flowrates, color='#3b82f6', linewidth=2)
    ax1.set_ylabel('Flowrate (L/min)', fontsize=11, fontweight='bold')
    ax1.set_title(f'Historical Trends - {equipment.name}', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Pressure
    ax2.plot(timestamps, pressures, color='#10b981', linewidth=2)
    ax2.set_ylabel('Pressure (bar)', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Temperature
    ax3.plot(timestamps, temperatures, color='#ef4444', linewidth=2)
    ax3.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Time', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return save_figure_to_base64(fig)


def generate_status_distribution(dark_mode=False):
    """Generate equipment status distribution chart."""
    from django.db.models import Count
    
    status_data = Equipment.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    if not status_data:
        return None
    
    statuses = [item['status'].title() for item in status_data]
    counts = [item['count'] for item in status_data]
    
    if dark_mode:
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    colors = {
        'Normal': '#10b981',
        'Warning': '#f59e0b',
        'Critical': '#ef4444',
        'Offline': '#6b7280'
    }
    bar_colors = [colors.get(s, '#3b82f6') for s in statuses]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(statuses, counts, color=bar_colors, alpha=0.8)
    
    ax.set_xlabel('Status', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Equipment Status Distribution', fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    return save_figure_to_base64(fig)


def generate_plant_location_comparison(dark_mode=False):
    """Generate comparison chart across plant locations."""
    from django.db.models import Count, Avg
    
    location_stats = PlantLocation.objects.annotate(
        equipment_count=Count('equipment', filter=models.Q(equipment__is_active=True)),
        avg_temperature=Avg('equipment__temperature', filter=models.Q(equipment__is_active=True)),
        avg_pressure=Avg('equipment__pressure', filter=models.Q(equipment__is_active=True))
    ).filter(equipment_count__gt=0)
    
    if not location_stats:
        return None
    
    locations = [loc.name for loc in location_stats]
    counts = [loc.equipment_count for loc in location_stats]
    
    if dark_mode:
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(locations, counts, color='#3b82f6', alpha=0.8)
    
    ax.set_xlabel('Plant Location', fontsize=12, fontweight='bold')
    ax.set_ylabel('Equipment Count', fontsize=12, fontweight='bold')
    ax.set_title('Equipment Distribution by Plant Location', fontsize=14, fontweight='bold', pad=20)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    return save_figure_to_base64(fig)
