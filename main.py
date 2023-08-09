import sys
import socket
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidget, QPushButton, QWidget
from ping3 import ping

class IPScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('IP Scanner')
        self.setGeometry(100, 100, 300, 400)

        self.ip_list_widget = QListWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.ip_list_widget)

        self.scan_button = QPushButton('Scan', self)
        self.scan_button.clicked.connect(self.scan_network)
        layout.addWidget(self.scan_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def scan_network(self):
        self.ip_list_widget.clear()
        
        my_ip = socket.gethostbyname(socket.gethostname())
        ip_range = [".".join([*my_ip.split(".")[:3], str(i)]) for i in range(1, 255)]
        thread_lock = threading.Lock()
        threads = []
                
        def scan_ip(ip):
            try:
                if ping(str(ip)) != False:
                    try:
                        hostname = socket.gethostbyaddr(str(ip))[0]
                    except socket.herror as e:
                        hostname = "unknown hostname"
                    thread_lock.acquire()
                    item_text = str(ip) + " : " + hostname
                    self.ip_list_widget.addItem(item_text)
                    thread_lock.release()
            except:
                pass

        for ip in ip_range:
            ip = str(ip)
            thread = threading.Thread(target=scan_ip, args=(ip, ))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IPScannerApp()
    window.show()
    sys.exit(app.exec())