export interface CatalogProduct {
  ean: string
  name: string
  unit_price: number
  created_at?: string
  updated_at?: string
}

export interface CatalogProductPayload {
  ean: string
  name: string
  unit_price: number
}
