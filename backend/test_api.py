import requests

BASE_URL = "http://localhost:5000"

def test_health():
    res = requests.get(f"{BASE_URL}/api/health")
    print("Health:", res.json())

def test_analyze(image_path, label):
    print(f"\n--- Testing: {label} ---")
    try:
        with open(image_path, 'rb') as f:
            res = requests.post(f"{BASE_URL}/api/analyze", files={"image": f})
        print("Status Code:", res.status_code)
        print("Response JSON:", res.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_health()
    test_analyze(r"C:\Users\Ruthu\.gemini\antigravity\brain\d5667750-ca9f-4e6c-9b0e-e4084d5ca4cc\one_face_1789985107207.png", "One Face")
    test_analyze(r"C:\Users\Ruthu\.gemini\antigravity\brain\d5667750-ca9f-4e6c-9b0e-e4084d5ca4cc\multiple_faces_1789985146329.png", "Multiple Faces")
    test_analyze(r"C:\Users\Ruthu\.gemini\antigravity\brain\d5667750-ca9f-4e6c-9b0e-e4084d5ca4cc\no_face_1789985174033.png", "No Face")
    test_analyze(r"C:\Users\Ruthu\Desktop\FaceSenseAI\invalid_file.txt", "Invalid File")
    
    res = requests.get(f"{BASE_URL}/api/history")
    print("\nHistory records count:", len(res.json()))
