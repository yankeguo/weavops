import logging
from contextlib import asynccontextmanager

from fastmcp import FastMCP

from .repository import managed_repository

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _mcp_lifespan(server: FastMCP):
    async with managed_repository.lifespan() as repository:
        yield {"repository": repository}


mcp = FastMCP("weavops", lifespan=_mcp_lifespan)
