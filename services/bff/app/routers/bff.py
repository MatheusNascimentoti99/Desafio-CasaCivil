from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from fastapi.responses import JSONResponse

from app.config import settings

router = APIRouter(prefix="/api/bff", tags=["bff"])


async def _load_product_names_by_ean(product_eans: set[str]) -> dict[str, str]:
    if not product_eans:
        return {}

    names: dict[str, str] = {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        for ean in product_eans:
            response = await client.get(f"{settings.CATALOG_SERVICE_URL}/api/catalog/products/{ean}")
            if response.status_code >= 400:
                continue

            try:
                payload = response.json()
            except ValueError:
                continue

            name = payload.get("name")
            if isinstance(name, str) and name:
                names[ean] = name

    return names


async def _enrich_orders_with_product_name(orders_payload: Any) -> Any:
    if not isinstance(orders_payload, list):
        return orders_payload

    product_eans: set[str] = set()
    for order in orders_payload:
        if not isinstance(order, dict):
            continue

        items = order.get("items", [])
        if not isinstance(items, list):
            continue

        for item in items:
            if isinstance(item, dict):
                ean = item.get("product_ean")
                if isinstance(ean, str) and ean:
                    product_eans.add(ean)

    product_names = await _load_product_names_by_ean(product_eans)
    if not product_names:
        return orders_payload

    for order in orders_payload:
        if not isinstance(order, dict):
            continue

        items = order.get("items", [])
        if not isinstance(items, list):
            continue

        for item in items:
            if not isinstance(item, dict):
                continue

            ean = item.get("product_ean")
            if isinstance(ean, str) and ean in product_names:
                item["product_name"] = product_names[ean]

    return orders_payload


async def _enrich_single_order_with_product_name(order_payload: Any) -> Any:
    if not isinstance(order_payload, dict):
        return order_payload

    enriched_orders = await _enrich_orders_with_product_name([order_payload])
    if isinstance(enriched_orders, list) and enriched_orders:
        return enriched_orders[0]

    return order_payload


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
    include_product: bool = Query(True, alias="includeProduct"),
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

    if status_code < 400 and include_product:
        try:
            payload = await _enrich_orders_with_product_name(payload)
        except Exception:
            # Graceful degradation: list orders even if catalog enrichment fails.
            pass

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

    if status_code < 400:
        try:
            payload = await _enrich_single_order_with_product_name(payload)
        except Exception:
            # Graceful degradation: return updated order even if catalog enrichment fails.
            pass

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
