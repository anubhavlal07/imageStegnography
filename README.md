# 🔐 Image Steganography with Encryption

## 📌 Overview
This project implements **secure image steganography** using **Python, OpenCV, and Cryptography**. It allows users to **hide encrypted messages within images** and retrieve them securely using a **password**. The project also features a **PyQt5 GUI** for ease of use.

## ✨ Features
- **🔒 Encryption Before Encoding**: Uses **Fernet encryption** to secure messages before embedding them.  
- **🖼️ Image-Based Message Hiding**: Encodes messages into the least significant bits of an image.  
- **🔓 Password-Protected Decoding**: Only users with the correct password can retrieve the hidden message.  
- **🎨 GUI Interface**: Built with **PyQt5**, making it user-friendly and interactive.  
- **🛠 Minimal Data Distortion**: Ensures the image quality is preserved after encoding.  

---

## 🚀 Technologies Used
| **Technology**  | **Purpose** |
|----------------|------------|
| Python        | Core Programming Language |
| OpenCV        | Image Processing |
| Cryptography (Fernet) | Message Encryption & Decryption |
| PyQt5         | Graphical User Interface |
| Base64 & Hashlib | Key Generation & Encoding |

---

## 🛠 Installation & Setup
### 🔹 Prerequisites  
Ensure you have **Python 3.x** installed. You can check your version with:
```sh
python --version
```
## Run Locally


Clone the repository:
   ```bash
   git clone https://github.com/anubhavlal07/imageStegnography.git
cd imageStegnography
   ```
## Screenshots
**Home UI**

![App Screenshot](https://raw.githubusercontent.com/anubhavlal07/imageStegnography/refs/heads/master/Home.png)

**Encode Image**

![App Screenshot](https://raw.githubusercontent.com/anubhavlal07/imageStegnography/refs/heads/master/Encode.png)

**Decode Image**

![App Screenshot](https://raw.githubusercontent.com/anubhavlal07/imageStegnography/refs/heads/master/Decode.png)