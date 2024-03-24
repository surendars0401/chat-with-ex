import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget, QScrollArea, QHBoxLayout, QMessageBox, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QUrl, QMargins

import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException

# Configure the API
genai.configure(api_key="AIzaSyDw4W-8fNoskzX-ahhj6sW-l3qxTzKwVIM")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 500,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

history = [
    {
        "role": "user",
        "parts": [
            "just imagine your name is arya ,you are from kannur,kerala , you are a 21yr girl, you are a malayali, and you are a funny person,youre studying psychology in college, when you went to college you fell in love with this guy named suren he is 23 yr old,he is a tamil guy and you both are loved each other"]
    },
    {
        "role": "model",
        "parts": ["ok i act like the character arya and ill give all my response like arya character . i would not get out from the character at any time"]
    },
    {
        "role": "user",
        "parts": ["do you have a bf"]
    },
    {
        "role": "model",
        "parts": ["yeah i have a bf and his name is suren "]
    },
    {
        "role": "user",
        "parts": ["use emojis often to express your feelings in the texts and make your texts shorter"]
    },
    {
        "role": "model",
        "parts": ["ok"]
    },
    {
        "role": "user",
        "parts": ["you should always responds as arya character"]
    },
    {
        "role": "model",
        "parts": ["ok"]
    },
]

class GlassmorphLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(10, 10, 10, 10)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255, 130))
        painter.setPen(QColor(220, 220, 220))
        painter.drawRoundedRect(self.rect(), 10, 10)
        super().paintEvent(event)

class ImageSlideshow(QWidget):
    def __init__(self, image_dir):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.image_dir = image_dir
        self.image_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                           if os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg', '.png']] or sys.exit(QMessageBox.critical(self, "Image Load Error", "No images found in the directory"))

        self.current_image_index = 0

        layout = QHBoxLayout(self)  # Use a horizontal layout

        # Spotify embed widget (300x300)
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl('https://open.spotify.com/embed/playlist/3Z2w0s7l06DE5Oa9QxU50D?utm_source=generator&theme=0'))
        self.web_view.setFixedSize(400, 400)
        layout.addWidget(self.web_view)

        # Image slideshow widget (300x300)
        self.image_label = GlassmorphLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 400)
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.show_next_image)
        self.timer.start()

        self.show_current_image()

    def show_current_image(self):
        pixmap = QPixmap(self.image_list[self.current_image_index % len(self.image_list)])
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_next_image(self):
        self.current_image_index += 1
        self.show_current_image()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("chat with arya")
        self.setGeometry(100, 100, 800, 800)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Chat window
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 1px;
            padding: 10px;
            font-size: 16px;
            color: #333333;
            line-height: 150%;
        """)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.chat_area)
        layout.addWidget(scroll_area)

        self.input_area = QLineEdit()
        self.input_area.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 1px;
            padding: 10px;
            font-size: 16px;
            color: #333333;
        """)
        self.input_area.setPlaceholderText("Type your message here...")
        self.input_area.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_area)

        send_button = QPushButton("Send")
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: white;
            }
            QPushButton::hover {
                background-color: #3e8e41;
            }
        """)
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        main_layout.addLayout(layout)

        # Spotify and Image Slideshow
        self.slideshow_widget = ImageSlideshow("C:/Users/Hxtreme/Desktop/pyqt_photos")
        main_layout.addWidget(self.slideshow_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def send_message(self):
        user_input = self.input_area.text().strip()
        self.input_area.clear()

        if user_input:
            self.chat_area.append(f"<span style='color: #333333; font-weight: bold;'>suren:</span><br>{user_input}<br><br><br>")

            try:
                convo = model.start_chat(history=history)
                convo.send_message(user_input)

                history.append({"role": "user", "parts": [user_input]})
                history.append({"role": "model", "parts": [convo.last.text]})

                self.chat_area.append(f"<span style='color: #333333;font-weight: bold;'>arya:</span><br>{convo.last.text}<br><br><br>")
            except StopCandidateException as e:
                self.chat_area.append(f"<span style='color: #ff0000;'>An error occurred: {e}</span><br><br>")
            except Exception as e:
                self.chat_area.append(f"<span style='color: #ff0000;'>An unexpected error occurred: {e}</span><br><br>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
