"""
Equipment Page Component for ChemData Application - COMPLETE FIXED VERSION
Now includes working Analytics Charts view!
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QLineEdit, QScrollArea,
                              QGridLayout, QSizePolicy, QButtonGroup)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from api_service import api_service
import requests

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
    print("[Equipment] Warning: matplotlib not available. Charts will not be displayed.")


class EquipmentLoader(QThread):
    """Thread for loading equipment data"""
    data_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            data = api_service.get_equipment()
            
            # Handle both list and dict with 'results' key
            if isinstance(data, dict):
                equipment_list = data.get('results', [])
                if not isinstance(equipment_list, list):
                    self.error_occurred.emit("Invalid response format from server")
                    return
            elif isinstance(data, list):
                equipment_list = data
            else:
                self.error_occurred.emit(f"Unexpected data type: {type(data)}")
                return
            
            self.data_loaded.emit(equipment_list)
            
        except requests.ConnectionError:
            self.error_occurred.emit("Cannot connect to backend server. Please ensure it's running at localhost:8000")
        except requests.Timeout:
            self.error_occurred.emit("Request timed out. The server may be slow or unresponsive")
        except Exception as e:
            error_msg = str(e)
            if "Authentication failed" in error_msg or "401" in error_msg:
                self.error_occurred.emit("Session expired. Please log in again")
            else:
                self.error_occurred.emit(error_msg)


class Equipment(QWidget):
    def __init__(self):
        super().__init__()
        self.equipment_data = []
        self.filtered_data = []
        self.search_term = ""
        self.view_mode = "grid"
        self.init_ui()
        # DON'T auto-load - wait for main.py to call load_equipment after login
    
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
        
        # Search bar
        search_widget = self.create_search_bar()
        layout.addWidget(search_widget)
        
        # Stats summary
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        layout.addLayout(self.stats_layout)
        
        # View toggle
        toggle_widget = self.create_view_toggle()
        layout.addWidget(toggle_widget)
        
        # Equipment grid container
        self.equipment_container = QWidget()
        self.equipment_grid = QGridLayout()
        self.equipment_grid.setSpacing(20)
        self.equipment_container.setLayout(self.equipment_grid)
        layout.addWidget(self.equipment_container)
        
        # Charts container (hidden by default)
        self.charts_container = QWidget()
        self.charts_layout = QVBoxLayout()
        self.charts_layout.setSpacing(20)
        self.charts_container.setLayout(self.charts_layout)
        self.charts_container.hide()
        layout.addWidget(self.charts_container)
        
        # Loading indicator
        self.loading_label = QLabel("Waiting for login...")
        self.loading_label.setObjectName("pageSubtitle")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)
        
        layout.addStretch()
        
        scroll_widget.setLayout(layout)
        scroll.setWidget(scroll_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def create_search_bar(self):
        search_widget = QWidget()
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Search equipment by name or type...")
        self.search_input.setFixedHeight(44)
        self.search_input.textChanged.connect(self.on_search_changed)
        
        search_layout.addWidget(self.search_input)
        
        search_widget.setLayout(search_layout)
        return search_widget
    
    def create_view_toggle(self):
        toggle_widget = QWidget()
        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(12)
        
        self.grid_btn = QPushButton("📊 Equipment Grid")
        self.grid_btn.setObjectName("primaryButton")
        self.grid_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid_btn.clicked.connect(lambda: self.set_view_mode("grid"))
        toggle_layout.addWidget(self.grid_btn)
        
        self.charts_btn = QPushButton("📈 Analytics Charts")
        self.charts_btn.setObjectName("secondaryButton")
        self.charts_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.charts_btn.clicked.connect(lambda: self.set_view_mode("charts"))
        toggle_layout.addWidget(self.charts_btn)
        
        toggle_layout.addStretch()
        
        toggle_widget.setLayout(toggle_layout)
        return toggle_widget
    
    def create_stat_card(self, label: str, value: str, icon: str, color: str = "#3b82f6"):
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumWidth(200)
        
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
        icon_label.setStyleSheet(f"font-size: 32px; color: {color};")
        header_layout.addWidget(icon_label)
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def create_equipment_card(self, equipment: dict):
        card = QFrame()
        card.setObjectName("equipmentCard")
        card.setMinimumWidth(300)
        card.setMaximumWidth(400)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header with name and status
        header_layout = QHBoxLayout()
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name = equipment.get('name', 'Unknown')
        name_label = QLabel(name)
        name_label.setObjectName("equipmentName")
        info_layout.addWidget(name_label)
        
        eq_type = equipment.get('type', equipment.get('equipment_type_name', 'Unknown'))
        type_label = QLabel(eq_type)
        type_label.setObjectName("equipmentType")
        info_layout.addWidget(type_label)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        # Status badge
        status = self.check_status(equipment)
        status_badge = QLabel(status.capitalize())
        status_badge.setObjectName(f"status{status.capitalize()}Badge")
        status_badge.setFixedHeight(24)
        status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(status_badge)
        
        layout.addLayout(header_layout)
        
        # Metrics
        metrics_layout = QVBoxLayout()
        metrics_layout.setSpacing(8)
        
        flowrate = equipment.get('flowrate', 0)
        flowrate_row = self.create_metric_row("💧 Flowrate", f"{flowrate} L/min")
        metrics_layout.addLayout(flowrate_row)
        
        pressure = equipment.get('pressure', 0)
        pressure_row = self.create_metric_row("📊 Pressure", f"{pressure} bar")
        metrics_layout.addLayout(pressure_row)
        
        temperature = equipment.get('temperature', 0)
        temp_row = self.create_metric_row("🌡️ Temperature", f"{temperature}°C")
        metrics_layout.addLayout(temp_row)
        
        layout.addLayout(metrics_layout)
        
        card.setLayout(layout)
        return card
    
    def create_metric_row(self, label: str, value: str):
        row_layout = QHBoxLayout()
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 13px; color: #9ca3af;")
        row_layout.addWidget(label_widget)
        
        row_layout.addStretch()
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet("font-size: 13px; font-weight: 600;")
        row_layout.addWidget(value_widget)
        
        return row_layout
    
    def check_status(self, equipment: dict) -> str:
        """Check equipment status based on readings"""
        # Default safe ranges by equipment type
        default_ranges = {
            'Compressor': {
                'flowrate': (80, 120),
                'pressure': (5, 12),
                'temperature': (90, 140)
            },
            'Condenser': {
                'flowrate': (140, 180),
                'pressure': (4, 11),
                'temperature': (100, 150)
            },
            'HeatExchanger': {
                'flowrate': (130, 160),
                'pressure': (6, 13),
                'temperature': (110, 145)
            },
            'Pump': {
                'flowrate': (110, 140),
                'pressure': (5, 10),
                'temperature': (100, 135)
            },
            'Reactor': {
                'flowrate': (120, 150),
                'pressure': (7, 14),
                'temperature': (120, 145)
            },
            'Valve': {
                'flowrate': (50, 80),
                'pressure': (3, 8),
                'temperature': (90, 120)
            }
        }
        
        eq_type = equipment.get('type', equipment.get('equipment_type_name', 'Unknown'))
        ranges = default_ranges.get(eq_type)
        
        if not ranges:
            return 'normal'
        
        flowrate = equipment.get('flowrate', 0)
        pressure = equipment.get('pressure', 0)
        temperature = equipment.get('temperature', 0)
        
        flowrate_ok = ranges['flowrate'][0] <= flowrate <= ranges['flowrate'][1]
        pressure_ok = ranges['pressure'][0] <= pressure <= ranges['pressure'][1]
        temp_ok = ranges['temperature'][0] <= temperature <= ranges['temperature'][1]
        
        return 'normal' if (flowrate_ok and pressure_ok and temp_ok) else 'warning'
    
    def load_equipment(self):
        """Load equipment data from API"""
        self.loading_label.setText("Loading equipment data...")
        self.loading_label.show()
        self.equipment_container.hide()
        self.charts_container.hide()
        
        self.loader = EquipmentLoader()
        self.loader.data_loaded.connect(self.on_equipment_loaded)
        self.loader.error_occurred.connect(self.on_error)
        self.loader.start()
    
    def on_equipment_loaded(self, data: list):
        """Handle successfully loaded equipment data"""
        self.equipment_data = data
        self.filtered_data = data
        self.loading_label.hide()
        
        if not data or len(data) == 0:
            self.show_empty_state()
        else:
            self.update_stats()
            if self.view_mode == "grid":
                self.equipment_container.show()
                self.update_equipment_grid()
            else:
                self.charts_container.show()
                self.update_charts_view()
    
    def on_error(self, error_msg: str):
        """Handle error loading equipment data"""
        self.loading_label.hide()
        self.equipment_container.hide()
        self.charts_container.hide()
        
        # Clear existing widgets - SAFE VERSION
        while self.equipment_grid.count():
            item = self.equipment_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create error display
        error_container = QWidget()
        error_layout = QVBoxLayout()
        error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.setSpacing(20)
        
        # Error icon
        error_icon = QLabel("⚠️")
        error_icon.setStyleSheet("font-size: 64px;")
        error_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(error_icon)
        
        # Error title
        error_title = QLabel("Failed to Load Equipment Data")
        error_title.setObjectName("pageTitle")
        error_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_title.setStyleSheet("color: #dc2626;")
        error_layout.addWidget(error_title)
        
        # Error message
        error_detail = QLabel(error_msg)
        error_detail.setObjectName("pageSubtitle")
        error_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_detail.setWordWrap(True)
        error_detail.setMaximumWidth(500)
        error_layout.addWidget(error_detail)
        
        # Retry button
        retry_btn = QPushButton("🔄 Retry Loading")
        retry_btn.setObjectName("primaryButton")
        retry_btn.setFixedWidth(200)
        retry_btn.setFixedHeight(44)
        retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        retry_btn.clicked.connect(self.load_equipment)
        error_layout.addWidget(retry_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Help text
        help_text = QLabel("💡 Make sure you're logged in and the backend server is running")
        help_text.setStyleSheet("font-size: 12px; color: #6b7280; margin-top: 12px;")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(help_text)
        
        error_container.setLayout(error_layout)
        self.equipment_grid.addWidget(error_container, 0, 0, 1, 3)
        self.equipment_container.show()
    
    def show_empty_state(self):
        """Show friendly empty state"""
        # Clear existing widgets - SAFE VERSION
        while self.equipment_grid.count():
            item = self.equipment_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        empty_container = QWidget()
        empty_layout = QVBoxLayout()
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.setSpacing(16)
        
        icon = QLabel("📭")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(icon)
        
        title = QLabel("No Equipment Found")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(title)
        
        subtitle = QLabel("There is no equipment data available.\nTry uploading data or clearing your search filters.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setMaximumWidth(400)
        empty_layout.addWidget(subtitle)
        
        empty_container.setLayout(empty_layout)
        self.equipment_grid.addWidget(empty_container, 0, 0, 1, 3)
        self.equipment_container.show()
    
    def on_search_changed(self, text: str):
        """Handle search input changes"""
        self.search_term = text.lower()
        self.filter_equipment()
        if self.view_mode == "grid":
            self.update_equipment_grid()
        else:
            self.update_charts_view()
    
    def filter_equipment(self):
        """Filter equipment based on search term"""
        if not self.search_term:
            self.filtered_data = self.equipment_data
        else:
            self.filtered_data = [
                eq for eq in self.equipment_data
                if self.search_term in eq.get('name', '').lower() or
                   self.search_term in eq.get('type', '').lower() or
                   self.search_term in eq.get('equipment_type_name', '').lower()
            ]
    
    def update_stats(self):
        """Update statistics cards - FIXED VERSION"""
        # Clear existing stats - SAFE VERSION
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        total = len(self.equipment_data)
        normal = sum(1 for eq in self.equipment_data if self.check_status(eq) == 'normal')
        warning = total - normal
        
        stat1 = self.create_stat_card("Total Equipment", str(total), "🏭", "#3b82f6")
        self.stats_layout.addWidget(stat1)
        
        stat2 = self.create_stat_card("Normal Status", str(normal), "✅", "#10b981")
        self.stats_layout.addWidget(stat2)
        
        stat3 = self.create_stat_card("Warnings", str(warning), "⚠️", "#f59e0b")
        self.stats_layout.addWidget(stat3)
        
        self.stats_layout.addStretch()
    
    def update_equipment_grid(self):
        """Update equipment grid - FIXED VERSION"""
        # Clear existing equipment cards - SAFE VERSION
        while self.equipment_grid.count():
            item = self.equipment_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.filtered_data:
            no_results = QLabel("No equipment found matching your search.")
            no_results.setObjectName("pageSubtitle")
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.equipment_grid.addWidget(no_results, 0, 0, 1, 3)
            return
        
        # Add equipment cards in grid layout (3 columns)
        for idx, equipment in enumerate(self.filtered_data):
            card = self.create_equipment_card(equipment)
            row = idx // 3
            col = idx % 3
            self.equipment_grid.addWidget(card, row, col)
    
    def create_chart_card(self, title: str, chart_widget):
        """Create a card for a chart"""
        card = QFrame()
        card.setObjectName("dashboardCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)
        
        # Chart
        layout.addWidget(chart_widget)
        
        card.setLayout(layout)
        return card
    
    def update_charts_view(self):
        """Update charts view with analytics - FULLY IMPLEMENTED"""
        # Clear existing charts
        while self.charts_layout.count():
            item = self.charts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not MATPLOTLIB_AVAILABLE:
            no_matplotlib = QLabel("📊 Analytics Charts require matplotlib\nInstall with: pip install matplotlib")
            no_matplotlib.setStyleSheet("font-size: 16px; color: #6b7280; padding: 60px;")
            no_matplotlib.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.charts_layout.addWidget(no_matplotlib)
            return
        
        if not self.filtered_data:
            no_data = QLabel("No equipment data available for charts")
            no_data.setStyleSheet("font-size: 16px; color: #6b7280; padding: 60px;")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.charts_layout.addWidget(no_data)
            return
        
        # Create charts
        # Chart 1: Flowrate Comparison
        flowrate_chart = self.create_flowrate_chart()
        flowrate_card = self.create_chart_card("Flowrate Comparison", flowrate_chart)
        self.charts_layout.addWidget(flowrate_card)
        
        # Chart 2: Temperature & Pressure Trends
        temp_pressure_chart = self.create_temp_pressure_chart()
        temp_pressure_card = self.create_chart_card("Temperature & Pressure Trends", temp_pressure_chart)
        self.charts_layout.addWidget(temp_pressure_card)
        
        # Chart 3: Equipment Type Distribution
        charts_row = QHBoxLayout()
        charts_row.setSpacing(20)
        
        type_dist_chart = self.create_type_distribution_chart()
        type_dist_card = self.create_chart_card("Equipment Type Distribution", type_dist_chart)
        charts_row.addWidget(type_dist_card)
        
        # Chart 4: Pressure vs Temperature Correlation
        correlation_chart = self.create_correlation_chart()
        correlation_card = self.create_chart_card("Pressure vs Temperature Correlation", correlation_chart)
        charts_row.addWidget(correlation_card)
        
        self.charts_layout.addLayout(charts_row)
    
    def create_flowrate_chart(self):
        """Create flowrate comparison bar chart"""
        fig = Figure(figsize=(12, 5), facecolor='#ffffff', dpi=100)
        ax = fig.add_subplot(111)
        
        # Get equipment names and flowrates
        names = [eq.get('name', f"Eq-{i}") for i, eq in enumerate(self.filtered_data)]
        flowrates = [eq.get('flowrate', 0) for eq in self.filtered_data]
        
        # Create bar chart
        bars = ax.bar(names, flowrates, color='#3b82f6', alpha=0.8, edgecolor='white', linewidth=0.5)
        
        ax.set_ylabel('L/min', fontsize=11, fontweight='600')
        ax.set_title('Flowrate Comparison', fontsize=13, fontweight='bold', pad=15)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_facecolor('#ffffff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout(pad=1.5)
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        canvas.setMaximumHeight(500)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return canvas
    
    def create_temp_pressure_chart(self):
        """Create temperature and pressure line chart"""
        fig = Figure(figsize=(12, 5), facecolor='#ffffff', dpi=100)
        ax = fig.add_subplot(111)
        
        # Create secondary y-axis
        ax2 = ax.twinx()
        
        # Get data
        names = [eq.get('name', f"Eq-{i}") for i, eq in enumerate(self.filtered_data)]
        temps = [eq.get('temperature', 0) for eq in self.filtered_data]
        pressures = [eq.get('pressure', 0) for eq in self.filtered_data]
        
        x_pos = range(len(names))
        
        # Plot lines
        line1 = ax.plot(x_pos, pressures, 'o-', color='#10b981', linewidth=2.5, 
                        markersize=7, label='Pressure (bar)', alpha=0.9, markeredgecolor='white', markeredgewidth=1)
        line2 = ax2.plot(x_pos, temps, 's-', color='#ef4444', linewidth=2.5, 
                         markersize=7, label='Temperature (°C)', alpha=0.9, markeredgecolor='white', markeredgewidth=1)
        
        # Labels
        ax.set_xlabel('Equipment', fontsize=11, fontweight='600')
        ax.set_ylabel('Pressure (bar)', color='#10b981', fontsize=11, fontweight='600')
        ax2.set_ylabel('Temperature (°C)', color='#ef4444', fontsize=11, fontweight='600')
        ax.set_title('Temperature & Pressure Trends', fontsize=13, fontweight='bold', pad=15)
        
        # Ticks
        ax.set_xticks(x_pos)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax.tick_params(axis='y', labelcolor='#10b981', labelsize=10)
        ax2.tick_params(axis='y', labelcolor='#ef4444', labelsize=10)
        
        # Grid and legend
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        
        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left', fontsize=10, framealpha=0.9)
        
        fig.tight_layout(pad=1.5)
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        canvas.setMaximumHeight(500)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return canvas
    
    def create_type_distribution_chart(self):
        """Create pie chart for equipment type distribution"""
        fig = Figure(figsize=(6, 5), facecolor='#ffffff', dpi=100)
        ax = fig.add_subplot(111)
        
        # Count equipment by type
        type_counts = {}
        for eq in self.filtered_data:
            eq_type = eq.get('type', eq.get('equipment_type_name', 'Unknown'))
            type_counts[eq_type] = type_counts.get(eq_type, 0) + 1
        
        # Prepare data
        labels = list(type_counts.keys())
        sizes = list(type_counts.values())
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%',
                                           colors=colors[:len(labels)], startangle=90,
                                           textprops={'fontsize': 10, 'fontweight': '600'},
                                           pctdistance=0.85)
        
        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # Make labels bold
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('600')
        
        ax.set_title('Equipment Type Distribution', fontsize=13, fontweight='bold', pad=15)
        
        fig.tight_layout(pad=1.5)
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(380)
        canvas.setMaximumHeight(450)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return canvas
    
    def create_correlation_chart(self):
        """Create scatter plot for pressure vs temperature correlation"""
        fig = Figure(figsize=(6, 5), facecolor='#ffffff', dpi=100)
        ax = fig.add_subplot(111)
        
        # Get data
        pressures = [eq.get('pressure', 0) for eq in self.filtered_data]
        temps = [eq.get('temperature', 0) for eq in self.filtered_data]
        
        # Create scatter plot with different colors by equipment type
        type_colors = {}
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
        color_idx = 0
        
        for eq in self.filtered_data:
            eq_type = eq.get('type', eq.get('equipment_type_name', 'Unknown'))
            if eq_type not in type_colors:
                type_colors[eq_type] = colors[color_idx % len(colors)]
                color_idx += 1
        
        # Plot points colored by type
        for eq_type in type_colors:
            type_pressures = []
            type_temps = []
            for eq in self.filtered_data:
                if eq.get('type', eq.get('equipment_type_name', 'Unknown')) == eq_type:
                    type_pressures.append(eq.get('pressure', 0))
                    type_temps.append(eq.get('temperature', 0))
            
            ax.scatter(type_pressures, type_temps, c=type_colors[eq_type], 
                      label=eq_type, alpha=0.8, s=100, edgecolors='white', linewidth=1.5)
        
        ax.set_xlabel('Pressure (bar)', fontsize=11, fontweight='600')
        ax.set_ylabel('Temperature (°C)', fontsize=11, fontweight='600')
        ax.set_title('Pressure vs Temperature Correlation', fontsize=13, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=9, loc='best', framealpha=0.9)
        ax.tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout(pad=1.5)
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(380)
        canvas.setMaximumHeight(450)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return canvas
    
    def set_view_mode(self, mode: str):
        """Change view mode between grid and charts"""
        self.view_mode = mode
        
        if mode == "grid":
            self.grid_btn.setObjectName("primaryButton")
            self.charts_btn.setObjectName("secondaryButton")
            self.charts_container.hide()
            self.equipment_container.show()
            if self.filtered_data:
                self.update_equipment_grid()
        else:
            self.grid_btn.setObjectName("secondaryButton")
            self.charts_btn.setObjectName("primaryButton")
            self.equipment_container.hide()
            self.charts_container.show()
            if self.filtered_data:
                self.update_charts_view()
        
        # Force style refresh
        self.grid_btn.style().unpolish(self.grid_btn)
        self.grid_btn.style().polish(self.grid_btn)
        self.charts_btn.style().unpolish(self.charts_btn)
        self.charts_btn.style().polish(self.charts_btn)
