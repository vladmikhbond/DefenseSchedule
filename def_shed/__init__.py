from flask import Flask

def create_app():
    """Фабрична функція для створення Flask-додатка"""
    app = Flask(__name__)
    
    # Налаштування конфігурації (можна імпортувати з файлу)
    # app.config.from_object("config.Config")

    # Імпорт та реєстрація Blueprint'ів
    from .routes import bp
    app.register_blueprint(bp)

    return app








