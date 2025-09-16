import os
from . import create_app
from .services.db import bootstrap_admin

app = create_app()

# Створення початкового адміна (якщо відсутній)
with app.app_context():
	bootstrap_admin()
    
if __name__ == "__main__":
	# Локальний запуск
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
