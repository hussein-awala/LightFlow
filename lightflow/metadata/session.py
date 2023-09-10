import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

logger = logging.getLogger(__name__)

async_engine: AsyncEngine
async_session_maker: async_sessionmaker[AsyncSession]


def get_async_engine(reset=False) -> AsyncEngine:
    global async_engine
    if reset or not async_engine:
        logger.info("Create new async engine")
        async_engine = create_async_engine(
            "postgresql+asyncpg://lightflow:lightflow@localhost/lightflow",
            echo=True,
        )
    return async_engine


def get_async_session_maker(reset=False) -> async_sessionmaker[AsyncSession]:
    global async_session_maker
    if reset or not async_session_maker:
        logger.info("Create new async session")
        async_session_maker = async_sessionmaker(
            get_async_engine(reset=reset), expire_on_commit=False,
        )
    return async_session_maker


def initialize():
    get_async_session_maker(reset=True)


def provide_async_session(func):
    async def wrapper(*args, **kwargs):
        async_session_args = kwargs.pop("async_session", None)
        if not async_session_args:
            _async_session_maker = get_async_session_maker()
            async with _async_session_maker() as async_session:
                logger.error(f"Create new async session {args}, {kwargs}")
                return await func(*args, async_session=async_session, **kwargs)
        return await func(*args, async_session=async_session_args, **kwargs)

    return wrapper
