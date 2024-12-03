#!/usr/bin/env python3

import argparse
import requests
import json
import keyring
import os
import sys

def get_access_token(args):
    # Vérifier si le token est mis en cache
    token = keyring.get_password('api_client_script', 'access_token')
    if token:
        return token

    # Construire la requête d'authentification
    auth_url = args.base_url + '/api/auth'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {}

    if args.auth_method == 'smsession':
        if not args.smsession:
            print("Le SMSESSION est requis pour l'authentification SMSESSION.")
            sys.exit(1)
        headers['SMSESSION'] = args.smsession
        data = {
            'client_id': args.client_id,
            'client_secret': args.client_secret,
            'grant_type': args.grant_type,
            'scope': args.scope
        }
    elif args.auth_method == 'service-account':
        if not args.username or not args.password:
            print("Le nom d'utilisateur et le mot de passe sont requis pour le compte de service.")
            sys.exit(1)
        data = {
            'client_id': args.client_id,
            'client_secret': args.client_secret,
            'grant_type': args.grant_type,
            'username': args.username,
            'password': args.password,
            'scope': args.scope
        }
    else:
        print("Méthode d'authentification non prise en charge.")
        sys.exit(1)

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        keyring.set_password('api_client_script', 'access_token', access_token)
        return access_token
    else:
        print("Échec de l'obtention du jeton d'accès :", response.text)
        sys.exit(1)

def make_api_call(args, access_token):
    url = args.base_url + args.url_path
    headers = {'Authorization': 'Bearer ' + access_token}

    # Ajouter des en-têtes supplémentaires
    if args.headers:
        for header in args.headers:
            if ':' not in header:
                print("Les en-têtes doivent être au format 'Clé: Valeur'.")
                sys.exit(1)
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()

    # Gérer le corps de la requête
    body = None
    if args.body:
        if os.path.isfile(args.body):
            with open(args.body, 'r') as f:
                body = json.load(f)
        else:
            try:
                body = json.loads(args.body)
            except json.JSONDecodeError:
                print("Le corps JSON est invalide.")
                sys.exit(1)
        # Définir Content-Type si non spécifié
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

    method = args.method.upper()
    response = None

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method in ['POST', 'PUT', 'PATCH']:
            response = requests.request(method, url, headers=headers, json=body)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print("Méthode HTTP non prise en charge.")
            sys.exit(1)

        if response.status_code == 401:
            # Le token a peut-être expiré, le supprimer du cache et réessayer
            keyring.delete_password('api_client_script', 'access_token')
            access_token = get_access_token(args)
            headers['Authorization'] = 'Bearer ' + access_token
            response = requests.request(method, url, headers=headers, json=body)
    except Exception as e:
        print("Erreur lors de l'appel API :", e)
        sys.exit(1)

    print("Code de statut :", response.status_code)
    print("Réponse :", response.text)

def main():
    parser = argparse.ArgumentParser(description='Script Client API')
    parser.add_argument('--auth-method', choices=['smsession', 'service-account'], required=True, help='Méthode d\'authentification à utiliser.')
    parser.add_argument('--smsession', help='Token SMSESSION (requis pour smsession).')
    parser.add_argument('--client-id', required=True, help='Identifiant du client.')
    parser.add_argument('--client-secret', required=True, help='Secret du client.')
    parser.add_argument('--grant-type', default='password', help='Type de grant OAuth2.')
    parser.add_argument('--username', help='Nom d\'utilisateur (requis pour service-account).')
    parser.add_argument('--password', help='Mot de passe (requis pour service-account).')
    parser.add_argument('--scope', default='', help='Scopes OAuth2.')
    parser.add_argument('--method', required=True, help='Méthode HTTP (GET, POST, etc.).')
    parser.add_argument('--url-path', required=True, help='Chemin de l\'API à appeler.')
    parser.add_argument('--headers', action='append', help='En-têtes supplémentaires (format: "Clé: Valeur").')
    parser.add_argument('--body', help='Corps JSON en tant que chaîne ou chemin vers un fichier JSON.')
    parser.add_argument('--base-url', default='https://pise.d.com', help='URL de base pour les appels API.')

    args = parser.parse_args()

    # Validation des arguments requis en fonction de la méthode d'authentification
    if args.auth_method == 'smsession' and not args.smsession:
        parser.error("--smsession est requis lorsque --auth-method est 'smsession'.")
    if args.auth_method == 'service-account' and (not args.username or not args.password):
        parser.error("--username et --password sont requis lorsque --auth-method est 'service-account'.")

    access_token = get_access_token(args)
    make_api_call(args, access_token)

if __name__ == '__main__':
    main()
