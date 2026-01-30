"""
Stylesheet for ChemData PyQt6 Application
Warm & Elegant Theme
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f0;
}

/* Sidebar Styles */
QWidget#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #eaeae5;
}

QLabel#logoText {
    color: #1a1a1a;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#navButton {
    background-color: transparent;
    border: none;
    color: #6b6b65;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    border-radius: 8px;
}

QPushButton#navButton:hover {
    background-color: #f5f5f0;
    color: #1a1a1a;
}

QPushButton#navButton[active="true"] {
    background-color: #faf6ed;
    color: #d4a855;
}

QLabel#sectionLabel {
    color: #6b6b65;
    font-size: 11px;
    font-weight: 600;
    padding: 8px 16px;
    letter-spacing: 0.5px;
}

/* User Profile */
QWidget#userProfile {
    background-color: #f5f5f0;
    border-radius: 12px;
    padding: 12px;
}

QLabel#userName {
    color: #1a1a1a;
    font-size: 14px;
    font-weight: 600;
}

QLabel#userRole {
    color: #6b6b65;
    font-size: 12px;
}

/* Main Content Area */
QWidget#mainContent {
    background-color: #f5f5f0;
}

/* Page Headers */
QLabel#pageTitle {
    color: #1a1a1a;
    font-size: 28px;
    font-weight: 700;
}

QLabel#pageSubtitle {
    color: #6b6b65;
    font-size: 14px;
}

/* Stat Cards */
QFrame#statCard {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 12px;
    padding: 20px;
}

QLabel#statLabel {
    color: #6b6b65;
    font-size: 13px;
    font-weight: 500;
}

QLabel#statValue {
    color: #1a1a1a;
    font-size: 32px;
    font-weight: 700;
}

QLabel#statUnit {
    color: #6b6b65;
    font-size: 16px;
}

QLabel#statMeta {
    color: #6b6b65;
    font-size: 12px;
}

/* Dashboard Cards */
QFrame#dashboardCard {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 12px;
    padding: 20px;
}

QLabel#cardTitle {
    color: #1a1a1a;
    font-size: 16px;
    font-weight: 600;
}

/* Buttons */
QPushButton#primaryButton {
    background-color: #d4a855;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#primaryButton:hover {
    background-color: #c09545;
}

QPushButton#secondaryButton {
    background-color: transparent;
    color: #2a2a2a;
    border: 1px solid #eaeae5;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#secondaryButton:hover {
    background-color: #f5f5f0;
}

/* Filters */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 8px;
    padding: 8px 12px;
    color: #1a1a1a;
    font-size: 14px;
}

QComboBox:hover {
    border-color: #d4a855;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 8px;
    selection-background-color: #faf6ed;
    selection-color: #d4a855;
}

/* Equipment Cards */
QFrame#equipmentCard {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 12px;
    padding: 16px;
}

QLabel#equipmentName {
    color: #1a1a1a;
    font-size: 16px;
    font-weight: 600;
}

QLabel#equipmentType {
    color: #6b6b65;
    font-size: 13px;
}

QLabel#metricLabel {
    color: #6b6b65;
    font-size: 12px;
}

QLabel#metricValue {
    color: #1a1a1a;
    font-size: 14px;
    font-weight: 600;
}

/* Status Badges */
QLabel#statusBadge[status="normal"] {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="warning"] {
    background-color: #fff3e0;
    color: #e65100;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="critical"] {
    background-color: #ffebee;
    color: #c62828;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Search Bar */
QLineEdit#searchInput {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 8px;
    padding: 10px 12px 10px 40px;
    font-size: 14px;
    color: #1a1a1a;
}

QLineEdit#searchInput:focus {
    border-color: #d4a855;
    outline: none;
}

/* Upload Dropzone */
QFrame#uploadDropzone {
    background-color: #f5f5f0;
    border: 2px dashed #eaeae5;
    border-radius: 12px;
    padding: 40px;
}

QFrame#uploadDropzone[dragActive="true"] {
    background-color: #faf6ed;
    border-color: #d4a855;
}

QLabel#dropzoneTitle {
    color: #1a1a1a;
    font-size: 18px;
    font-weight: 600;
}

QLabel#dropzoneSubtitle {
    color: #6b6b65;
    font-size: 14px;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #eaeae5;
    text-align: center;
    color: #1a1a1a;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #e8b962;
    border-radius: 4px;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #f5f5f0;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #eaeae5;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #d4a855;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Table Widget */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 8px;
    gridline-color: #f5f5f0;
}

QTableWidget::item {
    padding: 8px;
    color: #1a1a1a;
}

QTableWidget::item:selected {
    background-color: #faf6ed;
    color: #d4a855;
}

QHeaderView::section {
    background-color: #f5f5f0;
    color: #6b6b65;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #eaeae5;
    font-weight: 600;
    font-size: 12px;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1a1a;
}

/* Sidebar Styles */
QWidget#sidebar {
    background-color: #2a2a2a;
    border-right: 1px solid #353535;
}

QLabel#logoText {
    color: #f5f5f0;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#navButton {
    background-color: transparent;
    border: none;
    color: #a8a8a0;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    border-radius: 8px;
}

QPushButton#navButton:hover {
    background-color: #353535;
    color: #f5f5f0;
}

QPushButton#navButton[active="true"] {
    background-color: #3d3421;
    color: #e8b962;
}

QLabel#sectionLabel {
    color: #a8a8a0;
    font-size: 11px;
    font-weight: 600;
    padding: 8px 16px;
    letter-spacing: 0.5px;
}

/* User Profile */
QWidget#userProfile {
    background-color: #353535;
    border-radius: 12px;
    padding: 12px;
}

QLabel#userName {
    color: #f5f5f0;
    font-size: 14px;
    font-weight: 600;
}

QLabel#userRole {
    color: #a8a8a0;
    font-size: 12px;
}

/* Main Content Area */
QWidget#mainContent {
    background-color: #1a1a1a;
}

/* Page Headers */
QLabel#pageTitle {
    color: #f5f5f0;
    font-size: 28px;
    font-weight: 700;
}

QLabel#pageSubtitle {
    color: #a8a8a0;
    font-size: 14px;
}

/* Stat Cards */
QFrame#statCard {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 12px;
    padding: 20px;
}

QLabel#statLabel {
    color: #a8a8a0;
    font-size: 13px;
    font-weight: 500;
}

QLabel#statValue {
    color: #f5f5f0;
    font-size: 32px;
    font-weight: 700;
}

QLabel#statUnit {
    color: #a8a8a0;
    font-size: 16px;
}

QLabel#statMeta {
    color: #a8a8a0;
    font-size: 12px;
}

/* Dashboard Cards */
QFrame#dashboardCard {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 12px;
    padding: 20px;
}

QLabel#cardTitle {
    color: #f5f5f0;
    font-size: 16px;
    font-weight: 600;
}

/* Buttons */
QPushButton#primaryButton {
    background-color: #e8b962;
    color: #1a1a1a;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#primaryButton:hover {
    background-color: #d4a855;
}

QPushButton#secondaryButton {
    background-color: transparent;
    color: #d4d4cf;
    border: 1px solid #353535;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#secondaryButton:hover {
    background-color: #353535;
}

/* Filters */
QComboBox {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 8px;
    padding: 8px 12px;
    color: #f5f5f0;
    font-size: 14px;
}

QComboBox:hover {
    border-color: #e8b962;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 8px;
    selection-background-color: #3d3421;
    selection-color: #e8b962;
}

/* Equipment Cards */
QFrame#equipmentCard {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 12px;
    padding: 16px;
}

QLabel#equipmentName {
    color: #f5f5f0;
    font-size: 16px;
    font-weight: 600;
}

QLabel#equipmentType {
    color: #a8a8a0;
    font-size: 13px;
}

QLabel#metricLabel {
    color: #a8a8a0;
    font-size: 12px;
}

QLabel#metricValue {
    color: #f5f5f0;
    font-size: 14px;
    font-weight: 600;
}

/* Status Badges */
QLabel#statusBadge[status="normal"] {
    background-color: #1b5e20;
    color: #a5d6a7;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="warning"] {
    background-color: #e65100;
    color: #ffcc80;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

QLabel#statusBadge[status="critical"] {
    background-color: #b71c1c;
    color: #ef9a9a;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Search Bar */
QLineEdit#searchInput {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 8px;
    padding: 10px 12px 10px 40px;
    font-size: 14px;
    color: #f5f5f0;
}

QLineEdit#searchInput:focus {
    border-color: #e8b962;
    outline: none;
}

/* Upload Dropzone */
QFrame#uploadDropzone {
    background-color: #2a2a2a;
    border: 2px dashed #353535;
    border-radius: 12px;
    padding: 40px;
}

QFrame#uploadDropzone[dragActive="true"] {
    background-color: #3d3421;
    border-color: #e8b962;
}

QLabel#dropzoneTitle {
    color: #f5f5f0;
    font-size: 18px;
    font-weight: 600;
}

QLabel#dropzoneSubtitle {
    color: #a8a8a0;
    font-size: 14px;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #353535;
    text-align: center;
    color: #f5f5f0;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #e8b962;
    border-radius: 4px;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #2a2a2a;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #353535;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #e8b962;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Table Widget */
QTableWidget {
    background-color: #2a2a2a;
    border: 1px solid #353535;
    border-radius: 8px;
    gridline-color: #353535;
}

QTableWidget::item {
    padding: 8px;
    color: #f5f5f0;
}

QTableWidget::item:selected {
    background-color: #3d3421;
    color: #e8b962;
}

QHeaderView::section {
    background-color: #1a1a1a;
    color: #a8a8a0;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #353535;
    font-weight: 600;
    font-size: 12px;
}
"""

# Login Page Styles
LOGIN_LIGHT_THEME = """
QWidget#loginContainer {
    background-color: #f5f5f0;
}

QFrame#loginCard {
    background-color: #ffffff;
    border-radius: 16px;
    border: 1px solid #eaeae5;
}

QLabel#loginTitle {
    color: #1a1a1a;
    font-size: 24px;
    font-weight: 700;
}

QLabel#loginSubtitle {
    color: #6b6b65;
    font-size: 14px;
}

QLineEdit#loginInput {
    background-color: #ffffff;
    border: 1px solid #eaeae5;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #1a1a1a;
}

QLineEdit#loginInput:focus {
    border-color: #d4a855;
}

QPushButton#signInButton {
    background-color: #d4a855;
    color: #ffffff;
    border: none;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#signInButton:hover {
    background-color: #c09545;
}

QPushButton#signInButton:disabled {
    background-color: #a8a8a0;
}

QCheckBox {
    color: #2a2a2a;
    font-size: 14px;
}

QLabel#errorMessage {
    background-color: #ffebee;
    color: #c62828;
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
}
"""

LOGIN_DARK_THEME = """
QWidget#loginContainer {
    background-color: #1a1a1a;
}

QFrame#loginCard {
    background-color: #2a2a2a;
    border-radius: 16px;
    border: 1px solid #353535;
}

QLabel#loginTitle {
    color: #f5f5f0;
    font-size: 24px;
    font-weight: 700;
}

QLabel#loginSubtitle {
    color: #a8a8a0;
    font-size: 14px;
}

QLineEdit#loginInput {
    background-color: #1a1a1a;
    border: 1px solid #353535;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #f5f5f0;
}

QLineEdit#loginInput:focus {
    border-color: #e8b962;
}

QPushButton#signInButton {
    background-color: #e8b962;
    color: #1a1a1a;
    border: none;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#signInButton:hover {
    background-color: #d4a855;
}

QPushButton#signInButton:disabled {
    background-color: #353535;
}

QCheckBox {
    color: #d4d4cf;
    font-size: 14px;
}

QLabel#errorMessage {
    background-color: #b71c1c;
    color: #ef9a9a;
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
}
"""
