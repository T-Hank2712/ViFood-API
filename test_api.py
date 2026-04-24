"""
Test Script cho API
Hướng dẫn sử dụng: python test_api.py
"""
import requests
import json
from pathlib import Path


# Cấu hình
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"
API_KEY = "your-secret-api-key-change-this"  # Đổi theo API_KEY trong .env


def print_separator():
    """In dòng phân cách"""
    print("=" * 70)


def print_response(response):
    """In response một cách đẹp mắt"""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception:
        print(f"Response: {response.text}")


def test_root():
    """Test root endpoint"""
    print_separator()
    print("TEST 1: Root Endpoint")
    print_separator()
    
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    print()


def test_health():
    """Test health check endpoint"""
    print_separator()
    print("TEST 2: Health Check")
    print_separator()
    
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    print()


def test_upload_config():
    """Test upload config endpoint"""
    print_separator()
    print("TEST 3: Get Upload Config")
    print_separator()
    
    response = requests.get(f"{BASE_URL}{API_PREFIX}/upload/config")
    print_response(response)
    print()


def test_upload_image(image_path: str = None):
    """Test upload image endpoint"""
    print_separator()
    print("TEST 4: Upload Image")
    print_separator()
    
    if not image_path:
        print("⚠️  Không có đường dẫn file để upload")
        print("   Bỏ qua test này")
        print()
        return None
    
    image_path = Path(image_path)
    
    if not image_path.exists():
        print(f"❌ File không tồn tại: {image_path}")
        print()
        return None
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path.name, f, 'image/jpeg')}
            headers = {'X-API-Key': API_KEY}
            response = requests.post(f"{BASE_URL}{API_PREFIX}/upload/image", files=files, headers=headers)
        
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Upload thành công!")
            data = response.json()
            filename = data.get('data', {}).get('filename')
            print(f"Filename: {filename}")
            print()
            return filename
        else:
            print("\n❌ Upload thất bại!")
            print()
            return None
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        print()
        return None


def test_delete_image(filename: str = None):
    """Test delete image endpoint"""
    print_separator()
    print("TEST 5: Delete Image")
    print_separator()
    
    if not filename:
        print("⚠️  Không có filename để xóa")
        print("   Bỏ qua test này")
        print()
        return
    
    response = requests.delete(
        f"{BASE_URL}{API_PREFIX}/upload/image/{filename}",
        headers={'X-API-Key': API_KEY}
    )
    print_response(response)
    
    if response.status_code == 200:
        print("\n✅ Xóa file thành công!")
    else:
        print("\n❌ Xóa file thất bại!")
    print()


def test_example_endpoint():
    """Test example endpoint"""
    print_separator()
    print("TEST 6: Example Endpoint")
    print_separator()
    
    response = requests.get(f"{BASE_URL}{API_PREFIX}/example/")
    print_response(response)
    print()


def main():
    """Main test function"""
    print("\n" + "="*70)
    print("🧪 TESTING FASTAPI APPLICATION")
    print("="*70 + "\n")
    
    print(f"Base URL: {BASE_URL}")
    print(f"API Prefix: {API_PREFIX}")
    print("\n")
    
    # Test các endpoint cơ bản
    test_root()
    test_health()
    test_upload_config()
    test_example_endpoint()
    
    # Test upload (nếu có file)
    print_separator()
    image_path = input("📁 Nhập đường dẫn file ảnh để test upload (Enter để bỏ qua): ").strip().strip('"')
    print()
    
    filename = None
    if image_path:
        filename = test_upload_image(image_path)
        
        # Test xóa file (nếu upload thành công)
        if filename:
            choice = input("❓ Bạn có muốn xóa file vừa upload không? (y/n): ").strip().lower()
            if choice == 'y':
                test_delete_image(filename)
    
    print("="*70)
    print("✅ ĐÃ HOÀN THÀNH TẤT CẢ TEST!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test bị hủy bởi người dùng")
    except requests.exceptions.ConnectionError:
        print("\n❌ Không thể kết nối đến API!")
        print(f"   Hãy đảm bảo API đang chạy tại {BASE_URL}")
    except Exception as e:
        print(f"\n❌ Lỗi không xác định: {str(e)}")
