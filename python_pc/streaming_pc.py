import socket
import cv2
import numpy as np

def isImageData(data, length):
    return length > 2

host = 'IP Address'
port = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))
print(f"서버에 연결되었습니다.")

cv2.namedWindow('Live Stream', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Live Stream', 1920, 1080)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1920, 1080))

try:
    while True:
        data_size = client_socket.recv(16)
        if not data_size:
            break

        try:
            if isImageData(data_size, len(data_size)):
                data_size = int(data_size)
                data = b''
                while len(data) < data_size:
                    packet = client_socket.recv(min(data_size - len(data), 4096))
                    if not packet:
                        break
                    data += packet

                if len(data) == data_size:
                    img_data = np.frombuffer(data, dtype=np.uint8)
                    img = cv2.imdecode(img_data, 1)
                    cv2.imshow('Live Stream', img)

                out.write(img)

            else:
                data_size = int(data_size.decode('utf-8'))
                data = client_socket.recv(data_size)
                decoded_data = data.decode('utf-8')
                print(f"서버로부터 받은 데이터: {decoded_data}")

        except Exception as e:
            print(f"Error: {e}")

        if cv2.waitKey(1) == 27:
            break

finally:
    client_socket.close()
    out.release()
    cv2.destroyAllWindows()
