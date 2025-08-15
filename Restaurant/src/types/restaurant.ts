export interface MenuItem {
  id: string;
  name: string;
  price: number;
  category: string;
  description?: string;
  image?: string;
  available: boolean;
}

export interface OrderItem {
  menuItem: MenuItem;
  quantity: number;
  notes?: string;
}

export interface Order {
  id: string;
  type: 'dine-in' | 'takeaway';
  items: OrderItem[];
  subtotal: number;
  gst: number;
  discount: number;
  total: number;
  status: 'pending' | 'preparing' | 'ready' | 'completed';
  createdAt: Date;
  tableNumber?: string;
  customerName?: string;
  customerPhone?: string;
}

export interface Bill {
  order: Order;
  paymentMethod: 'cash' | 'card' | 'upi';
  amountPaid: number;
  change: number;
  printedAt: Date;
}

export type MenuCategory = 'starters' | 'mains' | 'desserts' | 'beverages';