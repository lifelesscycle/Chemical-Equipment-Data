"""
Login Page Component for ChemData Application
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QCheckBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor
from styles import LOGIN_LIGHT_THEME, LOGIN_DARK_THEME
from api_service import api_service


class LoginPage(QWidget):
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        self.setObjectName("loginContainer")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Theme toggle button
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        
        self.theme_toggle = QPushButton("☀️" if self.is_dark_mode else "🌙")
        self.theme_toggle.setFixedSize(40, 40)
        self.theme_toggle.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_toggle)
        
        main_layout.addLayout(theme_layout)
        main_layout.addStretch()
        
        # Login card
        login_card = QFrame()
        login_card.setObjectName("loginCard")
        login_card.setMaximumWidth(450)
        
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)
        
        # Logo and header
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_label = QLabel("⚡")
        logo_label.setStyleSheet("font-size: 32px;")
        logo_layout.addWidget(logo_label)
        
        logo_text = QLabel("ChemData.io")
        logo_text.setStyleSheet("font-size: 20px; font-weight: bold; margin-left: 8px;")
        logo_layout.addWidget(logo_text)
        
        card_layout.addLayout(logo_layout)
        
        # Title
        title = QLabel("Welcome Back")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Enter your credentials to access the equipment dashboard.")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        card_layout.addWidget(subtitle)
        
        # Error message (hidden by default)
        self.error_label = QLabel()
        self.error_label.setObjectName("errorMessage")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)
        
        # Email input
        email_label = QLabel("Email Address")
        email_label.setStyleSheet("font-size: 13px; font-weight: 600; margin-bottom: 4px;")
        card_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setObjectName("loginInput")
        self.email_input.setPlaceholderText("name@company.com")
        self.email_input.setFixedHeight(44)
        card_layout.addWidget(self.email_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 13px; font-weight: 600; margin-bottom: 4px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("loginInput")
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(44)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        # Remember me and forgot password
        options_layout = QHBoxLayout()
        
        self.remember_checkbox = QCheckBox("Remember me")
        options_layout.addWidget(self.remember_checkbox)
        
        options_layout.addStretch()
        
        forgot_button = QPushButton("Forgot Password?")
        forgot_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #2563eb;
                font-size: 13px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #1d4ed8;
            }
        """)
        forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        options_layout.addWidget(forgot_button)
        
        card_layout.addLayout(options_layout)
        
        # Sign in button
        self.sign_in_button = QPushButton("Sign In")
        self.sign_in_button.setObjectName("signInButton")
        self.sign_in_button.setFixedHeight(44)
        self.sign_in_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sign_in_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.sign_in_button)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        footer_text = QLabel("Don't have an account?")
        footer_text.setStyleSheet("font-size: 13px; color: #6b7280;")
        footer_layout.addWidget(footer_text)
        
        contact_button = QPushButton("Contact Admin")
        contact_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #2563eb;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                color: #1d4ed8;
            }
        """)
        contact_button.setCursor(Qt.CursorShape.PointingHandCursor)
        footer_layout.addWidget(contact_button)
        
        card_layout.addLayout(footer_layout)
        
        login_card.setLayout(card_layout)
        main_layout.addWidget(login_card, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addStretch()
        
        # Copyright footer
        copyright_label = QLabel("© 2023 Chemical Data Solutions. All rights reserved.")
        copyright_label.setStyleSheet("color: #9ca3af; font-size: 12px;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(copyright_label)
        
        self.setLayout(main_layout)
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_toggle.setText("☀️" if self.is_dark_mode else "🌙")
        self.apply_theme()
    
    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(LOGIN_DARK_THEME)
        else:
            self.setStyleSheet(LOGIN_LIGHT_THEME)
    
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        # Clear previous error
        self.error_label.hide()
        
        # Validate inputs
        if not email or not password:
            self.show_error("Please enter both email and password")
            return
        
        # Disable button and show loading state
        self.sign_in_button.setEnabled(False)
        self.sign_in_button.setText("Signing In...")
        
        try:
            # Attempt login
            api_service.login(email, password)
            
            # Store remember me preference
            if self.remember_checkbox.isChecked():
                # In a real app, you'd store this securely
                pass
            
            # Emit success signal
            self.login_successful.emit()
            
        except Exception as e:
            self.show_error(f"Login failed: {str(e)}")
            self.sign_in_button.setEnabled(True)
            self.sign_in_button.setText("Sign In")
    
    def show_error(self, message: str):
        self.error_label.setText(f"⚠️ {message}")
        self.error_label.show()
