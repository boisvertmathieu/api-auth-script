import os
import sys
from dotenv import load_dotenv
from src.config import APIConfig
from src.cli import create_parser
from src.auth import authenticate
from src.runner import run_normal_mode, run_runner_mode


def main():
    # Charger les variables d'environnement
    load_dotenv()

    # Récupérer les secrets depuis .env
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    smsession = os.getenv("SMSESSION")

    # Parser les arguments
    parser = create_parser()
    args = parser.parse_args()

    # Si aucune sous-commande n'est fournie, afficher l'aide et quitter
    if args.mode is None:
        parser.print_help()
        sys.exit(1)

    # Créer la configuration
    config = APIConfig(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        smsession=smsession,
        grant_type=args.grant_type,
        base_path=args.base_path,
        endpoint=args.endpoint,
        method=args.method,
        headers=args.headers,
        body=getattr(args, "body", None),
        runner_mode=(args.mode == "runner"),
        runner_dir=getattr(args, "runner_dir", None),
    )

    # Authentification
    token = authenticate(config)

    # Exécuter en fonction du mode
    if config.runner_mode:
        run_runner_mode(config, token)
    else:
        run_normal_mode(config, token)


if __name__ == "__main__":
    main()
