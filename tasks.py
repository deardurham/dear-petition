import invoke
import kubesae
from colorama import init

init(autoreset=True)


ns = invoke.Collection()
ns.add_collection(kubesae.image)

ns.configure(
    {
        "app": "petition",
        "aws": {"region": "us-east-1"},
        "container_name": "app",
        "run": {
            "echo": True,
            "pty": True,
            "env": {"COMPOSE_FILE": "docker-compose.yml:docker-compose-deploy.yml"},
        },
    }
)
