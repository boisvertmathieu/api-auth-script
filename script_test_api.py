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


if __name__ == "__main__":
    app.run(debug=True)
