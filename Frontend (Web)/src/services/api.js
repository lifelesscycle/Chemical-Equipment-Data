// API Service - Centralized API calls with authentication and error handling
const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.tokenRefreshPromise = null;
  }

  // ==================== TOKEN MANAGEMENT ====================
  
  getToken() {
    return localStorage.getItem('access_token');
  }

  setToken(token) {
    localStorage.setItem('access_token', token);
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  setRefreshToken(token) {
    localStorage.setItem('refresh_token', token);
  }

  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Refresh access token with promise caching to prevent multiple refresh calls
  async refreshAccessToken() {
    // If a refresh is already in progress, return that promise
    if (this.tokenRefreshPromise) {
      return this.tokenRefreshPromise;
    }

    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    this.tokenRefreshPromise = fetch(`${this.baseURL}/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    })
      .then(async (response) => {
        if (!response.ok) {
          this.clearTokens();
          throw new Error('Token refresh failed');
        }
        const data = await response.json();
        this.setToken(data.access);
        return data.access;
      })
      .finally(() => {
        this.tokenRefreshPromise = null;
      });

    return this.tokenRefreshPromise;
  }

  // ==================== GENERIC FETCH METHOD ====================
  
  async fetchWithAuth(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    let response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    // Handle 401 Unauthorized - try to refresh token
    if (response.status === 401 && this.getRefreshToken()) {
      try {
        await this.refreshAccessToken();
        // Retry the request with new token
        headers['Authorization'] = `Bearer ${this.getToken()}`;
        response = await fetch(`${this.baseURL}${endpoint}`, {
          ...options,
          headers,
        });
      } catch (error) {
        // Refresh failed, redirect to login
        this.clearTokens();
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw error;
      }
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ 
        detail: `HTTP error! status: ${response.status}` 
      }));
      throw new Error(error.detail || error.message || `HTTP error! status: ${response.status}`);
    }

    // Handle empty responses (like 204 No Content)
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    }
    return null;
  }

  // ==================== AUTHENTICATION ENDPOINTS ====================
  
  async login(username, password) {
    const response = await fetch(`${this.baseURL}/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(error.detail || 'Invalid credentials');
    }

    const data = await response.json();
    this.setToken(data.access);
    this.setRefreshToken(data.refresh);
    return data;
  }

  async logout() {
    try {
      // Call logout endpoint if it exists
      await this.fetchWithAuth('/logout/', { method: 'POST' });
    } catch (error) {
      console.error('Logout endpoint error:', error);
    } finally {
      this.clearTokens();
    }
  }

  async getCurrentUser() {
    return this.fetchWithAuth('/user/me/');
  }

  // ==================== EQUIPMENT ENDPOINTS ====================
  
  async getEquipment(filters = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(filters).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/equipment/?${queryParams}` : '/equipment/';
    return this.fetchWithAuth(endpoint);
  }

  async getEquipmentById(id) {
    return this.fetchWithAuth(`/equipment/${id}/`);
  }

  async createEquipment(data) {
    return this.fetchWithAuth('/equipment/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateEquipment(id, data) {
    return this.fetchWithAuth(`/equipment/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async patchEquipment(id, data) {
    return this.fetchWithAuth(`/equipment/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async deleteEquipment(id) {
    return this.fetchWithAuth(`/equipment/${id}/`, {
      method: 'DELETE',
    });
  }

  async bulkUpdateEquipment(data) {
    return this.fetchWithAuth('/equipment/bulk_update/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getEquipmentReadings(id, filters = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(filters).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams 
      ? `/equipment/${id}/readings/?${queryParams}` 
      : `/equipment/${id}/readings/`;
    return this.fetchWithAuth(endpoint);
  }

  async getEquipmentAlerts(id) {
    return this.fetchWithAuth(`/equipment/${id}/alerts/`);
  }

  async getEquipmentStatus() {
    return this.fetchWithAuth('/equipment/status/');
  }

  // ==================== EQUIPMENT TYPES ENDPOINTS ====================
  
  async getEquipmentTypes() {
    return this.fetchWithAuth('/equipment-types/');
  }

  async getEquipmentTypeById(id) {
    return this.fetchWithAuth(`/equipment-types/${id}/`);
  }

  async createEquipmentType(data) {
    return this.fetchWithAuth('/equipment-types/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateEquipmentType(id, data) {
    return this.fetchWithAuth(`/equipment-types/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteEquipmentType(id) {
    return this.fetchWithAuth(`/equipment-types/${id}/`, {
      method: 'DELETE',
    });
  }

  // ==================== PLANT LOCATIONS ENDPOINTS ====================
  
  async getPlantLocations() {
    return this.fetchWithAuth('/plant-locations/');
  }

  async getPlantLocationById(id) {
    return this.fetchWithAuth(`/plant-locations/${id}/`);
  }

  async createPlantLocation(data) {
    return this.fetchWithAuth('/plant-locations/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updatePlantLocation(id, data) {
    return this.fetchWithAuth(`/plant-locations/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deletePlantLocation(id) {
    return this.fetchWithAuth(`/plant-locations/${id}/`, {
      method: 'DELETE',
    });
  }

  // ==================== READINGS ENDPOINTS ====================
  
  async getReadings(filters = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(filters).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/readings/?${queryParams}` : '/readings/';
    return this.fetchWithAuth(endpoint);
  }

  async getReadingById(id) {
    return this.fetchWithAuth(`/readings/${id}/`);
  }

  async createReading(data) {
    return this.fetchWithAuth('/readings/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async bulkCreateReadings(data) {
    return this.fetchWithAuth('/readings/bulk_create/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async deleteReading(id) {
    return this.fetchWithAuth(`/readings/${id}/`, {
      method: 'DELETE',
    });
  }

  // ==================== ALERTS ENDPOINTS ====================
  
  async getAlerts(filters = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(filters).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/alerts/?${queryParams}` : '/alerts/';
    return this.fetchWithAuth(endpoint);
  }

  async getAlertById(id) {
    return this.fetchWithAuth(`/alerts/${id}/`);
  }

  async createAlert(data) {
    return this.fetchWithAuth('/alerts/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async acknowledgeAlert(id) {
    return this.fetchWithAuth(`/alerts/${id}/acknowledge/`, {
      method: 'POST',
    });
  }

  async resolveAlert(id) {
    return this.fetchWithAuth(`/alerts/${id}/resolve/`, {
      method: 'POST',
    });
  }

  async deleteAlert(id) {
    return this.fetchWithAuth(`/alerts/${id}/`, {
      method: 'DELETE',
    });
  }

  // ==================== DASHBOARD ENDPOINTS ====================
  
  async getDashboardStats(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/dashboard/stats/?${queryParams}` : '/dashboard/stats/';
    return this.fetchWithAuth(endpoint);
  }

  async getDashboardOverview(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/dashboard/overview/?${queryParams}` : '/dashboard/overview/';
    return this.fetchWithAuth(endpoint);
  }

  // ==================== CHARTS ENDPOINTS ====================
  
  async getCharts(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/charts/?${queryParams}` : '/charts/';
    return this.fetchWithAuth(endpoint);
  }

  async getEquipmentChartData(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/charts/equipment/?${queryParams}` : '/charts/equipment/';
    return this.fetchWithAuth(endpoint);
  }

  async getPressureTrends(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/charts/pressure/?${queryParams}` : '/charts/pressure/';
    return this.fetchWithAuth(endpoint);
  }

  async getTemperatureTrends(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/charts/temperature/?${queryParams}` : '/charts/temperature/';
    return this.fetchWithAuth(endpoint);
  }

  // ==================== FILE OPERATIONS ====================
  
  async uploadFile(file, metadata = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Add any additional metadata
    Object.entries(metadata).forEach(([key, value]) => {
      formData.append(key, value);
    });

    const token = this.getToken();
    const response = await fetch(`${this.baseURL}/upload/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(error.detail || 'File upload failed');
    }

    return response.json();
  }

  async uploadCSV(file) {
    return this.uploadFile(file, { file_type: 'csv' });
  }

  async uploadExcel(file) {
    return this.uploadFile(file, { file_type: 'excel' });
  }

  async exportData(filters = {}, format = 'csv') {
    const params = { ...filters, format };
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/export/?${queryParams}` : '/export/';
    const token = this.getToken();
    
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Export failed');
    }

    return response.blob();
  }

  async downloadReport(reportType, filters = {}) {
    const params = { ...filters, report_type: reportType };
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/reports/download/?${queryParams}` : '/reports/download/';
    const token = this.getToken();
    
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Download failed');
    }

    return response.blob();
  }

  // ==================== UPLOAD HISTORY ====================
  
  async getUploadHistory(filters = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(filters).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/uploads/?${queryParams}` : '/uploads/';
    return this.fetchWithAuth(endpoint);
  }

  async getUploadById(id) {
    return this.fetchWithAuth(`/uploads/${id}/`);
  }

  async deleteUpload(id) {
    return this.fetchWithAuth(`/uploads/${id}/`, {
      method: 'DELETE',
    });
  }

  // ==================== ANALYTICS ====================
  
  async getAnalytics(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/analytics/?${queryParams}` : '/analytics/';
    return this.fetchWithAuth(endpoint);
  }

  async getEquipmentAnalytics(id, params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams 
      ? `/equipment/${id}/analytics/?${queryParams}` 
      : `/equipment/${id}/analytics/`;
    return this.fetchWithAuth(endpoint);
  }

  // ==================== STATISTICS ====================
  
  async getStatistics(params = {}) {
    const queryParams = new URLSearchParams(
      Object.entries(params).filter(([_, v]) => v != null)
    ).toString();
    const endpoint = queryParams ? `/statistics/?${queryParams}` : '/statistics/';
    return this.fetchWithAuth(endpoint);
  }
}

// Export singleton instance
const apiService = new ApiService();
export default apiService;

// Also export the class for testing purposes
export { ApiService };
