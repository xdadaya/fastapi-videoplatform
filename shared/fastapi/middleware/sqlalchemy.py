from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from app.database.db import reset_session_context, session, set_session_context


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        session_id = str(uuid4())
        context = set_session_context(session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as exception:
            raise exception
        finally:
            await session.remove()
            reset_session_context(context)
