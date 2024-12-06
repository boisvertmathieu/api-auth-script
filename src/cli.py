import argparse


def create_parser() -> argparse.ArgumentParser:
    # TODO : Réutiliser les définitions de 'help', et 'choices' pour éviter la duplication

    """Crée et configure le parser d'arguments."""
    parser = argparse.ArgumentParser(description="Script pour appeler une API en production")
    subparsers = parser.add_subparsers(dest="mode", help="Mode d'exécution")

    # Sous-commande normal
    normal_parser = subparsers.add_parser("normal", help="Mode normal: Appel unique")
    normal_parser.add_argument(
        "--grant-type", default="password", help="Type de grant_type OAuth2 (ex: 'password'). Par défaut : 'password'"
    )
    normal_parser.add_argument("--base-path", required=True, help="Le path de base de l'API (ex: /api/v1)")
    normal_parser.add_argument("--endpoint", default="", help="Endpoint supplémentaire (ex: /pascal)")
    normal_parser.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE", "PATCH"], help="Méthode HTTP")
    normal_parser.add_argument("--headers", nargs="*", help='Headers personnalisés (ex: "X-Request-Id=1234")')
    normal_parser.add_argument("--body", type=str, help='Body JSON (ex: \'{"key":"value"}\')')

    # Sous-commande runner
    runner_parser = subparsers.add_parser("runner", help="Mode runner: Appel multiple avec différents bodies")
    runner_parser.add_argument("runner_dir", help="Chemin du répertoire contenant les fichiers JSON")
    runner_parser.add_argument(
        "--grant-type", default="password", help="Type de grant_type OAuth2 (ex: 'password'). Par défaut : 'password'"
    )
    runner_parser.add_argument("--base-path", required=True, help="Le path de base de l'API (ex: /api/v1)")
    runner_parser.add_argument("--endpoint", default="", help="Endpoint supplémentaire (ex: /pascal)")
    runner_parser.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE", "PATCH"], help="Méthode HTTP")
    runner_parser.add_argument("--headers", nargs="*", help='Headers personnalisés (ex: "X-Request-Id=1234")')

    return parser
