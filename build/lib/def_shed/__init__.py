from flask import Flask

def create_app():
    """Фабрична функція для створення Flask-додатка"""
    app = Flask(__name__)
     # Налаштування конфігурації (можна імпортувати з файлу)
    # app.config.from_object("config.Config")

    # Імпорт маршрутів та реєстрація Blueprint'ів
    from .routes import main
    app.register_blueprint(main)

    return app








