import socket
import threading
import requests
import json
import datetime
import os

# 소켓 서버 설정
HOST = '0.0.0.0'  # 모든 네트워크 인터페이스에서 연결을 허용
PORT = 8001  # 안드로이드 클라이언트와 통신할 포트

# 절대 경로 설정
base_dir = "/home/MWmid325/request"  # PythonAnywhere의 경로
#base_dir = "/home/your_project_directory/request"  # PythonAnywhere의 경로에 맞게 설정

def handle_client(client_socket):
    try:
        # Django 서버로 요청을 보내고 응답을 받아 처리
        response = requests.get("https://mwmid325.pythonanywhere.com/api_root/Post/")
        if response.status_code == 200:
            # JSON 응답에서 이미지 URL을 가져와 JSON 형식으로 변환
            json_data = response.json()
            
            # json_data가 리스트 형태인지 확인하고, 그렇지 않다면 리스트로 변환
            if isinstance(json_data, list):
                image_urls = [item["image"] for item in json_data if "image" in item]
            elif "results" in json_data:  # 'results' 키가 있을 경우
                image_urls = [item["image"] for item in json_data["results"] if "image" in item]
            else:
                image_urls = []

            response_data = json.dumps({"images": image_urls})
            
            # 현재 시간에 따라 파일 생성
            current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            file_path = os.path.join(base_dir, f"{current_time}.bin")
            
            # 응답 데이터를 파일에 저장
            with open(file_path, 'w') as file:
                file.write(response_data)

            # 전송할 데이터를 콘솔에 출력하여 확인
            print("Sending data to Android client:", response_data)
            
            # 안드로이드 클라이언트에 응답 전송
            client_socket.sendall(response_data.encode('utf-8'))
            print("Data sent to Android client.")
        else:
            client_socket.sendall(b"Error: Could not fetch data from Django")
            print("Error fetching data from Django")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
