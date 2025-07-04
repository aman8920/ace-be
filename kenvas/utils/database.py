from os 
from tortoise import Tortoise, run_async

def get_secret(name, default=None):
    # Try environment variable
    value = os.getenv(name)
    if value:
        return value

    # Try reading from mounted file (CSI driver path)
    path = f"/mnt/secrets-store/{name}"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read().strip()

    return default

# Load database credentials
PG_USERNAME = get_secret("POSTGRES_USER", "postgres")
PG_PASSWORD = get_secret("POSTGRES_PASSWORD", "postgres")
PG_HOST = get_secret("POSTGRES_HOST", "localhost")
PG_PORT = int(get_secret("POSTGRES_PORT", 5432))
PG_DATABASE = get_secret("POSTGRES_DB", "postgres1")

DB_URI = f"postgres://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
DB_MODELS = ["kenvas.models.db.user", "kenvas.models.db.planogram"]


async def db_init(db_url=None):
    await Tortoise.init(
        db_url=DB_URI,
        modules={"models": DB_MODELS},
    )


if __name__ == "__main__":
    run_async(db_init())
