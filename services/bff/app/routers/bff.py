from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from fastapi.responses import JSONResponse

from app.config import settings

router = APIRouter(prefix="/api/bff", tags=["bff"])


async def _request_json(
    method: str,
    service_base_url: str,
    service_path: str,
    *,
    token: str | None = None,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> tuple[int, Any]:
    headers: dict[str, str] = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            method,
            f"{service_base_url}{service_path}",
            headers=headers,
            params=params,
            json=body,
        )

    try:
        payload = response.json()
    except ValueError:
        payload = {"detail": "Resposta inválida do serviço de backend"}

    return response.status_code, payload


def _cookie_kwargs() -> dict[str, Any]:
    return {
        "httponly": True,
        "secure": settings.BFF_COOKIE_SECURE,
        "samesite": settings.BFF_COOKIE_SAMESITE,
        "max_age": settings.BFF_COOKIE_MAX_AGE,
        "path": "/",
    }


def _get_session_token(request: Request) -> str:
    token = request.cookies.get(settings.BFF_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
    return token


@router.post("/auth/register")
async def register(body: dict[str, Any]):
    status_code, payload = await _request_json(
        "POST",
        settings.AUTH_SERVICE_URL,
        "/api/auth/register",
        body=body,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.post("/auth/login")
async def login(body: dict[str, Any]):
    status_code, payload = await _request_json(
        "POST",
        settings.AUTH_SERVICE_URL,
        "/api/auth/login",
        body=body,
    )

    if status_code >= 400:
        return JSONResponse(status_code=status_code, content=payload)

    access_token = payload.get("access_token")
    if not access_token:
        raise HTTPException(status_code=502, detail="Resposta de autenticação sem token")

    response = JSONResponse(content={"authenticated": True})
    response.set_cookie(
        key=settings.BFF_COOKIE_NAME,
        value=access_token,
        **_cookie_kwargs(),
    )
    return response


@router.post("/auth/logout")
async def logout():
    response = JSONResponse(content={"authenticated": False})
    response.delete_cookie(key=settings.BFF_COOKIE_NAME, path="/")
    return response


@router.get("/session")
async def session(request: Request):
    token = _get_session_token(request)
    status_code, payload = await _request_json(
        "GET",
        settings.AUTH_SERVICE_URL,
        "/api/auth/users/me",
        token=token,
    )

    if status_code >= 400:
        response = JSONResponse(status_code=status_code, content=payload)
        response.delete_cookie(key=settings.BFF_COOKIE_NAME, path="/")
        return response

    return {"authenticated": True, "user": payload}


@router.get("/users")
async def list_users(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    token = _get_session_token(request)
    status_code, payload = await _request_json(
        "GET",
        settings.AUTH_SERVICE_URL,
        "/api/auth/users",
        token=token,
        params={"skip": skip, "limit": limit},
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.get("/users/me")
async def current_user(request: Request):
    token = _get_session_token(request)
    status_code, payload = await _request_json(
        "GET",
        settings.AUTH_SERVICE_URL,
        "/api/auth/users/me",
        token=token,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.get("/orders/")
async def list_orders(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
):
    token = _get_session_token(request)

    params: dict[str, Any] = {
        "skip": skip,
        "limit": limit,
    }
    if status_filter is not None:
        params["status"] = status_filter

    status_code, payload = await _request_json(
        "GET",
        settings.ORDERS_SERVICE_URL,
        "/api/orders/",
        token=token,
        params=params,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.post("/orders/")
async def create_order(request: Request, body: dict[str, Any]):
    token = _get_session_token(request)
    status_code, payload = await _request_json(
        "POST",
        settings.ORDERS_SERVICE_URL,
        "/api/orders/",
        token=token,
        body=body,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.patch("/orders/{order_id}/status")
async def patch_order_status(order_id: str, request: Request, body: dict[str, Any]):
    token = _get_session_token(request)
    status_code, payload = await _request_json(
        "PATCH",
        settings.ORDERS_SERVICE_URL,
        f"/api/orders/{order_id}/status",
        token=token,
        body=body,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.get("/catalog/products/")
async def list_catalog_products(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    _get_session_token(request)
    status_code, payload = await _request_json(
        "GET",
        settings.CATALOG_SERVICE_URL,
        "/api/catalog/products/",
        params={"skip": skip, "limit": limit},
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.get("/catalog/products/{ean}")
async def get_catalog_product(ean: str, request: Request):
    _get_session_token(request)
    status_code, payload = await _request_json(
        "GET",
        settings.CATALOG_SERVICE_URL,
        f"/api/catalog/products/{ean}",
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.post("/catalog/products/")
async def create_catalog_product(request: Request, body: dict[str, Any]):
    _get_session_token(request)
    status_code, payload = await _request_json(
        "POST",
        settings.CATALOG_SERVICE_URL,
        "/api/catalog/products/",
        body=body,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.put("/catalog/products/{ean}")
async def update_catalog_product(ean: str, request: Request, body: dict[str, Any]):
    _get_session_token(request)
    status_code, payload = await _request_json(
        "PUT",
        settings.CATALOG_SERVICE_URL,
        f"/api/catalog/products/{ean}",
        body=body,
    )
    return JSONResponse(status_code=status_code, content=payload)


@router.delete("/catalog/products/{ean}")
async def delete_catalog_product(ean: str, request: Request):
    _get_session_token(request)
    status_code, payload = await _request_json(
        "DELETE",
        settings.CATALOG_SERVICE_URL,
        f"/api/catalog/products/{ean}",
    )

    if status_code == status.HTTP_204_NO_CONTENT:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return JSONResponse(status_code=status_code, content=payload)
