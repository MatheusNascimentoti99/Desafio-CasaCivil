export type OrderStatus = 'pendente' | 'confirmado' | 'enviado' | 'entregue' | 'cancelado'

export interface OrderItem {
  id?: string
  product_name: string
  quantity: number
  unit_price: number
}

export interface Order {
  id: string
  customer_name: string
  status: OrderStatus
  total?: number
  user_id?: string
  items: OrderItem[]
  created_at?: string
  updated_at?: string
}

export interface UpdateOrderStatusPayload {
  status: OrderStatus
}

export interface CreateOrderPayload {
  customer_name: string
  items: Array<{
    product_name: string
    quantity: number
    unit_price: number
  }>
}
