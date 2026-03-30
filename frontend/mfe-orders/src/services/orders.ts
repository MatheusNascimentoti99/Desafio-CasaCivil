import type { CreateOrderPayload, Order, OrderStatus } from '../types/order'
import { buildUrl, parseError } from './auth'

export interface ListOrdersParams {
  skip?: number
  limit?: number
  status?: OrderStatus
}

export async function listOrders(params: ListOrdersParams = {}): Promise<Order[]> {
  const requestUrl = new URL(buildUrl('/orders/'))
  requestUrl.searchParams.set('skip', String(params.skip ?? 0))
  requestUrl.searchParams.set('limit', String(params.limit ?? 50))

  if (params.status) {
    requestUrl.searchParams.set('status', params.status)
  }

  const response = await fetch(requestUrl.toString(), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<Order[]>
}

export async function createOrder(payload: CreateOrderPayload): Promise<Order> {
  const response = await fetch(buildUrl('/orders/'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<Order>
}

export async function updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
  const response = await fetch(buildUrl(`/orders/${orderId}/status`), {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ status }),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<Order>
}
