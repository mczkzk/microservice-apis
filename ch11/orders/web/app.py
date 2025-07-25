import os
from pathlib import Path

import yaml
from fastapi import FastAPI
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from starlette import status
from starlette.middleware.base import (
    RequestResponseEndpoint,
    BaseHTTPMiddleware,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from orders.web.api.auth import decode_and_validate_token

app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

oas_doc = yaml.safe_load((Path(__file__).parent / "../../oas.yaml").read_text())


app.openapi = lambda: oas_doc


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if os.getenv("AUTH_ON", "False") != "True":
            request.state.user_id = "test"
            return await call_next(request)

        # ドキュメントとOpenAPI仕様書は認証をスキップ
        if request.url.path in ["/docs/orders", "/openapi/orders.json"]:
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")  # Authorizationヘッダー全体
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                },
            )
        try:
            auth_token = bearer_token.split(" ")[1].strip()  # トークン部分を取得 JWT
            token_payload = decode_and_validate_token(auth_token)  # トークンの検証
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:
            # 認証エラーの場合は401 Unauthorizedを返す
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)},
            )
        else:
            request.state.user_id = token_payload["sub"]
        return await call_next(request)


app.add_middleware(AuthorizeRequestMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可
    allow_credentials=True,  # クロスオリジンリクエストの Cookie をサポート
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)


from orders.web.api import api
