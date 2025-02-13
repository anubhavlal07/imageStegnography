import cv2
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# 🔹 Generate a key from the password
def generate_key(password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key[:32])

# 🔹 Encrypt and Decrypt Message
def encrypt_message(message: str, password: str) -> str:
    key = generate_key(password)
    cipher = Fernet(key)
    return base64.b64encode(cipher.encrypt(message.encode())).decode()

def decrypt_message(encrypted_message: str, password: str) -> str:
    try:
        key = generate_key(password)
        cipher = Fernet(key)
        return cipher.decrypt(base64.b64decode(encrypted_message)).decode()
    except Exception:
        return None

# 🔹 Convert Text to Binary
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8) if int(binary[i:i+8], 2) != 0)

# 🔹 Encode & Decode Functions
def encode_message(image_path, message, password, output_path):
    img = cv2.imread(image_path)
    if img is None:
        return "❌ Error: Image not found!"

    encrypted_msg = encrypt_message(message, password) + '###'
    binary_msg = text_to_binary(encrypted_msg)

    h, w, _ = img.shape
    max_bits = h * w * 3

    if len(binary_msg) > max_bits:
        return "❌ Error: Message too long for this image!"

    idx = 0
    for row in range(h):
        for col in range(w):
            for channel in range(3):
                if idx < len(binary_msg):
                    img[row, col, channel] = (img[row, col, channel] & 254) | int(binary_msg[idx])
                    idx += 1
                else:
                    break
            if idx >= len(binary_msg):
                break
        if idx >= len(binary_msg):
            break

    cv2.imwrite(output_path, img)
    return f"✅ Message successfully encoded in {output_path}"

def decode_message(image_path, password):
    img = cv2.imread(image_path)
    if img is None:
        return "❌ Error: Image not found!"

    binary_msg = ""
    for row in img:
        for pixel in row:
            for channel in range(3):
                binary_msg += str(pixel[channel] & 1)

    hidden_text = binary_to_text(binary_msg)
    if '###' in hidden_text:
        hidden_text = hidden_text.split('###')[0]
        decrypted_message = decrypt_message(hidden_text, password)

        return f"🔓 Decrypted message: {decrypted_message}" if decrypted_message else "❌ Incorrect password!"
    else:
        return "❌ No hidden message found!"

# 🔹 PyQt5 GUI with Black Theme and Greenish Foreground
class SteganographyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🔐 Secure Image Steganography")
        self.setGeometry(300, 200, 500, 450)
        self.setStyleSheet("background-color: black; color: #fff;")

        # Labels
        self.label = QLabel("📂 Image Steganographer", self)
        self.label.setFont(QFont("Arial", 12))
        self.label.setStyleSheet("color: #fff;")

        # Select Image Button
        self.btn_select = QPushButton("🖼️ Select Image", self)
        self.btn_select.clicked.connect(self.select_image)
        self.btn_select.setStyleSheet("background-color: #000000; color: #fff; border: 2px solid #000000;")

        # Message Input
        self.msg_input = QTextEdit(self)
        self.msg_input.setPlaceholderText("Enter your secret message here...")
        self.msg_input.setStyleSheet("background-color: #000000; color: #fff; border: 1px solid #000000;")

        # Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password for encryption/decryption")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: #000000; color: #fff; border: 1px solid #000000;")

        # Encode & Decode Buttons
        self.btn_encode = QPushButton("🔒 Encode Message", self)
        self.btn_encode.clicked.connect(self.encode_message)
        self.btn_encode.setStyleSheet("background-color: #000000; color: #fff; border: 2px solid #000000;")

        self.btn_decode = QPushButton("🔓 Decode Message", self)
        self.btn_decode.clicked.connect(self.decode_message)
        self.btn_decode.setStyleSheet("background-color: #000000; color: #fff; border: 2px solid #000000;")

        # Result Display
        self.result_label = QLabel("", self)
        self.result_label.setStyleSheet("color: #fff; font-size: 14px;")
        self.result_label.setWordWrap(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.msg_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_encode)
        layout.addWidget(self.btn_decode)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.label.setText(f"✔ Selected: {file_path.split('/')[-1]}")

    def encode_message(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "⚠ Please select an image first!")
            return

        message = self.msg_input.toPlainText().strip()
        password = self.password_input.text().strip()
        if not message or not password:
            QMessageBox.warning(self, "Error", "⚠ Message and password cannot be empty!")
            return

        output_path = "encoded_image.png"
        result = encode_message(self.image_path, message, password, output_path)
        self.result_label.setText(result)

        # Clear fields after encoding
        self.msg_input.clear()
        self.password_input.clear()

        if "✅" in result:
            QMessageBox.information(self, "Success", f"✔ Message encoded! Saved as {output_path}")

    def decode_message(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "⚠ Please select an image first!")
            return

        password = self.password_input.text().strip()
        if not password:
            QMessageBox.warning(self, "Error", "⚠ Please enter the password for decryption!")
            return

        result = decode_message(self.image_path, password)
        self.result_label.setText(result)

        # Clear password after decryption
        self.password_input.clear()

        QMessageBox.information(self, "Decryption Result", result)


# Run the App
if __name__ == "__main__":
    app = QApplication([])
    window = SteganographyApp()
    window.show()
    app.exec_()
