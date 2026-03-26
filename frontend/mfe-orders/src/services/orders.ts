import type { CreateOrderPayload, Order, OrderStatus } from '../types/order'
import { buildUrl, getAuthHeaders, parseError } from './auth'

export interface ListOrdersParams {
  skip?: number
  limit?: number
}

export async function listOrders(params: ListOrdersParams = {}): Promise<Order[]> {
  const requestUrl = new URL(buildUrl('/api/orders/'))
  requestUrl.searchParams.set('skip', String(params.skip ?? 0))
  requestUrl.searchParams.set('limit', String(params.limit ?? 50))

  const response = await fetch(requestUrl.toString(), {
    headers: {
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<Order[]>
}

export async function createOrder(payload: CreateOrderPayload): Promise<Order> {
  const response = await fetch(buildUrl('/api/orders/'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<Order>
}

export async function updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
  const response = await fetch(buildUrl(`/api/orders/${orderId}/status`), {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ status }),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<Order>
}
