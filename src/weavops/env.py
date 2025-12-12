import os
from typing import cast

from dotenv import load_dotenv

load_dotenv()  # pyright: ignore[reportUnusedCallResult]

HOST = os.getenv("WEAVOPS_HOST", "0.0.0.0")

PORT = int(os.getenv("WEAVOPS_PORT", "8000"))

REPO_DIR = os.getenv("WEAVOPS_REPO_DIR", "repo")

REPO_URL: str = cast(str, os.getenv("WEAVOPS_REPO_URL"))

REPO_USERNAME = os.getenv("WEAVOPS_REPO_USERNAME")

REPO_PASSWORD = os.getenv("WEAVOPS_REPO_PASSWORD")

REPO_BRANCH = os.getenv("WEAVOPS_REPO_BRANCH", "main")

if not REPO_URL:
    raise ValueError("WEAVOPS_REPO_URL is required")
