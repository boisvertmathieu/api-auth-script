from flask import Flask, request, jsonify

app = Flask(__name__)


# Endpoint pour l'authentification
@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.form
    client_id = data.get("client_id")
    client_secret = data.get("client_secret")
    grant_type = data.get("grant_type")

    if grant_type == "password":
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"error": "Username and password are required for password grant type"}), 400

    # Simuler la génération d'un token d'accès
    access_token = "fake_access_token"
    return jsonify({"access_token": access_token})


# Endpoint pour recevoir une valeur bidon en JSON
@app.route("/api/v1/pascal", methods=["GET"])
def pascal():
    # Simuler une réponse JSON bidon
    response_data = {"message": "This is a test response", "value": "dummy_value"}
    return jsonify(response_data)


# Nouvel endpoint pour traiter le body JSON (POST)
@app.route("/api/v1/pascal/runner", methods=["POST"])
def pascal_post():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()

    # Vérifier la structure du JSON
    if not data or "data" not in data or "val" not in data["data"]:
        return jsonify({"error": "Invalid JSON structure. Expected format: {'data': {'val': value}}"}), 400

    # Extraire et retourner la valeur
    return jsonify({"value": data["data"]["val"]})


@app.route("/api/v1/pascal/runner", methods=["GET"])
def pascal_get():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()

    # Vérifier la structure du JSON
    if not data or "data" not in data or "val" not in data["data"]:
        return jsonify({"error": "Invalid JSON structure. Expected format: {'data': {'val': value}}"}), 400

    # Extraire et retourner la valeur
    return jsonify({"value": data["data"]["val"]})


if __name__ == "__main__":
    app.run(debug=True)
