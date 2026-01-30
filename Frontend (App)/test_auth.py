"""
Authentication Debug Script
Run this to test if login and token management works
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_authentication():
    print("=" * 60)
    print("TESTING AUTHENTICATION FLOW")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Testing Login...")
    login_data = {
        'username': 'Aarya',  # Change this to your username
        'password': 'aarya'   # Change this to your password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/token/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   Access Token: {data.get('access', 'N/A')[:50]}...")
            print(f"   Refresh Token: {data.get('refresh', 'N/A')[:50]}...")
            
            access_token = data.get('access')
            
            # Step 2: Test Equipment Endpoint
            print("\n2. Testing Equipment Endpoint with Token...")
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            equipment_response = requests.get(
                f"{BASE_URL}/equipment/",
                headers=headers
            )
            
            print(f"   Status Code: {equipment_response.status_code}")
            
            if equipment_response.status_code == 200:
                equipment_data = equipment_response.json()
                print(f"   ✅ Equipment data retrieved!")
                print(f"   Data structure: {type(equipment_data)}")
                
                if isinstance(equipment_data, dict):
                    print(f"   Keys: {equipment_data.keys()}")
                    if 'results' in equipment_data:
                        print(f"   Equipment count: {len(equipment_data['results'])}")
                    elif 'count' in equipment_data:
                        print(f"   Equipment count: {equipment_data['count']}")
                elif isinstance(equipment_data, list):
                    print(f"   Equipment count: {len(equipment_data)}")
                
                print(f"\n   Sample data:")
                print(json.dumps(equipment_data if isinstance(equipment_data, dict) else equipment_data[:1], indent=2)[:500])
            else:
                print(f"   ❌ Equipment request failed!")
                print(f"   Response: {equipment_response.text[:200]}")
                
        else:
            print(f"   ❌ Login failed!")
            print(f"   Response: {response.text}")
            
    except requests.ConnectionError:
        print("   ❌ Cannot connect to backend at localhost:8000")
        print("   Make sure the backend server is running")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_authentication()
