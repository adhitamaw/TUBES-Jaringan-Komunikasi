import socket
import os

# Tentukan alamat IP server
IP = 'localhost'
# Tentukan port yang akan digunakan
PORT = 8080

# Buat socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket ke alamat IP dan port tertentu
server_socket.bind((IP, PORT))

# Listen koneksi masuk
server_socket.listen()

print('Web server sedang berjalan di http://{}:{}/'.format(IP, PORT))

while True:
    # Terima koneksi dari client
    client_socket, address = server_socket.accept()
    
    # Terima data dari client
    request = client_socket.recv(1024).decode()
    
    # Parse HTTP request
    request_parts = request.split(' ')
    method = request_parts[0]
    file_path = request_parts[1][1:]
    
    # Jika request file kosong, set file default ke index.html
    if file_path == '':
        file_path = 'index.html'
    
    # Cari file yang diminta oleh client
    file_exists = os.path.exists(file_path)
    
    if file_exists:
        # Buka file yang diminta oleh client
        with open(file_path, 'rb') as file:
            # Baca isi file
            file_contents = file.read()
            
        # Buat HTTP response message
        response_headers = 'HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n'.format(len(file_contents))
        response_body = file_contents
    else:
        # Buat HTTP response message 404 Not Found
        response_headers = 'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n'
        response_body = '<html><body><h1>404 Not Found</h1></body></html>'.encode()
    
    # Kirim HTTP response message ke client
    client_socket.sendall(response_headers.encode() + response_body)
    
    # Tutup koneksi
    client_socket.close()

"""  
1. Socket TCP dibuat dengan menggunakan socket.socket() dan kemudian 
di-bind ke alamat IP dan port tertentu menggunakan socket.bind().

2. Ketika ada koneksi masuk dari client, program menerima request HTTP dari client 
menggunakan client_socket.recv() dan kemudian mem-parse request tersebut.

3. Program mencari file yang diminta oleh client dengan menggunakan os.path.exists().

4. Jika file yang diminta ditemukan, program membuka file tersebut dan membaca isinya 
menggunakan open() dan file.read(). Kemudian program membuat HTTP response message dengan 
header yang berisi status code 200 OK dan content-type text/html, serta body yang berisi isi 
file yang diminta. Jika file tidak ditemukan, program membuat HTTP response message dengan 
header yang berisi status code 404 Not Found dan content-type text/html, serta body yang 
berisi pesan "404 Not Found".

5. Program mengirim HTTP response message ke client menggunakan client_socket.sendall().

6. Koneksi ditutup menggunakan client_socket.close().


"""