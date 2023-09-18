import httpx
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.authorization_header_elements import get_bearer_token
from fastapi import Depends

from app.budget_breakdown.models import User
from app.infra.db import db_session
from app.json_web_token import JsonWebToken


def validate_token_and_get_user(
    token: str = Depends(get_bearer_token),
    session: Session = Depends(db_session),
):
    token_payload = TokenPayload.model_validate(JsonWebToken(token).validate())
    get_user_query = select(User).where(User.sub == token_payload.sub)
    user = session.execute(get_user_query).scalar_one_or_none()
    if user is None:
        response = httpx.get(
            "https://dev-bmbazij1sjiidmnc.us.auth0.com/userinfo",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        user_info = UserInfo.model_validate(response.json())
        user = User(**user_info.model_dump())
        session.add(user)
        session.commit()

    return user


class TokenPayload(BaseModel):
    iss: str
    sub: str
    aud: list[str]
    iat: int
    exp: int
    azp: str
    scope: str


class UserInfo(BaseModel):
    sub: str | None
    given_name: str | None
    family_name: str | None
    nickname: str | None
    name: str | None
    picture: str | None
    locale: str | None
    updated_at: str | None
    email: str
    email_verified: bool | None
