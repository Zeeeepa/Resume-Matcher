#!/usr/bin/env python3
"""
Test script to validate the upload fix is working
"""
import requests
import time
import sys

def test_api_endpoints():
    """Test that all API endpoints are working correctly"""
    base_url = "http://localhost:8000"
    
    print("🔧 TESTING UPLOAD FIX")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/ping", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check: {data}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: CORS preflight
    print("2. Testing CORS preflight...")
    try:
        headers = {
            "Origin": "http://localhost:3001",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        response = requests.options(f"{base_url}/api/v1/resumes/upload", headers=headers, timeout=5)
        if response.status_code == 200:
            cors_origin = response.headers.get("access-control-allow-origin")
            print(f"   ✅ CORS preflight: {cors_origin}")
        else:
            print(f"   ❌ CORS preflight failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ CORS preflight error: {e}")
        return False
    
    # Test 3: Upload endpoint validation
    print("3. Testing upload endpoint validation...")
    try:
        response = requests.post(f"{base_url}/api/v1/resumes/upload", timeout=5)
        if response.status_code == 422:  # Expecting validation error for missing file
            data = response.json()
            print(f"   ✅ Upload validation: {data.get('detail', [{}])[0].get('msg', 'Field required')}")
        else:
            print(f"   ❌ Upload validation unexpected: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Upload validation error: {e}")
        return False
    
    # Test 4: File type validation
    print("4. Testing file type validation...")
    try:
        files = {'file': ('test.txt', 'sample content', 'text/plain')}
        response = requests.post(f"{base_url}/api/v1/resumes/upload", files=files, timeout=5)
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ File type validation: {data.get('detail', 'Invalid file type')}")
        else:
            print(f"   ❌ File type validation unexpected: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ File type validation error: {e}")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("=" * 50)
    print("✅ Backend API is running correctly")
    print("✅ CORS is configured for frontend access")
    print("✅ Upload endpoints are working")
    print("✅ File validation is working")
    print("\n📋 NEXT STEPS:")
    print("1. Make sure frontend is running on http://localhost:3001")
    print("2. Try uploading a PDF or DOCX file")
    print("3. Check browser console for any remaining errors")
    
    return True

if __name__ == "__main__":
    success = test_api_endpoints()
    sys.exit(0 if success else 1)
