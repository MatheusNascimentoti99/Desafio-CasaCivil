import type { CreateOrderPayload, Order } from '../types/order'
import { buildUrl, getAuthHeaders, parseError } from './auth'

export async function listOrders(): Promise<Order[]> {
  const response = await fetch(buildUrl('/api/orders/'), {
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
