from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

type CreateFunc[T] = Callable[[], Awaitable[T]]
type DestroyFunc[T] = Callable[[T], Awaitable[None]]


class Managed[T]:
    """
    A lifecycle container for managing global objects.

    Usage:
        http_client: Managed[ClientSession] = Managed(
            create=create_managed_aiohttp_client,
            destroy=destroy_managed_aiohttp_client,
        )

        # Manual management
        await http_client.init()
        session = http_client.get()
        await http_client.cleanup()

        # Or via lifespan
        async with http_client.lifespan():
            session = http_client.get()
    """

    _create: CreateFunc[T]
    _destroy: DestroyFunc[T] | None
    _instance: T | None

    def __init__(
        self,
        create: CreateFunc[T],
        destroy: DestroyFunc[T] | None = None,
    ):
        self._create = create
        self._destroy = destroy
        self._instance = None

    @property
    def initialized(self) -> bool:
        """Whether the instance has been initialized."""
        return self._instance is not None

    def __call__(self) -> T:
        return self.get()

    def get(self) -> T:
        """Get the instance. Raises RuntimeError if not initialized."""
        if self._instance is None:
            raise RuntimeError("Managed instance not initialized. Call init() first.")
        return self._instance

    async def init(self) -> T:
        """Initialize the instance."""
        if self._instance is not None:
            return self._instance

        self._instance = await self._create()
        return self._instance

    async def cleanup(self) -> None:
        """Clean up the instance."""
        if self._instance is None:
            return

        if self._destroy:
            await self._destroy(self._instance)

        self._instance = None

    @asynccontextmanager
    async def lifespan(self, _app: object = None) -> AsyncGenerator[T, None]:
        """Context manager for FastAPI/Starlette lifespan."""
        try:
            yield await self.init()
        finally:
            await self.cleanup()


__all__ = ("Managed",)
