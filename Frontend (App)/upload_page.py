"""
Upload Page Component for ChemData Application
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QScrollArea, QFileDialog,
                              QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from api_service import api_service
from pathlib import Path
from datetime import datetime


class UploadThread(QThread):
    """Thread for uploading files"""
    upload_complete = pyqtSignal(dict)
    upload_failed = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            # Simulate progress updates
            for i in range(0, 100, 10):
                self.progress_updated.emit(i)
                self.msleep(100)
            
            # Determine file type
            ext = Path(self.file_path).suffix.lower()
            if ext == '.csv':
                result = api_service.upload_csv(self.file_path)
            elif ext in ['.xls', '.xlsx']:
                result = api_service.upload_excel(self.file_path)
            else:
                result = api_service.upload_file(self.file_path)
            
            self.progress_updated.emit(100)
            self.upload_complete.emit(result)
            
        except Exception as e:
            self.upload_failed.emit(str(e))


class UploadHistoryLoader(QThread):
    """Thread for loading upload history"""
    data_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def run(self):
        try:
            data = api_service.get_upload_history()
            uploads = data.get('results', data) if isinstance(data, dict) else data
            self.data_loaded.emit(uploads if isinstance(uploads, list) else [])
        except Exception as e:
            self.error_occurred.emit(str(e))


class UploadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.upload_history = []
        self.uploading = False
        self.setAcceptDrops(True)
        self.init_ui()
    
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
        
        # Upload section
        upload_section = self.create_upload_section()
        layout.addWidget(upload_section)
        
        # Stats row
        stats_row = self.create_stats_row()
        layout.addWidget(stats_row)
        
        # Recent uploads section
        recent_section = self.create_recent_uploads_section()
        layout.addWidget(recent_section)
        
        layout.addStretch()
        
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
        
        title = QLabel("Upload Equipment Data")
        title.setObjectName("pageTitle")
        left_layout.addWidget(title)
        
        subtitle = QLabel("Import your chemical inventory and equipment status logs.")
        subtitle.setObjectName("pageSubtitle")
        left_layout.addWidget(subtitle)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        # Right side - action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        notification_btn = QPushButton("🔔 3")
        notification_btn.setObjectName("secondaryButton")
        notification_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout.addWidget(notification_btn)
        
        download_btn = QPushButton("Download Template")
        download_btn.setObjectName("primaryButton")
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        download_btn.clicked.connect(self.download_template)
        btn_layout.addWidget(download_btn)
        
        header_layout.addLayout(btn_layout)
        
        header_widget.setLayout(header_layout)
        return header_widget
    
    def create_upload_section(self):
        section = QFrame()
        section.setObjectName("dashboardCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        # Dropzone
        self.dropzone = QFrame()
        self.dropzone.setObjectName("uploadDropzone")
        self.dropzone.setMinimumHeight(300)
        
        dropzone_layout = QVBoxLayout()
        dropzone_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dropzone_layout.setSpacing(16)
        
        # Upload icon
        icon_label = QLabel("📁")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dropzone_layout.addWidget(icon_label)
        
        # Title
        self.dropzone_title = QLabel("Drag & Drop your CSV file here")
        self.dropzone_title.setObjectName("dropzoneTitle")
        self.dropzone_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dropzone_layout.addWidget(self.dropzone_title)
        
        # Subtitle
        subtitle = QLabel("Supports .csv, .xls, .xlsx files up to 50MB.")
        subtitle.setObjectName("dropzoneSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dropzone_layout.addWidget(subtitle)
        
        info = QLabel("Ensure your columns match the equipment template.")
        info.setObjectName("dropzoneSubtitle")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dropzone_layout.addWidget(info)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        dropzone_layout.addWidget(self.progress_bar)
        
        # Divider
        divider_layout = QHBoxLayout()
        divider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        divider = QLabel("OR")
        divider.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-size: 12px;
                font-weight: 600;
                padding: 0 16px;
            }
        """)
        divider_layout.addWidget(divider)
        
        dropzone_layout.addLayout(divider_layout)
        
        # Browse button
        self.browse_btn = QPushButton("📂 Browse Files")
        self.browse_btn.setObjectName("primaryButton")
        self.browse_btn.setFixedHeight(44)
        self.browse_btn.setMinimumWidth(160)
        self.browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_btn.clicked.connect(self.browse_files)
        dropzone_layout.addWidget(self.browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.dropzone.setLayout(dropzone_layout)
        layout.addWidget(self.dropzone)
        
        # Message label (hidden by default)
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("""
            QLabel {
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
        self.message_label.hide()
        layout.addWidget(self.message_label)
        
        section.setLayout(layout)
        return section
    
    def create_stats_row(self):
        stats_widget = QWidget()
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Total Records
        stat1 = self.create_stat_box("Total Records", "24,592", "+12% this month", "positive")
        stats_layout.addWidget(stat1)
        
        # Success Rate
        stat2 = self.create_stat_box("Success Rate", "99.8%", "Stable", "stable")
        stats_layout.addWidget(stat2)
        
        # Errors Found
        stat3 = self.create_stat_box("Errors Found", "12", "Action needed", "warning")
        stats_layout.addWidget(stat3)
        
        stats_widget.setLayout(stats_layout)
        return stats_widget
    
    def create_stat_box(self, label: str, value: str, status: str, status_type: str):
        box = QFrame()
        box.setObjectName("statCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setObjectName("statLabel")
        layout.addWidget(label_widget)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        layout.addWidget(value_label)
        
        # Status
        status_label = QLabel(status)
        status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {"#10b981" if status_type == "positive" else "#f59e0b" if status_type == "warning" else "#6b7280"};
            }}
        """)
        layout.addWidget(status_label)
        
        box.setLayout(layout)
        return box
    
    def create_recent_uploads_section(self):
        section = QFrame()
        section.setObjectName("dashboardCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Recent Uploads")
        title.setObjectName("cardTitle")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setObjectName("secondaryButton")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.load_history)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Uploads list
        self.uploads_container = QWidget()
        self.uploads_layout = QVBoxLayout()
        self.uploads_layout.setSpacing(12)
        self.uploads_container.setLayout(self.uploads_layout)
        
        layout.addWidget(self.uploads_container)
        
        section.setLayout(layout)
        return section
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.dropzone.setProperty("dragActive", "true")
            self.dropzone.style().unpolish(self.dropzone)
            self.dropzone.style().polish(self.dropzone)
    
    def dragLeaveEvent(self, event):
        self.dropzone.setProperty("dragActive", "false")
        self.dropzone.style().unpolish(self.dropzone)
        self.dropzone.style().polish(self.dropzone)
    
    def dropEvent(self, event: QDropEvent):
        self.dropzone.setProperty("dragActive", "false")
        self.dropzone.style().unpolish(self.dropzone)
        self.dropzone.style().polish(self.dropzone)
        
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.handle_file_upload(files[0])
    
    def browse_files(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Upload",
            "",
            "Data Files (*.csv *.xls *.xlsx);;All Files (*.*)"
        )
        
        if file_path:
            self.handle_file_upload(file_path)
    
    def handle_file_upload(self, file_path: str):
        # Validate file
        path = Path(file_path)
        
        # Check file type
        valid_extensions = ['.csv', '.xls', '.xlsx']
        if path.suffix.lower() not in valid_extensions:
            self.show_message("Invalid file type. Please upload a CSV or Excel file.", "error")
            return
        
        # Check file size (50MB)
        if path.stat().st_size > 50 * 1024 * 1024:
            self.show_message("File size exceeds 50MB limit.", "error")
            return
        
        # Start upload
        self.uploading = True
        self.dropzone_title.setText("Uploading...")
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.browse_btn.setEnabled(False)
        self.message_label.hide()
        
        self.upload_thread = UploadThread(file_path)
        self.upload_thread.progress_updated.connect(self.on_progress_updated)
        self.upload_thread.upload_complete.connect(self.on_upload_complete)
        self.upload_thread.upload_failed.connect(self.on_upload_failed)
        self.upload_thread.start()
    
    def on_progress_updated(self, value: int):
        self.progress_bar.setValue(value)
    
    def on_upload_complete(self, result: dict):
        self.uploading = False
        self.dropzone_title.setText("Drag & Drop your CSV file here")
        self.progress_bar.hide()
        self.browse_btn.setEnabled(True)
        
        success = result.get('records_success', 0)
        failed = result.get('records_failed', 0)
        
        if success > 0:
            message = f"✅ Success! Imported {success} records. ({failed} skipped)"
            self.show_message(message, "success")
        elif failed > 0:
            message = f"⚠️ Warning: File uploaded but all {failed} records failed to import."
            self.show_message(message, "warning")
        else:
            self.show_message("✅ File uploaded successfully.", "success")
        
        # Refresh history after a short delay
        QTimer.singleShot(1000, self.load_history)
    
    def on_upload_failed(self, error: str):
        self.uploading = False
        self.dropzone_title.setText("Drag & Drop your CSV file here")
        self.progress_bar.hide()
        self.browse_btn.setEnabled(True)
        
        self.show_message(f"❌ Upload failed: {error}", "error")
    
    def show_message(self, text: str, msg_type: str):
        self.message_label.setText(text)
        
        if msg_type == "success":
            bg_color = "#d1fae5"
            text_color = "#065f46"
        elif msg_type == "warning":
            bg_color = "#fef3c7"
            text_color = "#92400e"
        else:  # error
            bg_color = "#fee2e2"
            text_color = "#991b1b"
        
        self.message_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
            }}
        """)
        self.message_label.show()
    
    def load_history(self):
        self.refresh_btn.setText("Refreshing...")
        self.refresh_btn.setEnabled(False)
        
        self.history_loader = UploadHistoryLoader()
        self.history_loader.data_loaded.connect(self.on_history_loaded)
        self.history_loader.start()
    
    def on_history_loaded(self, uploads: list):
        self.upload_history = uploads
        self.refresh_btn.setText("Refresh")
        self.refresh_btn.setEnabled(True)
        self.update_uploads_display()
    
    def update_uploads_display(self):
        # Clear existing items
        for i in reversed(range(self.uploads_layout.count())): 
            self.uploads_layout.itemAt(i).widget().setParent(None)
        
        if not self.upload_history:
            no_uploads = QLabel("No uploads yet. Upload your first file to get started!")
            no_uploads.setObjectName("pageSubtitle")
            no_uploads.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.uploads_layout.addWidget(no_uploads)
            return
        
        for upload in self.upload_history[:10]:  # Show last 10
            item = self.create_upload_item(upload)
            self.uploads_layout.addWidget(item)
    
    def create_upload_item(self, upload: dict):
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.02);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Icon
        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        filename = upload.get('filename', upload.get('name', 'Unknown'))
        name_label = QLabel(filename)
        name_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        info_layout.addWidget(name_label)
        
        created_at = upload.get('created_at', upload.get('date', ''))
        file_size = upload.get('file_size', 0)
        
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                date_str = dt.strftime('%b %d, %Y')
            except:
                date_str = created_at
        else:
            date_str = 'Unknown date'
        
        size_str = self.format_file_size(file_size)
        meta_label = QLabel(f"{date_str} • {size_str}")
        meta_label.setStyleSheet("font-size: 12px; color: #6b7280;")
        info_layout.addWidget(meta_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Status badge
        status = upload.get('status', 'completed')
        status_badge = QLabel(status.upper())
        status_badge.setObjectName("statusBadge")
        status_badge.setProperty("status", "normal" if status in ['done', 'completed'] else "warning")
        status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_badge)
        
        item.setLayout(layout)
        return item
    
    def format_file_size(self, bytes_size: int) -> str:
        if bytes_size == 0:
            return '0 Bytes'
        
        k = 1024
        sizes = ['Bytes', 'KB', 'MB', 'GB']
        i = 0
        size = bytes_size
        
        while size >= k and i < len(sizes) - 1:
            size /= k
            i += 1
        
        return f"{size:.1f} {sizes[i]}"
    
    def download_template(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Template",
                "equipment_template.csv",
                "CSV Files (*.csv)"
            )
            
            if file_path:
                blob = api_service.download_report('template', {'format': 'csv'})
                with open(file_path, 'wb') as f:
                    f.write(blob)
                self.show_message("✅ Template downloaded successfully!", "success")
        except Exception as e:
            self.show_message(f"❌ Failed to download template: {str(e)}", "error")
