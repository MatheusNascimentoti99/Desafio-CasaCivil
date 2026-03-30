import type { CatalogProduct, CatalogProductPayload } from '../types/catalog'
import { buildUrl, parseError } from './auth'

export async function listCatalogProducts(): Promise<CatalogProduct[]> {
  const response = await fetch(buildUrl('/catalog/products/'), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<CatalogProduct[]>
}

export async function createCatalogProduct(payload: CatalogProductPayload): Promise<CatalogProduct> {
  const response = await fetch(buildUrl('/catalog/products/'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<CatalogProduct>
}

export async function updateCatalogProduct(ean: string, payload: CatalogProductPayload): Promise<CatalogProduct> {
  const response = await fetch(buildUrl(`/catalog/products/${ean}`), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<CatalogProduct>
}

export async function deleteCatalogProduct(ean: string): Promise<void> {
  const response = await fetch(buildUrl(`/catalog/products/${ean}`), {
    method: 'DELETE',
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }
}
