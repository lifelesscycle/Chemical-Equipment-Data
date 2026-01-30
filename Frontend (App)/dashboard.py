"""
Dashboard Page Component for ChemData Application - COMPLETE FIXED VERSION
Now includes actual charts using matplotlib!
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QComboBox, QScrollArea,
                              QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from api_service import api_service
import io
from datetime import datetime

# Try to import matplotlib for charts
try:
    import matplotlib
    matplotlib.use('Qt5Agg')  # Use Qt backend
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[Dashboard] Warning: matplotlib not available. Charts will not be displayed.")
    print("[Dashboard] Install with: pip install matplotlib")


class DataLoader(QThread):
    """Thread for loading data from API"""
    data_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, load_func, params=None):
        super().__init__()
        self.load_func = load_func
        self.params = params or {}
    
    def run(self):
        try:
            data = self.load_func(**self.params)
            self.data_loaded.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.timeframe = '24h'
        self.location = 'all'
        self.equipment_type = 'all'
        self.stats_data = None
        self.chart_data = None
        self.alerts_data = []
        self.init_ui()
        # DON'T auto-load - wait for main.py to call load_data after login
    
    def init_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Main widget for scroll area
        scroll_widget = QWidget()
        scroll_widget.setObjectName("mainContent")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Filters
        filters = self.create_filters()
        layout.addWidget(filters)
        
        # Stats grid
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(20)
        layout.addLayout(self.stats_grid)
        
        # Dashboard cards
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setSpacing(20)
        layout.addLayout(self.cards_layout)
        
        # Loading indicator
        self.loading_label = QLabel("Waiting for login...")
        self.loading_label.setObjectName("pageSubtitle")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)
        
        scroll_widget.setLayout(layout)
        scroll.setWidget(scroll_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def create_header(self):
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        
        title = QLabel("Equipment Overview")
        title.setObjectName("pageTitle")
        left_layout.addWidget(title)
        
        subtitle = QLabel("Monitor and manage your chemical processing equipment")
        subtitle.setObjectName("pageSubtitle")
        left_layout.addWidget(subtitle)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        # Right side - action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(refresh_btn)
        
        download_btn = QPushButton("📥 Download Report")
        download_btn.setObjectName("primaryButton")
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        download_btn.clicked.connect(self.download_report)
        btn_layout.addWidget(download_btn)
        
        header_layout.addLayout(btn_layout)
        
        header_widget.setLayout(header_layout)
        return header_widget
    
    def create_filters(self):
        filter_widget = QWidget()
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(16)
        
        # Timeframe filter
        timeframe_layout = QVBoxLayout()
        timeframe_layout.setSpacing(6)
        timeframe_label = QLabel("Timeframe")
        timeframe_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        timeframe_layout.addWidget(timeframe_label)
        
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['Last 24 Hours', 'Last 7 Days', 'Last 30 Days', 'Last 90 Days'])
        self.timeframe_combo.setFixedHeight(40)
        self.timeframe_combo.currentIndexChanged.connect(self.on_filter_changed)
        timeframe_layout.addWidget(self.timeframe_combo)
        
        filter_layout.addLayout(timeframe_layout)
        
        # Location filter
        location_layout = QVBoxLayout()
        location_layout.setSpacing(6)
        location_label = QLabel("Plant Location")
        location_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        location_layout.addWidget(location_label)
        
        self.location_combo = QComboBox()
        self.location_combo.addItems(['All Locations', 'North Plant', 'South Plant', 'East Plant'])
        self.location_combo.setFixedHeight(40)
        self.location_combo.currentIndexChanged.connect(self.on_filter_changed)
        location_layout.addWidget(self.location_combo)
        
        filter_layout.addLayout(location_layout)
        
        # Equipment type filter
        equipment_layout = QVBoxLayout()
        equipment_layout.setSpacing(6)
        equipment_label = QLabel("Equipment Type")
        equipment_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        equipment_layout.addWidget(equipment_label)
        
        self.equipment_combo = QComboBox()
        self.equipment_combo.addItems(['All Types', 'Reactors', 'Pumps', 'Mixers'])
        self.equipment_combo.setFixedHeight(40)
        self.equipment_combo.currentIndexChanged.connect(self.on_filter_changed)
        equipment_layout.addWidget(self.equipment_combo)
        
        filter_layout.addLayout(equipment_layout)
        
        filter_layout.addStretch()
        
        filter_widget.setLayout(filter_layout)
        return filter_widget
    
    def create_stat_card(self, label: str, value: str, unit: str = "", icon: str = "📊", color: str = "blue"):
        card = QFrame()
        card.setObjectName("statCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Header
        header_layout = QHBoxLayout()
        
        label_widget = QLabel(label)
        label_widget.setObjectName("statLabel")
        header_layout.addWidget(label_widget)
        
        header_layout.addStretch()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        layout.addLayout(header_layout)
        
        # Value
        value_layout = QHBoxLayout()
        value_layout.setSpacing(4)
        
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_layout.addWidget(value_label)
        
        if unit:
            unit_label = QLabel(unit)
            unit_label.setObjectName("statUnit")
            value_layout.addWidget(unit_label)
        
        value_layout.addStretch()
        layout.addLayout(value_layout)
        
        card.setLayout(layout)
        return card
    
    def create_dashboard_card(self, title: str, content_widget: QWidget):
        card = QFrame()
        card.setObjectName("dashboardCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Content
        layout.addWidget(content_widget)
        
        card.setLayout(layout)
        return card
    
    def create_chart_widget(self, equipment_data: list):
        """Create charts showing equipment metrics"""
        if not MATPLOTLIB_AVAILABLE:
            # Show message if matplotlib not installed
            no_chart = QLabel("📊 Charts require matplotlib\nInstall with: pip install matplotlib")
            no_chart.setStyleSheet("font-size: 14px; color: #6b7280; padding: 40px;")
            no_chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return no_chart
        
        if not equipment_data or len(equipment_data) == 0:
            no_data = QLabel("No data available for charts")
            no_data.setStyleSheet("font-size: 14px; color: #6b7280; padding: 40px;")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return no_data
        
        # Create matplotlib figure with white background
        fig = Figure(figsize=(14, 5), facecolor='#ffffff', dpi=100)
        
        # Create 3 subplots for different metrics
        ax1 = fig.add_subplot(131)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)
        
        # Extract data (limit to 10 for readability)
        equipment_subset = equipment_data[:10]
        names = [eq.get('name', f"Equip-{i}") for i, eq in enumerate(equipment_subset)]
        flowrates = [eq.get('flowrate', 0) for eq in equipment_subset]
        pressures = [eq.get('pressure', 0) for eq in equipment_subset]
        temps = [eq.get('temperature', 0) for eq in equipment_subset]
        
        # Style settings
        text_color = '#1f2937'
        grid_color = '#e5e7eb'
        
        # Plot 1: Flowrate
        ax1.barh(names, flowrates, color='#3b82f6', alpha=0.8)
        ax1.set_xlabel('Flowrate (L/min)', color=text_color, fontsize=10)
        ax1.set_title('Equipment Flowrates', color=text_color, fontsize=11, fontweight='bold', pad=10)
        ax1.tick_params(colors=text_color, labelsize=8)
        ax1.set_facecolor('#ffffff')
        ax1.grid(True, alpha=0.3, color=grid_color, axis='x')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Plot 2: Pressure
        ax2.barh(names, pressures, color='#10b981', alpha=0.8)
        ax2.set_xlabel('Pressure (bar)', color=text_color, fontsize=10)
        ax2.set_title('Equipment Pressure', color=text_color, fontsize=11, fontweight='bold', pad=10)
        ax2.tick_params(colors=text_color, labelsize=8)
        ax2.set_facecolor('#ffffff')
        ax2.grid(True, alpha=0.3, color=grid_color, axis='x')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # Plot 3: Temperature
        ax3.barh(names, temps, color='#f59e0b', alpha=0.8)
        ax3.set_xlabel('Temperature (°C)', color=text_color, fontsize=10)
        ax3.set_title('Equipment Temperature', color=text_color, fontsize=11, fontweight='bold', pad=10)
        ax3.tick_params(colors=text_color, labelsize=8)
        ax3.set_facecolor('#ffffff')
        ax3.grid(True, alpha=0.3, color=grid_color, axis='x')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        
        # Adjust layout to prevent label cutoff
        fig.tight_layout(pad=2.0)
        
        # Create canvas widget with fixed size
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        canvas.setMaximumHeight(500)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        return canvas
    
    def on_filter_changed(self):
        # Map combo box selections to API parameters
        timeframe_map = {0: '24h', 1: '7d', 2: '30d', 3: '90d'}
        location_map = {0: 'all', 1: 'north', 2: 'south', 3: 'east'}
        equipment_map = {0: 'all', 1: 'reactors', 2: 'pumps', 3: 'mixers'}
        
        self.timeframe = timeframe_map.get(self.timeframe_combo.currentIndex(), '24h')
        self.location = location_map.get(self.location_combo.currentIndex(), 'all')
        self.equipment_type = equipment_map.get(self.equipment_combo.currentIndex(), 'all')
        
        self.load_data()
    
    def load_data(self):
        """Load dashboard data from API"""
        self.loading_label.setText("Loading dashboard data...")
        self.loading_label.show()
        
        # Prepare filters
        params = {'timeframe': self.timeframe}
        if self.location != 'all':
            params['location'] = self.location
        if self.equipment_type != 'all':
            params['equipment_type'] = self.equipment_type
        
        # Load stats - wrap in 'params' key for the method
        self.stats_loader = DataLoader(api_service.get_dashboard_stats, {'params': params})
        self.stats_loader.data_loaded.connect(self.on_stats_loaded)
        self.stats_loader.error_occurred.connect(self.on_error)
        self.stats_loader.start()
        
        # Load alerts - wrap in 'filters' key for the method
        alert_params = {'filters': {'severity': 'critical', 'limit': 5}}
        self.alerts_loader = DataLoader(api_service.get_alerts, alert_params)
        self.alerts_loader.data_loaded.connect(self.on_alerts_loaded)
        self.alerts_loader.error_occurred.connect(self.on_error)
        self.alerts_loader.start()
        
        # Load equipment for charts - wrap in 'filters' key for the method
        self.equipment_loader = DataLoader(api_service.get_equipment, {'filters': params})
        self.equipment_loader.data_loaded.connect(self.on_equipment_loaded)
        self.equipment_loader.start()
    
    def on_stats_loaded(self, data: dict):
        """Handle loaded statistics data"""
        if not data or not isinstance(data, dict):
            self.on_error("Invalid data received from server")
            return
        
        self.stats_data = data
        self.loading_label.hide()
        self.update_stats_display()
    
    def on_alerts_loaded(self, data: dict):
        """Handle loaded alerts data"""
        self.alerts_data = data.get('results', data) if isinstance(data, dict) else data
        self.update_alerts_display()
    
    def on_equipment_loaded(self, data: dict):
        """Handle loaded equipment data for charts"""
        if isinstance(data, dict):
            equipment_list = data.get('results', [])
        elif isinstance(data, list):
            equipment_list = data
        else:
            equipment_list = []
        
        self.update_charts_display(equipment_list)
    
    def on_error(self, error_msg: str):
        """Handle error loading data"""
        self.loading_label.hide()
        
        # Clear stats grid - SAFE VERSION
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Show error card
        error_widget = QWidget()
        error_layout = QVBoxLayout()
        error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.setSpacing(12)
        
        icon = QLabel("⚠️")
        icon.setStyleSheet("font-size: 48px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(icon)
        
        title = QLabel("Dashboard Unavailable")
        title.setObjectName("pageTitle")
        title.setStyleSheet("color: #dc2626;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(title)
        
        detail = QLabel(error_msg)
        detail.setObjectName("pageSubtitle")
        detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail.setWordWrap(True)
        error_layout.addWidget(detail)
        
        retry_btn = QPushButton("🔄 Reload Dashboard")
        retry_btn.setObjectName("primaryButton")
        retry_btn.clicked.connect(self.load_data)
        retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        error_layout.addWidget(retry_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        error_widget.setLayout(error_layout)
        self.stats_grid.addWidget(error_widget, 0, 0, 1, 4)
    
    def update_stats_display(self):
        """Update statistics display - FIXED VERSION"""
        if not self.stats_data:
            return
        
        # Clear existing stats - SAFE VERSION
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Total Equipment
        total_equipment = self.stats_data.get('total_equipment', 0)
        stat1 = self.create_stat_card("Total Equipment", str(total_equipment), "", "🏭", "blue")
        self.stats_grid.addWidget(stat1, 0, 0)
        
        # Avg Pressure
        avg_pressure = self.stats_data.get('avg_pressure', 0)
        stat2 = self.create_stat_card("Avg Pressure", f"{avg_pressure:.1f}", "bar", "📊", "purple")
        self.stats_grid.addWidget(stat2, 0, 1)
        
        # Avg Temperature
        avg_temp = self.stats_data.get('avg_temperature', 0)
        stat3 = self.create_stat_card("Avg Temperature", f"{avg_temp:.1f}", "°C", "🌡️", "orange")
        self.stats_grid.addWidget(stat3, 0, 2)
        
        # Max Flowrate
        max_flowrate = self.stats_data.get('max_flowrate', 0)
        stat4 = self.create_stat_card("Max Flowrate", f"{max_flowrate:.1f}", "L/min", "💧", "teal")
        self.stats_grid.addWidget(stat4, 0, 3)
        
        # Clear cards layout once at the beginning
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Equipment status card
        self.update_equipment_status()
    
    def update_equipment_status(self):
        """Update equipment status display - FIXED VERSION"""
        if not self.stats_data:
            return
        
        # DON'T clear - just add the card
        # Equipment Status
        status_widget = QWidget()
        status_layout = QVBoxLayout()
        status_layout.setSpacing(12)
        
        normal_count = self.stats_data.get('normal_count', 0)
        warning_count = self.stats_data.get('warning_count', 0)
        critical_count = self.stats_data.get('critical_count', 0)
        
        status_items = [
            ("Normal", normal_count, "#10b981"),
            ("Warning", warning_count, "#f59e0b"),
            ("Critical", critical_count, "#ef4444"),
        ]
        
        for status_label, count, color in status_items:
            item_layout = QHBoxLayout()
            
            indicator = QLabel("●")
            indicator.setStyleSheet(f"color: {color}; font-size: 16px;")
            item_layout.addWidget(indicator)
            
            label = QLabel(status_label)
            label.setStyleSheet("font-size: 14px;")
            item_layout.addWidget(label)
            
            item_layout.addStretch()
            
            count_label = QLabel(str(count))
            count_label.setStyleSheet("font-size: 18px; font-weight: 700;")
            item_layout.addWidget(count_label)
            
            status_layout.addLayout(item_layout)
        
        status_widget.setLayout(status_layout)
        
        status_card = self.create_dashboard_card("Equipment Status", status_widget)
        self.cards_layout.addWidget(status_card)
    
    def update_charts_display(self, equipment_data: list):
        """Update charts display"""
        chart_widget = self.create_chart_widget(equipment_data)
        chart_card = self.create_dashboard_card("Equipment Metrics Overview", chart_widget)
        self.cards_layout.addWidget(chart_card)
    
    def update_alerts_display(self):
        """Update alerts display - FIXED VERSION"""
        # Always show alerts card, even if no data
        
        # Alerts card
        alerts_widget = QWidget()
        alerts_layout = QVBoxLayout()
        alerts_layout.setSpacing(12)
        
        if self.alerts_data and isinstance(self.alerts_data, list) and len(self.alerts_data) > 0:
            for alert in self.alerts_data[:5]:
                alert_item = QFrame()
                alert_item.setStyleSheet("""
                    QFrame {
                        background-color: rgba(239, 68, 68, 0.1);
                        border-left: 3px solid #ef4444;
                        border-radius: 8px;
                        padding: 12px;
                    }
                """)
                
                alert_layout = QHBoxLayout()
                
                icon_label = QLabel("⚠️")
                icon_label.setStyleSheet("font-size: 20px;")
                alert_layout.addWidget(icon_label)
                
                info_layout = QVBoxLayout()
                info_layout.setSpacing(4)
                
                message = alert.get('message', alert.get('title', 'Alert'))
                message_label = QLabel(message)
                message_label.setStyleSheet("font-size: 14px; font-weight: 600;")
                info_layout.addWidget(message_label)
                
                equipment_name = alert.get('equipment_name', 'Unknown')
                created_at = alert.get('created_at', '')
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        time_str = dt.strftime('%b %d, %Y %I:%M %p')
                    except:
                        time_str = created_at
                else:
                    time_str = 'Unknown time'
                
                meta_label = QLabel(f"{equipment_name} • {time_str}")
                meta_label.setStyleSheet("font-size: 12px; color: #6b7280;")
                info_layout.addWidget(meta_label)
                
                alert_layout.addLayout(info_layout)
                alert_layout.addStretch()
                
                alert_item.setLayout(alert_layout)
                alerts_layout.addWidget(alert_item)
        else:
            no_alerts = QLabel("✅ No critical alerts at this time")
            no_alerts.setStyleSheet("font-size: 14px; color: #10b981; padding: 20px;")
            no_alerts.setAlignment(Qt.AlignmentFlag.AlignCenter)
            alerts_layout.addWidget(no_alerts)
        
        alerts_widget.setLayout(alerts_layout)
        
        alerts_card = self.create_dashboard_card("Recent Alerts", alerts_widget)
        self.cards_layout.addWidget(alerts_card)
    
    def download_report(self):
        """Download dashboard report"""
        try:
            print("📥 Downloading report...")
            # In a real implementation, this would:
            # 1. Call api_service.download_report()
            # 2. Open file dialog to save
            # 3. Write the file
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Download", "Report download feature coming soon!")
        except Exception as e:
            print(f"Download failed: {e}")
