import React, { useState } from 'react';
import { useFileUpload, useUploadHistory } from '../hooks/useApi';
import apiService from '../services/api';
import '../styles/UploadPages.css';

const UploadPage = ({ isDarkMode }) => {
  const [dragActive, setDragActive] = useState(false);
  const { uploadFile, uploading, progress, error: uploadError } = useFileUpload();
  const { data: uploadHistory, loading: historyLoading, refetch: refetchHistory } = useUploadHistory();
  const [uploadMessage, setUploadMessage] = useState('');

  const recentUploads = uploadHistory?.results || uploadHistory || [];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = async (e) => {
    if (e.target.files && e.target.files[0]) {
      await handleFileUpload(e.target.files[0]);
    }
  };

  const handleFileUpload = async (file) => {
    try {
      setUploadMessage('');
      
      // Validate file type
      const validTypes = ['.csv', '.xls', '.xlsx'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!validTypes.includes(fileExtension)) {
        setUploadMessage('Invalid file type. Please upload a CSV or Excel file.');
        return;
      }

      // Validate file size (50MB max)
      if (file.size > 50 * 1024 * 1024) {
        setUploadMessage('File size exceeds 50MB limit.');
        return;
      }

      const result = await uploadFile(file, { file_type: fileExtension });
      if (result.records_success > 0) {
        setUploadMessage(`Success! Imported ${result.records_success} records. (${result.records_failed} skipped)`);
    } else if (result.records_failed > 0) {
        setUploadMessage(`Warning: File uploaded but all ${result.records_failed} records failed to import.`);
    } else {
        setUploadMessage(`File uploaded successfully.`);
    }
      
      // Refresh upload history
      setTimeout(() => {
        refetchHistory();
      }, 1000);

      // Clear file input
      const fileInput = document.getElementById('fileInput');
      if (fileInput) fileInput.value = '';
      
    } catch (err) {
      setUploadMessage(`Upload failed: ${err.message}`);
    }
  };

  const handleDownloadTemplate = async () => {
    try {
      const blob = await apiService.downloadReport('template', { format: 'csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'equipment_template.csv';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      setUploadMessage('Failed to download template');
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'done':
      case 'completed':
        return 'success';
      case 'processing':
      case 'pending':
        return 'processing';
      case 'failed':
      case 'error':
        return 'failed';
      default:
        return 'archived';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className={`upload-page ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="upload-header">
        <div className="header-content">
          <h1 className="page-title">Upload Equipment Data</h1>
          <p className="page-subtitle">Import your chemical inventory and equipment status logs.</p>
        </div>
        <div className="header-actions">
          <button className="notification-btn">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M15 6.66667C15 5.34058 14.4732 4.06881 13.5355 3.13113C12.5979 2.19345 11.3261 1.66667 10 1.66667C8.67392 1.66667 7.40215 2.19345 6.46447 3.13113C5.52678 4.06881 5 5.34058 5 6.66667C5 12.5 2.5 14.1667 2.5 14.1667H17.5C17.5 14.1667 15 12.5 15 6.66667Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M11.4417 17.5C11.2952 17.7526 11.0849 17.9622 10.8319 18.1079C10.5789 18.2537 10.292 18.3304 10 18.3304C9.70802 18.3304 9.42116 18.2537 9.16815 18.1079C8.91514 17.9622 8.70484 17.7526 8.55835 17.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span className="notification-badge">3</span>
          </button>
          <button className="download-template-btn" onClick={handleDownloadTemplate}>
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M10 3V13M10 13L6 9M10 13L14 9M3 17H17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Download Template
          </button>
        </div>
      </div>

      <div className="upload-content">
        <div className="upload-section">
          <div 
            className={`upload-dropzone ${dragActive ? 'drag-active' : ''} ${uploading ? 'uploading' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {uploading ? (
              <div className="upload-progress">
                <div className="progress-circle">
                  <svg width="80" height="80" viewBox="0 0 80 80">
                    <circle cx="40" cy="40" r="35" stroke="#e5e7eb" strokeWidth="6" fill="none"/>
                    <circle 
                      cx="40" 
                      cy="40" 
                      r="35" 
                      stroke="#3b82f6" 
                      strokeWidth="6" 
                      fill="none"
                      strokeDasharray={`${2 * Math.PI * 35}`}
                      strokeDashoffset={`${2 * Math.PI * 35 * (1 - progress / 100)}`}
                      strokeLinecap="round"
                      style={{ transition: 'stroke-dashoffset 0.3s' }}
                    />
                  </svg>
                  <div className="progress-text">{progress}%</div>
                </div>
                <h3 className="dropzone-title">Uploading...</h3>
                <p className="dropzone-subtitle">Please wait while we process your file</p>
              </div>
            ) : (
              <>
                <div className="dropzone-icon">
                  <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                    <circle cx="32" cy="32" r="32" fill="currentColor" opacity="0.1"/>
                    <path d="M32 20V44M32 44L24 36M32 44L40 36" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M44 28C44 27.4696 43.7893 26.9609 43.4142 26.5858C43.0391 26.2107 42.5304 26 42 26H38" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <h3 className="dropzone-title">Drag & Drop your CSV file here</h3>
                <p className="dropzone-subtitle">
                  Supports <strong>.csv</strong>, <strong>.xls</strong>, <strong>.xlsx</strong> files up to 50MB.
                </p>
                <p className="dropzone-info">Ensure your columns match the equipment template.</p>
                
                <div className="dropzone-divider">
                  <span>OR</span>
                </div>

                <input 
                  type="file" 
                  id="fileInput" 
                  accept=".csv,.xls,.xlsx"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                  disabled={uploading}
                />
                <button 
                  className="browse-btn"
                  onClick={() => document.getElementById('fileInput').click()}
                  disabled={uploading}
                >
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M17.5 12.5V15.8333C17.5 16.2754 17.3244 16.6993 17.0118 17.0118C16.6993 17.3244 16.2754 17.5 15.8333 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V12.5M14.1667 6.66667L10 2.5M10 2.5L5.83333 6.66667M10 2.5V12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Browse Files
                </button>
              </>
            )}
          </div>

          {(uploadMessage || uploadError) && (
            <div className={`upload-message ${uploadError ? 'error' : 'success'}`}>
              {uploadError || uploadMessage}
            </div>
          )}

          <div className="stats-row">
            <div className="stat-box">
              <div className="stat-header">
                <span className="stat-label">Total Records</span>
                <div className="stat-icon blue">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M3 4H17M3 8H10M3 12H17M3 16H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">24,592</div>
              <div className="stat-trend positive">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M6 10V2M6 2L2 6M6 2L10 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                +12% this month
              </div>
            </div>

            <div className="stat-box">
              <div className="stat-header">
                <span className="stat-label">Success Rate</span>
                <div className="stat-icon green">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="7" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M7 10L9 12L13 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">99.8%</div>
              <div className="stat-status stable">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <circle cx="6" cy="6" r="5" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M6 4V6H8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Stable
              </div>
            </div>

            <div className="stat-box">
              <div className="stat-header">
                <span className="stat-label">Errors Found</span>
                <div className="stat-icon warning">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 6V10M10 14H10.01M18 10C18 14.4183 14.4183 18 10 18C5.58172 18 2 14.4183 2 10C2 5.58172 5.58172 2 10 2C14.4183 2 18 5.58172 18 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">12</div>
              <div className="stat-status warning">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M6 2L2 10H10L6 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M6 7V5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  <circle cx="6" cy="8.5" r="0.5" fill="currentColor"/>
                </svg>
                Action needed
              </div>
            </div>
          </div>
        </div>

        <div className="recent-uploads-section">
          <div className="section-header">
            <h2 className="section-title">Recent Uploads</h2>
            <button className="view-all-btn" onClick={refetchHistory}>
              {historyLoading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>

          <div className="uploads-list">
            {historyLoading ? (
              <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading upload history...</p>
              </div>
            ) : recentUploads.length > 0 ? (
              recentUploads.map((upload) => (
                <div key={upload.id} className="upload-item">
                  <div className={`file-icon ${getStatusColor(upload.status)}`}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path d="M11.667 1.667H5.00033C4.55831 1.667 4.13437 1.84259 3.82181 2.15515C3.50925 2.46771 3.33366 2.89164 3.33366 3.33366V16.667C3.33366 17.109 3.50925 17.533 3.82181 17.8455C4.13437 18.1581 4.55831 18.3337 5.00033 18.3337H15.0003C15.4424 18.3337 15.8663 18.1581 16.1789 17.8455C16.4914 17.533 16.667 17.109 16.667 16.667V6.66699L11.667 1.667Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M11.667 1.667V6.66699H16.667" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <div className="file-info">
                    <div className="file-name" title={upload.filename || upload.name}>
                      {upload.filename || upload.name}
                    </div>
                    <div className="file-meta">
                      {formatDate(upload.created_at || upload.date)} • {formatFileSize(upload.file_size || 0)}
                    </div>
                  </div>
                  <span className={`status-badge ${getStatusColor(upload.status)}`}>
                    {upload.status}
                  </span>
                </div>
              ))
            ) : (
              <div className="no-uploads">
                <p>No uploads yet. Upload your first file to get started!</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {uploading && (
        <div className="processing-queue">
          <div className="queue-content">
            <div className="queue-header">
              <h3>Processing Queue</h3>
            </div>
            <p className="queue-text">Currently analyzing uploaded file.</p>
            <div className="queue-loader">
              <div className="loader-bar" style={{ width: `${progress}%` }}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
