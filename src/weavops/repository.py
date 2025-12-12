import asyncio
import os
from urllib.parse import quote, urlparse, urlunparse

from .env import REPO_BRANCH, REPO_DIR, REPO_PASSWORD, REPO_URL, REPO_USERNAME
from .managed import Managed


class Repository:
    dir: str
    url: str
    username: str | None
    password: str | None
    branch: str

    def __init__(
        self,
        dir: str,
        url: str,
        username: str | None = None,
        password: str | None = None,
        branch: str = "main",
    ):
        self.dir = dir
        self.url = url
        self.username = username
        self.password = password
        self.branch = branch

    def _build_url(self) -> str:
        """Build URL with optional authentication (username:password@host format)."""
        # If no credentials provided, return the original URL for public repos
        if not self.username or not self.password:
            return self.url

        parsed = urlparse(self.url)
        # URL-encode username and password to handle special characters like @, :, /
        encoded_username = quote(self.username, safe="")
        encoded_password = quote(self.password, safe="")
        auth_netloc = f"{encoded_username}:{encoded_password}@{parsed.hostname}"
        if parsed.port:
            auth_netloc += f":{parsed.port}"
        return urlunparse(parsed._replace(netloc=auth_netloc))

    async def _run_git(self, *args: str, cwd: str | None = None) -> None:
        """Run a git command and raise on failure."""
        proc = await asyncio.create_subprocess_exec(
            "git",
            *args,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(
                f"git {' '.join(args)} failed: {stderr.decode().strip()}"
            )

    async def init(self) -> None:
        """Initialize the repository: clone if not exists, or pull if exists."""
        url = self._build_url()

        if not os.path.exists(self.dir):
            # Directory doesn't exist, clone the repository
            await self._run_git(
                "clone", "--branch", self.branch, "--single-branch", url, self.dir
            )
        else:
            # Directory exists, verify it's a git repository
            git_dir = os.path.join(self.dir, ".git")
            if not os.path.isdir(git_dir):
                raise RuntimeError(f"{self.dir} exists but is not a git repository")

            # Set remote URL and pull
            await self._run_git("remote", "set-url", "origin", url, cwd=self.dir)
            await self._run_git("fetch", "origin", self.branch, cwd=self.dir)
            await self._run_git("checkout", self.branch, cwd=self.dir)
            await self._run_git("pull", "origin", self.branch, cwd=self.dir)


async def _create_repository() -> Repository:
    repo = Repository(
        dir=REPO_DIR,
        url=REPO_URL,
        username=REPO_USERNAME,
        password=REPO_PASSWORD,
        branch=REPO_BRANCH,
    )
    await repo.init()
    return repo


managed_repository = Managed(
    create=_create_repository,
)
