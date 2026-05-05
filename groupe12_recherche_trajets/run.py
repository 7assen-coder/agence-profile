from app import create_app

# Crée l'application Flask
app = create_app()

if __name__ == "__main__":
    # Lance le serveur sur le port 5012 (groupe 12)
    app.run(debug=True, port=5012)