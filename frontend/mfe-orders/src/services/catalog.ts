import type { CatalogProduct } from '../types/catalog'
import { buildUrl, parseError } from './auth'

export interface ListCatalogProductsParams {
  skip?: number
  limit?: number
}

export async function listCatalogProducts(
  params: ListCatalogProductsParams = {},
): Promise<CatalogProduct[]> {
  const requestUrl = new URL(buildUrl('/catalog/products/'))
  requestUrl.searchParams.set('skip', String(params.skip ?? 0))
  requestUrl.searchParams.set('limit', String(params.limit ?? 100))

  const response = await fetch(requestUrl.toString(), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<CatalogProduct[]>
}
