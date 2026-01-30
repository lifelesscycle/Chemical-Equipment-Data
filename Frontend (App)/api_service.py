"""
API Service - FIXED VERSION with Improved Authentication
Key fixes:
1. Better token storage and retrieval
2. Automatic token refresh on 401 errors
3. Request timeout handling
4. Detailed error messages
5. Debug logging
"""
import requests
import json
from typing import Optional, Dict, Any, List
from pathlib import Path


class ApiService:
    def __init__(self, base_url: str = 'http://localhost:8000/api', debug: bool = True):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self._token_refresh_in_progress = False
        self.debug = debug
        
        if self.debug:
            print(f"[API Service] Initialized with base URL: {base_url}")
    
    # ==================== TOKEN MANAGEMENT ====================
    
    def get_token(self) -> Optional[str]:
        return self.access_token
    
    def set_token(self, token: str):
        self.access_token = token
        if self.debug:
            print(f"[API Service] Access token set: {token[:20]}...")
    
    def get_refresh_token(self) -> Optional[str]:
        return self.refresh_token
    
    def set_refresh_token(self, token: str):
        self.refresh_token = token
        if self.debug:
            print(f"[API Service] Refresh token set: {token[:20]}...")
    
    def clear_tokens(self):
        self.access_token = None
        self.refresh_token = None
        if self.debug:
            print("[API Service] Tokens cleared")
    
    def refresh_access_token(self) -> str:
        """Refresh access token using refresh token"""
        if self._token_refresh_in_progress:
            raise Exception("Token refresh already in progress")
        
        if not self.refresh_token:
            raise Exception('No refresh token available')
        
        self._token_refresh_in_progress = True
        try:
            if self.debug:
                print("[API Service] Refreshing access token...")
                
            response = requests.post(
                f"{self.base_url}/token/refresh/",
                json={'refresh': self.refresh_token},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if not response.ok:
                self.clear_tokens()
                raise Exception('Token refresh failed')
            
            data = response.json()
            self.set_token(data['access'])
            
            if self.debug:
                print("[API Service] Token refreshed successfully")
                
            return data['access']
        finally:
            self._token_refresh_in_progress = False
    
    # ==================== GENERIC FETCH METHOD ====================
    
    def fetch_with_auth(self, endpoint: str, method: str = 'GET', 
                       data: Optional[Dict] = None, files: Optional[Dict] = None,
                       params: Optional[Dict] = None) -> Any:
        """Generic method to make authenticated API requests - FIXED VERSION"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        # CRITICAL FIX: Always add Authorization header if token exists
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
            if self.debug:
                print(f"[API Service] Request: {method} {url}")
                print(f"[API Service] Auth header: Bearer {self.access_token[:20]}...")
        else:
            if self.debug:
                print(f"[API Service] WARNING: No access token available!")
                print(f"[API Service] Request: {method} {url} (UNAUTHENTICATED)")
        
        # Don't set Content-Type for file uploads
        if files is None and data is not None:
            headers['Content-Type'] = 'application/json'
        
        kwargs = {
            'headers': headers,
            'params': params,
            'timeout': 30  # Add timeout
        }
        
        if data and files is None:
            kwargs['json'] = data
        elif files:
            kwargs['files'] = files
            if data:
                kwargs['data'] = data
        
        try:
            response = requests.request(method, url, **kwargs)
            
            if self.debug:
                print(f"[API Service] Response: {response.status_code}")
            
            # Handle 401 Unauthorized - try to refresh token
            if response.status_code == 401:
                if self.debug:
                    print("[API Service] 401 Unauthorized - attempting token refresh")
                
                if self.refresh_token:
                    try:
                        self.refresh_access_token()
                        # Retry the request with new token
                        headers['Authorization'] = f'Bearer {self.access_token}'
                        kwargs['headers'] = headers
                        response = requests.request(method, url, **kwargs)
                        
                        if self.debug:
                            print(f"[API Service] Retry response: {response.status_code}")
                    except Exception as e:
                        self.clear_tokens()
                        raise Exception(f"Authentication failed: {str(e)}")
                else:
                    raise Exception("Authentication credentials were not provided. Please log in again.")
            
            if not response.ok:
                try:
                    error = response.json()
                    error_msg = error.get('detail') or error.get('message') or f'HTTP error! status: {response.status_code}'
                except:
                    error_msg = f'HTTP error! status: {response.status_code}'
                    
                if self.debug:
                    print(f"[API Service] Error: {error_msg}")
                    
                raise Exception(error_msg)
            
            # Handle empty responses
            if response.status_code == 204 or not response.content:
                return None
            
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            return response
            
        except requests.ConnectionError as e:
            raise Exception("Cannot connect to backend server. Please ensure it's running at localhost:8000")
        except requests.Timeout as e:
            raise Exception("Request timed out. The server may be slow or unresponsive")
        except Exception as e:
            if "Authentication" not in str(e):
                if self.debug:
                    print(f"[API Service] Exception: {str(e)}")
            raise
    
    # ==================== AUTHENTICATION ENDPOINTS ====================
    
    def login(self, username: str, password: str) -> Dict:
        """Login and get access tokens - FIXED VERSION"""
        if self.debug:
            print(f"[API Service] Attempting login for user: {username}")
            
        try:
            response = requests.post(
                f"{self.base_url}/token/",
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if self.debug:
                print(f"[API Service] Login response: {response.status_code}")
            
            if not response.ok:
                try:
                    error = response.json()
                    error_detail = error.get('detail', 'Invalid credentials')
                    if self.debug:
                        print(f"[API Service] Login failed: {error_detail}")
                    raise Exception(error_detail)
                except:
                    raise Exception('Login failed')
            
            data = response.json()
            
            # CRITICAL FIX: Ensure tokens are stored properly
            if 'access' in data and 'refresh' in data:
                self.set_token(data['access'])
                self.set_refresh_token(data['refresh'])
                
                if self.debug:
                    print("[API Service] ✅ Login successful - tokens stored")
                    print(f"[API Service] Access token: {data['access'][:30]}...")
                    print(f"[API Service] Refresh token: {data['refresh'][:30]}...")
            else:
                raise Exception("Login response missing access or refresh token")
            
            return data
            
        except requests.ConnectionError:
            raise Exception("Cannot connect to backend server at localhost:8000")
        except requests.Timeout:
            raise Exception("Login request timed out")
    
    def logout(self):
        """Logout and clear tokens"""
        try:
            self.fetch_with_auth('/logout/', method='POST')
        except:
            pass
        finally:
            self.clear_tokens()
    
    def get_current_user(self) -> Dict:
        """Get current user information"""
        return self.fetch_with_auth('/user/me/')
    
    # ==================== EQUIPMENT ENDPOINTS ====================
    
    def get_equipment(self, filters: Optional[Dict] = None) -> Dict:
        """Get equipment list with optional filters"""
        if self.debug:
            print(f"[API Service] Fetching equipment with filters: {filters}")
        return self.fetch_with_auth('/equipment/', params=filters)
    
    def get_equipment_by_id(self, equipment_id: int) -> Dict:
        """Get specific equipment by ID"""
        return self.fetch_with_auth(f'/equipment/{equipment_id}/')
    
    def create_equipment(self, data: Dict) -> Dict:
        """Create new equipment"""
        return self.fetch_with_auth('/equipment/', method='POST', data=data)
    
    def update_equipment(self, equipment_id: int, data: Dict) -> Dict:
        """Update equipment"""
        return self.fetch_with_auth(f'/equipment/{equipment_id}/', method='PUT', data=data)
    
    def delete_equipment(self, equipment_id: int):
        """Delete equipment"""
        return self.fetch_with_auth(f'/equipment/{equipment_id}/', method='DELETE')
    
    def get_equipment_status(self) -> Dict:
        """Get equipment status summary"""
        return self.fetch_with_auth('/equipment/status/')
    
    def get_equipment_readings(self, equipment_id: int, filters: Optional[Dict] = None) -> Dict:
        """Get readings for specific equipment"""
        return self.fetch_with_auth(f'/equipment/{equipment_id}/readings/', params=filters)
    
    def get_equipment_alerts(self, equipment_id: int) -> List[Dict]:
        """Get alerts for specific equipment"""
        return self.fetch_with_auth(f'/equipment/{equipment_id}/alerts/')
    
    # ==================== EQUIPMENT TYPES ENDPOINTS ====================
    
    def get_equipment_types(self) -> List[Dict]:
        """Get all equipment types"""
        return self.fetch_with_auth('/equipment-types/')
    
    def get_equipment_type_by_id(self, type_id: int) -> Dict:
        """Get specific equipment type"""
        return self.fetch_with_auth(f'/equipment-types/{type_id}/')
    
    # ==================== PLANT LOCATIONS ENDPOINTS ====================
    
    def get_plant_locations(self) -> List[Dict]:
        """Get all plant locations"""
        return self.fetch_with_auth('/plant-locations/')
    
    # ==================== READINGS ENDPOINTS ====================
    
    def get_readings(self, filters: Optional[Dict] = None) -> Dict:
        """Get readings with optional filters"""
        return self.fetch_with_auth('/readings/', params=filters)
    
    def create_reading(self, data: Dict) -> Dict:
        """Create new reading"""
        return self.fetch_with_auth('/readings/', method='POST', data=data)
    
    def bulk_create_readings(self, data: List[Dict]) -> Dict:
        """Bulk create readings"""
        return self.fetch_with_auth('/readings/bulk_create/', method='POST', data=data)
    
    # ==================== ALERTS ENDPOINTS ====================
    
    def get_alerts(self, filters: Optional[Dict] = None) -> Dict:
        """Get alerts with optional filters"""
        return self.fetch_with_auth('/alerts/', params=filters)
    
    def acknowledge_alert(self, alert_id: int) -> Dict:
        """Acknowledge an alert"""
        return self.fetch_with_auth(f'/alerts/{alert_id}/acknowledge/', method='POST')
    
    def resolve_alert(self, alert_id: int) -> Dict:
        """Resolve an alert"""
        return self.fetch_with_auth(f'/alerts/{alert_id}/resolve/', method='POST')
    
    # ==================== DASHBOARD ENDPOINTS ====================
    
    def get_dashboard_stats(self, params: Optional[Dict] = None) -> Dict:
        """Get dashboard statistics"""
        return self.fetch_with_auth('/dashboard/stats/', params=params)
    
    def get_dashboard_overview(self, params: Optional[Dict] = None) -> Dict:
        """Get dashboard overview"""
        return self.fetch_with_auth('/dashboard/overview/', params=params)
    
    # ==================== CHARTS ENDPOINTS ====================
    
    def get_charts(self, params: Optional[Dict] = None) -> Dict:
        """Get chart data"""
        return self.fetch_with_auth('/charts/', params=params)
    
    def get_equipment_chart_data(self, params: Optional[Dict] = None) -> Dict:
        """Get equipment chart data"""
        return self.fetch_with_auth('/charts/equipment/', params=params)
    
    def get_pressure_trends(self, params: Optional[Dict] = None) -> Dict:
        """Get pressure trends"""
        return self.fetch_with_auth('/charts/pressure/', params=params)
    
    def get_temperature_trends(self, params: Optional[Dict] = None) -> Dict:
        """Get temperature trends"""
        return self.fetch_with_auth('/charts/temperature/', params=params)
    
    # ==================== FILE OPERATIONS ====================
    
    def upload_file(self, file_path: str, metadata: Optional[Dict] = None) -> Dict:
        """Upload a file"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = metadata or {}
            
            headers = {}
            if self.access_token:
                headers['Authorization'] = f'Bearer {self.access_token}'
            
            response = requests.post(
                f"{self.base_url}/upload/",
                files=files,
                data=data,
                headers=headers,
                timeout=60
            )
            
            if not response.ok:
                try:
                    error = response.json()
                    raise Exception(error.get('detail', 'Upload failed'))
                except:
                    raise Exception('File upload failed')
            
            return response.json()
    
    def upload_csv(self, file_path: str) -> Dict:
        """Upload CSV file"""
        return self.upload_file(file_path, {'file_type': 'csv'})
    
    def upload_excel(self, file_path: str) -> Dict:
        """Upload Excel file"""
        return self.upload_file(file_path, {'file_type': 'excel'})
    
    def export_data(self, filters: Optional[Dict] = None, format: str = 'csv') -> bytes:
        """Export data"""
        params = {**(filters or {}), 'format': format}
        response = self.fetch_with_auth('/export/', params=params)
        return response.content
    
    def download_report(self, report_type: str, filters: Optional[Dict] = None) -> bytes:
        """Download report"""
        params = {**(filters or {}), 'report_type': report_type}
        response = self.fetch_with_auth('/reports/download/', params=params)
        return response.content
    
    # ==================== UPLOAD HISTORY ====================
    
    def get_upload_history(self, filters: Optional[Dict] = None) -> Dict:
        """Get upload history"""
        return self.fetch_with_auth('/uploads/', params=filters)
    
    def get_upload_by_id(self, upload_id: int) -> Dict:
        """Get specific upload"""
        return self.fetch_with_auth(f'/uploads/{upload_id}/')
    
    def delete_upload(self, upload_id: int):
        """Delete upload"""
        return self.fetch_with_auth(f'/uploads/{upload_id}/', method='DELETE')
    
    # ==================== ANALYTICS ====================
    
    def get_analytics(self, params: Optional[Dict] = None) -> Dict:
        """Get analytics"""
        return self.fetch_with_auth('/analytics/', params=params)
    
    def get_equipment_analytics(self, equipment_id: int, params: Optional[Dict] = None) -> Dict:
        """Get equipment analytics"""
        return self.fetch_with_auth(f'/equipment/{equipment_id}/analytics/', params=params)
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self, params: Optional[Dict] = None) -> Dict:
        """Get statistics"""
        return self.fetch_with_auth('/statistics/', params=params)


# Singleton instance
api_service = ApiService(debug=True)  # Enable debug mode
