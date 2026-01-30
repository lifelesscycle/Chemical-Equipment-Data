"""
Stylesheet for ChemData PyQt6 Application
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #f9fafb;
}

/* Sidebar Styles */
QWidget#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

QLabel#logoText {
    color: #111827;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#navButton {
    background-color: transparent;
    border: none;
    color: #6b7280;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    border-radius: 8px;
}

QPushButton#navButton:hover {
    background-color: #f3f4f6;
    color: #111827;
}

QPushButton#navButton[active="true"] {
    background-color: #eff6ff;
    color: #2563eb;
}

QLabel#sectionLabel {
    color: #9ca3af;
    font-size: 11px;
    font-weight: 600;
    padding: 8px 16px;
    letter-spacing: 0.5px;
}

/* User Profile */
QWidget#userProfile {
    background-color: #f9fafb;
    border-radius: 12px;
    padding: 12px;
}

QLabel#userName {
    color: #111827;
    font-size: 14px;
    font-weight: 600;
}

QLabel#userRole {
    color: #6b7280;
    font-size: 12px;
}

/* Main Content Area */
QWidget#mainContent {
    background-color: #f9fafb;
}

/* Page Headers */
QLabel#pageTitle {
    color: #111827;
    font-size: 28px;
    font-weight: 700;
}

QLabel#pageSubtitle {
    color: #6b7280;
    font-size: 14px;
}

/* Stat Cards */
QFrame#statCard {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
}

QLabel#statLabel {
    color: #6b7280;
    font-size: 13px;
    font-weight: 500;
}

QLabel#statValue {
    color: #111827;
    font-size: 32px;
    font-weight: 700;
}

QLabel#statUnit {
    color: #6b7280;
    font-size: 16px;
}

QLabel#statMeta {
    color: #9ca3af;
    font-size: 12px;
}

/* Dashboard Cards */
QFrame#dashboardCard {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
}

QLabel#cardTitle {
    color: #111827;
    font-size: 16px;
    font-weight: 600;
}

/* Buttons */
QPushButton#primaryButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#primaryButton:hover {
    background-color: #1d4ed8;
}

QPushButton#secondaryButton {
    background-color: transparent;
    color: #374151;
    border: 1px solid #d1d5db;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#secondaryButton:hover {
    background-color: #f9fafb;
}

/* Filters */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 8px 12px;
    color: #111827;
    font-size: 14px;
}

QComboBox:hover {
    border-color: #9ca3af;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    selection-background-color: #eff6ff;
    selection-color: #2563eb;
}

/* Equipment Cards */
QFrame#equipmentCard {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
}

QLabel#equipmentName {
    color: #111827;
    font-size: 16px;
    font-weight: 600;
}

QLabel#equipmentType {
    color: #6b7280;
    font-size: 13px;
}

QLabel#metricLabel {
    color: #6b7280;
    font-size: 12px;
}

QLabel#metricValue {
    color: #111827;
    font-size: 14px;
    font-weight: 600;
}

/* Status Badges */
QLabel#statusBadge[status="normal"] {
    background-color: #d1fae5;
    color: #065f46;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="warning"] {
    background-color: #fef3c7;
    color: #92400e;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="critical"] {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Search Bar */
QLineEdit#searchInput {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 10px 12px 10px 40px;
    font-size: 14px;
    color: #111827;
}

QLineEdit#searchInput:focus {
    border-color: #2563eb;
    outline: none;
}

/* Upload Dropzone */
QFrame#uploadDropzone {
    background-color: #f9fafb;
    border: 2px dashed #d1d5db;
    border-radius: 12px;
    padding: 40px;
}

QFrame#uploadDropzone[dragActive="true"] {
    background-color: #eff6ff;
    border-color: #2563eb;
}

QLabel#dropzoneTitle {
    color: #111827;
    font-size: 18px;
    font-weight: 600;
}

QLabel#dropzoneSubtitle {
    color: #6b7280;
    font-size: 14px;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #e5e7eb;
    text-align: center;
    color: #111827;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #3b82f6;
    border-radius: 4px;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #f3f4f6;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #d1d5db;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9ca3af;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Table Widget */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    gridline-color: #f3f4f6;
}

QTableWidget::item {
    padding: 8px;
    color: #111827;
}

QTableWidget::item:selected {
    background-color: #eff6ff;
    color: #2563eb;
}

QHeaderView::section {
    background-color: #f9fafb;
    color: #6b7280;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #e5e7eb;
    font-weight: 600;
    font-size: 12px;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #111827;
}

/* Sidebar Styles */
QWidget#sidebar {
    background-color: #1f2937;
    border-right: 1px solid #374151;
}

QLabel#logoText {
    color: #f9fafb;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#navButton {
    background-color: transparent;
    border: none;
    color: #9ca3af;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    border-radius: 8px;
}

QPushButton#navButton:hover {
    background-color: #374151;
    color: #f9fafb;
}

QPushButton#navButton[active="true"] {
    background-color: #1e3a8a;
    color: #60a5fa;
}

QLabel#sectionLabel {
    color: #6b7280;
    font-size: 11px;
    font-weight: 600;
    padding: 8px 16px;
    letter-spacing: 0.5px;
}

/* User Profile */
QWidget#userProfile {
    background-color: #374151;
    border-radius: 12px;
    padding: 12px;
}

QLabel#userName {
    color: #f9fafb;
    font-size: 14px;
    font-weight: 600;
}

QLabel#userRole {
    color: #9ca3af;
    font-size: 12px;
}

/* Main Content Area */
QWidget#mainContent {
    background-color: #111827;
}

/* Page Headers */
QLabel#pageTitle {
    color: #f9fafb;
    font-size: 28px;
    font-weight: 700;
}

QLabel#pageSubtitle {
    color: #9ca3af;
    font-size: 14px;
}

/* Stat Cards */
QFrame#statCard {
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 20px;
}

QLabel#statLabel {
    color: #9ca3af;
    font-size: 13px;
    font-weight: 500;
}

QLabel#statValue {
    color: #f9fafb;
    font-size: 32px;
    font-weight: 700;
}

QLabel#statUnit {
    color: #9ca3af;
    font-size: 16px;
}

QLabel#statMeta {
    color: #6b7280;
    font-size: 12px;
}

/* Dashboard Cards */
QFrame#dashboardCard {
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 20px;
}

QLabel#cardTitle {
    color: #f9fafb;
    font-size: 16px;
    font-weight: 600;
}

/* Buttons */
QPushButton#primaryButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#primaryButton:hover {
    background-color: #1d4ed8;
}

QPushButton#secondaryButton {
    background-color: transparent;
    color: #d1d5db;
    border: 1px solid #4b5563;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#secondaryButton:hover {
    background-color: #374151;
}

/* Filters */
QComboBox {
    background-color: #1f2937;
    border: 1px solid #4b5563;
    border-radius: 8px;
    padding: 8px 12px;
    color: #f9fafb;
    font-size: 14px;
}

QComboBox:hover {
    border-color: #6b7280;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 8px;
    selection-background-color: #1e3a8a;
    selection-color: #60a5fa;
}

/* Equipment Cards */
QFrame#equipmentCard {
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 16px;
}

QLabel#equipmentName {
    color: #f9fafb;
    font-size: 16px;
    font-weight: 600;
}

QLabel#equipmentType {
    color: #9ca3af;
    font-size: 13px;
}

QLabel#metricLabel {
    color: #9ca3af;
    font-size: 12px;
}

QLabel#metricValue {
    color: #f9fafb;
    font-size: 14px;
    font-weight: 600;
}

/* Status Badges */
QLabel#statusBadge[status="normal"] {
    background-color: #064e3b;
    color: #a7f3d0;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="warning"] {
    background-color: #78350f;
    color: #fde68a;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="critical"] {
    background-color: #7f1d1d;
    color: #fecaca;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Search Bar */
QLineEdit#searchInput {
    background-color: #1f2937;
    border: 1px solid #4b5563;
    border-radius: 8px;
    padding: 10px 12px 10px 40px;
    font-size: 14px;
    color: #f9fafb;
}

QLineEdit#searchInput:focus {
    border-color: #2563eb;
    outline: none;
}

/* Upload Dropzone */
QFrame#uploadDropzone {
    background-color: #1f2937;
    border: 2px dashed #4b5563;
    border-radius: 12px;
    padding: 40px;
}

QFrame#uploadDropzone[dragActive="true"] {
    background-color: #1e3a8a;
    border-color: #2563eb;
}

QLabel#dropzoneTitle {
    color: #f9fafb;
    font-size: 18px;
    font-weight: 600;
}

QLabel#dropzoneSubtitle {
    color: #9ca3af;
    font-size: 14px;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #374151;
    text-align: center;
    color: #f9fafb;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #3b82f6;
    border-radius: 4px;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #1f2937;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #4b5563;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6b7280;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Table Widget */
QTableWidget {
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 8px;
    gridline-color: #374151;
}

QTableWidget::item {
    padding: 8px;
    color: #f9fafb;
}

QTableWidget::item:selected {
    background-color: #1e3a8a;
    color: #60a5fa;
}

QHeaderView::section {
    background-color: #111827;
    color: #9ca3af;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #374151;
    font-weight: 600;
    font-size: 12px;
}
"""

# Login Page Styles
LOGIN_LIGHT_THEME = """
QWidget#loginContainer {
    background-color: #f9fafb;
}

QFrame#loginCard {
    background-color: #ffffff;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
}

QLabel#loginTitle {
    color: #111827;
    font-size: 24px;
    font-weight: 700;
}

QLabel#loginSubtitle {
    color: #6b7280;
    font-size: 14px;
}

QLineEdit#loginInput {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #111827;
}

QLineEdit#loginInput:focus {
    border-color: #2563eb;
}

QPushButton#signInButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#signInButton:hover {
    background-color: #1d4ed8;
}

QPushButton#signInButton:disabled {
    background-color: #9ca3af;
}

QCheckBox {
    color: #374151;
    font-size: 14px;
}

QLabel#errorMessage {
    background-color: #fee2e2;
    color: #991b1b;
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
}
"""

LOGIN_DARK_THEME = """
QWidget#loginContainer {
    background-color: #111827;
}

QFrame#loginCard {
    background-color: #1f2937;
    border-radius: 16px;
    border: 1px solid #374151;
}

QLabel#loginTitle {
    color: #f9fafb;
    font-size: 24px;
    font-weight: 700;
}

QLabel#loginSubtitle {
    color: #9ca3af;
    font-size: 14px;
}

QLineEdit#loginInput {
    background-color: #111827;
    border: 1px solid #4b5563;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #f9fafb;
}

QLineEdit#loginInput:focus {
    border-color: #2563eb;
}

QPushButton#signInButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#signInButton:hover {
    background-color: #1d4ed8;
}

QPushButton#signInButton:disabled {
    background-color: #4b5563;
}

QCheckBox {
    color: #d1d5db;
    font-size: 14px;
}

QLabel#errorMessage {
    background-color: #7f1d1d;
    color: #fecaca;
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
}
"""
