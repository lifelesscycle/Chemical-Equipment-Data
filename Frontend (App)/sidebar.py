"""
Sidebar Component for ChemData Application
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon


class Sidebar(QWidget):
    tab_changed = pyqtSignal(str)
    theme_toggled = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(260)
        self.active_tab = 'dashboard'
        self.nav_buttons = {}
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)
        
        # Logo
        logo_widget = self.create_logo()
        layout.addWidget(logo_widget)
        
        layout.addSpacing(20)
        
        # Navigation menu
        nav_items = [
            {'id': 'dashboard', 'label': 'Dashboard', 'icon': '📊'},
            {'id': 'equipment', 'label': 'Equipment', 'icon': '🏭'},
            {'id': 'upload', 'label': 'Upload Data', 'icon': '📤'},
            {'id': 'history', 'label': 'History', 'icon': '🕐'},
        ]
        
        for item in nav_items:
            btn = self.create_nav_button(item['id'], item['label'], item['icon'])
            self.nav_buttons[item['id']] = btn
            layout.addWidget(btn)
        
        layout.addSpacing(20)
        
        # Support section
        support_label = QLabel("SUPPORT")
        support_label.setObjectName("sectionLabel")
        layout.addWidget(support_label)
        
        support_items = [
            {'id': 'help', 'label': 'Help Center', 'icon': '❓'},
            {'id': 'settings', 'label': 'Settings', 'icon': '⚙️'},
        ]
        
        for item in support_items:
            btn = self.create_nav_button(item['id'], item['label'], item['icon'])
            self.nav_buttons[item['id']] = btn
            layout.addWidget(btn)
        
        # Spacer to push user profile to bottom
        layout.addStretch()
        
        # User profile
        profile_widget = self.create_user_profile()
        layout.addWidget(profile_widget)
        
        # Theme toggle
        self.theme_button = QPushButton("☀️")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 8px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
        # Set initial active state
        self.set_active_tab('dashboard')
    
    def create_logo(self):
        logo_widget = QWidget()
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(12, 0, 0, 0)
        logo_layout.setSpacing(12)
        
        # Logo icon (using emoji for simplicity)
        logo_icon = QLabel("⚡")
        logo_icon.setStyleSheet("""
            QLabel {
                background-color: #DC2626;
                color: white;
                font-size: 20px;
                padding: 8px;
                border-radius: 7px;
            }
        """)
        logo_icon.setFixedSize(36, 36)
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_icon)
        
        # Logo text
        logo_text = QLabel("CHEMDATA")
        logo_text.setObjectName("logoText")
        logo_layout.addWidget(logo_text)
        
        logo_layout.addStretch()
        logo_widget.setLayout(logo_layout)
        
        return logo_widget
    
    def create_nav_button(self, btn_id: str, label: str, icon: str):
        button = QPushButton()
        button.setObjectName("navButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Create layout for button content
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(12)
        
        # Icon label
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px;")
        btn_layout.addWidget(icon_label)
        
        # Text label
        text_label = QLabel(label)
        btn_layout.addWidget(text_label)
        
        btn_layout.addStretch()
        
        # Set layout to button
        button.setLayout(btn_layout)
        button.setFixedHeight(44)
        
        # Connect click event
        button.clicked.connect(lambda: self.on_nav_click(btn_id))
        
        return button
    
    def create_user_profile(self):
        profile_widget = QWidget()
        profile_widget.setObjectName("userProfile")
        
        profile_layout = QHBoxLayout()
        profile_layout.setContentsMargins(12, 12, 12, 12)
        profile_layout.setSpacing(12)
        
        # Avatar
        avatar = QLabel("DS")
        avatar.setStyleSheet("""
            QLabel {
                background-color: #2563eb;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 20px;
            }
        """)
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.addWidget(avatar)
        
        # User info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name_label = QLabel("Dr. Sam Wheeler")
        name_label.setObjectName("userName")
        info_layout.addWidget(name_label)
        
        role_label = QLabel("Chief Engineer")
        role_label.setObjectName("userRole")
        info_layout.addWidget(role_label)
        
        profile_layout.addLayout(info_layout)
        profile_layout.addStretch()
        
        profile_widget.setLayout(profile_layout)
        
        return profile_widget
    
    def on_nav_click(self, tab_id: str):
        self.set_active_tab(tab_id)
        self.tab_changed.emit(tab_id)
    
    def set_active_tab(self, tab_id: str):
        # Update active state for all buttons
        for btn_id, button in self.nav_buttons.items():
            if btn_id == tab_id:
                button.setProperty("active", "true")
                self.active_tab = tab_id
            else:
                button.setProperty("active", "false")
            # Force style refresh
            button.style().unpolish(button)
            button.style().polish(button)
    
    def toggle_theme(self):
        current_text = self.theme_button.text()
        is_dark = current_text == "☀️"
        self.theme_button.setText("🌙" if is_dark else "☀️")
        self.theme_toggled.emit(not is_dark)
