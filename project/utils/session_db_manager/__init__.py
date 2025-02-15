from sqlalchemy.ext.asyncio import AsyncSession


class SessionDBManager:
    def __init__(self, session_db: AsyncSession = None):
        self.session_db = session_db
        self._own_session = False

    async def get_session(self) -> AsyncSession:
        if self.session_db is None:
            from project.database.mariadb import async_session
            
            self._own_session = True
            self.session_db = async_session()
        return self.session_db

    async def close_session(self):
        if self._own_session and self.session_db:
            await self.session_db.close()
