"""
Main Application - ChemData Equipment Monitoring System
PyQt6 Desktop Application
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from styles import LIGHT_THEME, DARK_THEME
from login_page import LoginPage
from sidebar import Sidebar
from dashboard import Dashboard
from equipment import Equipment
from upload_page import UploadPage


class PlaceholderPage(QWidget):
    """Placeholder for pages not yet implemented"""
    def __init__(self, page_name: str):
        super().__init__()
        from PyQt6.QtWidgets import QVBoxLayout, QLabel
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel(page_name)
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel(f"{page_name} content coming soon...")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_logged_in = False
        self.is_dark_mode = True
        self.current_page = 'login'
        
        self.setWindowTitle("ChemData - Equipment Monitoring System")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Initialize UI
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        # Central widget with stacked layout for login/main views
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QStackedWidget()
        
        # Login page
        self.login_page = LoginPage()
        self.login_page.login_successful.connect(self.on_login_success)
        self.main_layout.addWidget(self.login_page)
        
        # Main application widget (sidebar + content)
        self.main_app_widget = QWidget()
        self.setup_main_app()
        self.main_layout.addWidget(self.main_app_widget)
        
        # Set login page as initial view
        self.main_layout.setCurrentWidget(self.login_page)
        
        # Layout for central widget
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_layout)
        self.central_widget.setLayout(layout)
    
    def setup_main_app(self):
        """Setup the main application layout with sidebar and content area"""
        app_layout = QHBoxLayout()
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.tab_changed.connect(self.on_tab_changed)
        self.sidebar.theme_toggled.connect(self.on_theme_toggle)
        app_layout.addWidget(self.sidebar)
        
        # Content area with stacked widget
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("mainContent")
        
        # Create pages
        self.dashboard_page = Dashboard()
        self.equipment_page = Equipment()
        self.upload_page = UploadPage()
        self.history_page = PlaceholderPage("History")
        self.help_page = PlaceholderPage("Help Center")
        self.settings_page = PlaceholderPage("Settings")
        
        # Add pages to stack
        self.pages = {
            'dashboard': self.dashboard_page,
            'equipment': self.equipment_page,
            'upload': self.upload_page,
            'history': self.history_page,
            'help': self.help_page,
            'settings': self.settings_page,
        }
        
        for page in self.pages.values():
            self.content_stack.addWidget(page)
        
        # Set initial page
        self.content_stack.setCurrentWidget(self.dashboard_page)
        
        app_layout.addWidget(self.content_stack, stretch=1)
        
        self.main_app_widget.setLayout(app_layout)
    
    def on_login_success(self):
        """Handle successful login"""
        self.is_logged_in = True
        # Get dark mode preference from login page
        self.is_dark_mode = self.login_page.is_dark_mode
        self.main_layout.setCurrentWidget(self.main_app_widget)
        self.apply_theme()
        
        print("[MainWindow] Login successful - loading page data...")
        self.dashboard_page.load_data()
        self.equipment_page.load_equipment()
        self.upload_page.load_history()
    
    def on_tab_changed(self, tab_id: str):
        """Handle sidebar tab changes"""
        if tab_id in self.pages:
            self.current_page = tab_id
            self.content_stack.setCurrentWidget(self.pages[tab_id])
            
        if self.is_logged_in:
            if tab_id == 'dashboard':
                self.dashboard_page.load_data()
            elif tab_id == 'equipment':
                self.equipment_page.load_equipment()
            elif tab_id == 'upload':
                self.upload_page.load_history()
                
    
    def on_theme_toggle(self, is_dark: bool):
        """Handle theme toggle"""
        self.is_dark_mode = is_dark
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        if self.is_dark_mode:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    
    # Set application-wide properties
    app.setApplicationName("ChemData")
    app.setOrganizationName("Chemical Data Solutions")
    app.setApplicationVersion("1.0.0")
    
    # Set default font
    from PyQt6.QtGui import QFont
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
