import os
import sys
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

load_dotenv()

class WeatherThread(QThread):
    weather_fetched = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, city):
        super().__init__()
        self.city = city
        self.API_KEY = os.getenv("API_KEY")
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    def run(self):
        try:
            url = f"{self.BASE_URL}?q={self.city}&appid={self.API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data["cod"] == 200:
                self.weather_fetched.emit(data)
            else:
                self.error_occurred.emit("City not found 😢")
        except requests.exceptions.RequestException:
            self.error_occurred.emit("Network error. Please check your connection.")
        except Exception as e:
            self.error_occurred.emit("An error occurred while fetching weather data.")

class ModernWeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setFixedSize(400, 700)
        self.setStyleSheet(self.get_main_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        self.create_header(main_layout)
        
        # Search section
        self.create_search_section(main_layout)
        
        # Weather display section
        self.create_weather_section(main_layout)
        
        # Status bar (for loading/error messages)
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                padding: 10px;
                background: transparent;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        main_layout.addStretch()
        
    def create_header(self, layout):
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 10)
        
        title = QLabel("Weather")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        subtitle = QLabel("Get current weather information")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                background: transparent;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)
        
    def create_search_section(self, layout):
        search_frame = QFrame()
        search_frame.setFixedHeight(80)
        search_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: none;
            }
        """)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(20, 15, 20, 15)
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name...")
        self.city_input.setStyleSheet("""
            QLineEdit {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 16px;
                color: #495057;
            }
            QLineEdit:focus {
                border-color: #667eea;
                background: white;
            }
        """)
        self.city_input.returnPressed.connect(self.search_weather)
        
        self.search_btn = QPushButton("🔍")
        self.search_btn.setFixedSize(50, 50)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4190);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4e5bc6, stop:1 #5e377e);
            }
        """)
        self.search_btn.clicked.connect(self.search_weather)
        
        search_layout.addWidget(self.city_input)
        search_layout.addWidget(self.search_btn)
        layout.addWidget(search_frame)
        
    def create_weather_section(self, layout):
        self.weather_frame = QFrame()
        self.weather_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: none;
            }
        """)
        
        self.weather_layout = QVBoxLayout(self.weather_frame)
        self.weather_layout.setContentsMargins(20, 20, 20, 20)
        self.weather_layout.setSpacing(20)
        
        # Initially show welcome message
        self.show_welcome_message()
        
        layout.addWidget(self.weather_frame)
        
    def show_welcome_message(self):
        self.clear_weather_display()
        
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-radius: 15px;
                border: 1px solid #dee2e6;
            }
        """)
        
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setContentsMargins(30, 40, 30, 40)
        
        icon_label = QLabel("🌤️")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 60px;
                background: transparent;
                margin-bottom: 20px;
            }
        """)
        
        welcome_text = QLabel("Welcome to Weather App")
        welcome_text.setAlignment(Qt.AlignCenter)
        welcome_text.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                margin-bottom: 10px;
            }
        """)
        
        instruction_text = QLabel("Enter a city name to get current weather information")
        instruction_text.setAlignment(Qt.AlignCenter)
        instruction_text.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                background: transparent;
            }
        """)
        instruction_text.setWordWrap(True)
        
        welcome_layout.addWidget(icon_label)
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addWidget(instruction_text)
        
        self.weather_layout.addWidget(welcome_frame)
        
    def display_weather(self, data):
        self.clear_weather_display()
        
        main = data["main"]
        weather = data["weather"][0]
        city_name = data["name"]
        country = data["sys"]["country"]
        
        # Weather icon mapping
        weather_icons = {
            "clear sky": "☀️",
            "few clouds": "🌤️",
            "scattered clouds": "⛅",
            "broken clouds": "☁️",
            "shower rain": "🌦️",
            "rain": "🌧️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️"
        }
        
        weather_icon = weather_icons.get(weather["description"], "🌤️")
        
        # Main weather card
        weather_card = QFrame()
        weather_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
                border: none;
            }
        """)
        
        card_layout = QVBoxLayout(weather_card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        
        # City name
        city_label = QLabel(f"{city_name}, {country}")
        city_label.setAlignment(Qt.AlignCenter)
        city_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                margin-bottom: 10px;
            }
        """)
        
        # Weather icon
        icon_label = QLabel(weather_icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 80px;
                background: transparent;
                margin: 20px 0;
            }
        """)
        
        # Temperature
        temp_label = QLabel(f"{int(main['temp'])}°C")
        temp_label.setAlignment(Qt.AlignCenter)
        temp_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                background: transparent;
                margin-bottom: 10px;
            }
        """)
        
        # Description
        desc_label = QLabel(weather["description"].title())
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 18px;
                background: transparent;
            }
        """)
        
        card_layout.addWidget(city_label)
        card_layout.addWidget(icon_label)
        card_layout.addWidget(temp_label)
        card_layout.addWidget(desc_label)
        
        # Details section
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                border: 1px solid #e9ecef;
            }
        """)
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setContentsMargins(20, 20, 20, 20)
        
        # Humidity
        humidity_row = self.create_detail_row("💧", "Humidity", f"{main['humidity']}%")
        details_layout.addWidget(humidity_row)
        
        # Feels like
        feels_like_row = self.create_detail_row("🌡️", "Feels like", f"{int(main['feels_like'])}°C")
        details_layout.addWidget(feels_like_row)
        
        # Pressure
        pressure_row = self.create_detail_row("📊", "Pressure", f"{main['pressure']} hPa")
        details_layout.addWidget(pressure_row)
        
        self.weather_layout.addWidget(weather_card)
        self.weather_layout.addWidget(details_frame)
        
    def create_detail_row(self, icon, label, value):
        row = QFrame()
        row.setStyleSheet("QFrame { background: transparent; }")
        
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 5, 0, 5)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background: transparent;
                min-width: 30px;
            }
        """)
        
        text_label = QLabel(label)
        text_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 16px;
                background: transparent;
            }
        """)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignRight)
        value_label.setStyleSheet("""
            QLabel {
                color: #212529;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        layout.addWidget(value_label)
        
        return row
        
    def clear_weather_display(self):
        while self.weather_layout.count():
            child = self.weather_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def search_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.status_label.setText("Please enter a city name")
            return
            
        self.status_label.setText("Loading weather data...")
        self.search_btn.setEnabled(False)
        self.city_input.setEnabled(False)
        
        self.weather_thread = WeatherThread(city)
        self.weather_thread.weather_fetched.connect(self.on_weather_fetched)
        self.weather_thread.error_occurred.connect(self.on_error)
        self.weather_thread.start()
        
    def on_weather_fetched(self, data):
        self.display_weather(data)
        self.status_label.setText("")
        self.search_btn.setEnabled(True)
        self.city_input.setEnabled(True)
        
    def on_error(self, error_message):
        self.status_label.setText(error_message)
        self.search_btn.setEnabled(True)
        self.city_input.setEnabled(True)
        
    def get_main_stylesheet(self):
        return """
        QMainWindow {
            background: #f8f9fa;
        }
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        """

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = ModernWeatherApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()