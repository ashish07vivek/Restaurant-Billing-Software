import { useState, useMemo } from 'react';
import { MenuItem, OrderItem, Order, MenuCategory } from '@/types/restaurant';
import { menuItems } from '@/data/menuData';
import RestaurantHeader from '@/components/RestaurantHeader';
import CategoryFilter from '@/components/CategoryFilter';
import MenuGrid from '@/components/MenuGrid';
import OrderCart from '@/components/OrderCart';
import OrderTypeSelector from '@/components/OrderTypeSelector';
import BillModal from '@/components/BillModal';
import { toast } from '@/hooks/use-toast';

const Index = () => {
  const [cart, setCart] = useState<OrderItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [orderType, setOrderType] = useState<'dine-in' | 'takeaway'>('dine-in');
  const [showBillModal, setShowBillModal] = useState(false);
  const [currentOrder, setCurrentOrder] = useState<Order | null>(null);

  const categories: (MenuCategory | 'all')[] = ['all', 'starters', 'mains', 'desserts', 'beverages'];

  // Calculate bill totals
  const { subtotal, gst, discount, total } = useMemo(() => {
    const subtotal = cart.reduce((sum, item) => sum + (item.menuItem.price * item.quantity), 0);
    const gst = subtotal * 0.18; // 18% GST
    const discount = 0; // No discount for now
    const total = subtotal + gst - discount;
    
    return { subtotal, gst, discount, total };
  }, [cart]);

  const addToCart = (menuItem: MenuItem) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.menuItem.id === menuItem.id);
      
      if (existingItem) {
        return prevCart.map(item =>
          item.menuItem.id === menuItem.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevCart, { menuItem, quantity: 1 }];
      }
    });

    toast({
      title: "Added to cart",
      description: `${menuItem.name} has been added to your cart.`,
    });
  };

  const removeFromCart = (menuItemId: string) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.menuItem.id === menuItemId);
      
      if (existingItem && existingItem.quantity > 1) {
        return prevCart.map(item =>
          item.menuItem.id === menuItemId
            ? { ...item, quantity: item.quantity - 1 }
            : item
        );
      } else {
        return prevCart.filter(item => item.menuItem.id !== menuItemId);
      }
    });
  };

  const clearCart = () => {
    setCart([]);
    toast({
      title: "Cart cleared",
      description: "All items have been removed from your cart.",
    });
  };

  const proceedToBill = () => {
    if (cart.length === 0) {
      toast({
        title: "Empty cart",
        description: "Please add items to your cart before proceeding.",
        variant: "destructive",
      });
      return;
    }

    const order: Order = {
      id: `ORD-${Date.now()}`,
      type: orderType,
      items: cart,
      subtotal,
      gst,
      discount,
      total,
      status: 'pending',
      createdAt: new Date(),
    };

    setCurrentOrder(order);
    setShowBillModal(true);
  };

  const handlePayment = (method: 'cash' | 'card' | 'upi') => {
    toast({
      title: "Payment processed",
      description: `Payment of ₹${total.toFixed(2)} processed via ${method.toUpperCase()}.`,
    });
    
    setShowBillModal(false);
    setCart([]);
    setCurrentOrder(null);
  };

  const handleViewCart = () => {
    // Scroll to cart section or show cart modal on mobile
    const cartElement = document.getElementById('order-cart');
    if (cartElement) {
      cartElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-kitchen font-inter">
      <RestaurantHeader 
        cartItemsCount={cart.reduce((sum, item) => sum + item.quantity, 0)}
        onViewCart={handleViewCart}
      />
      
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Category Filter */}
            <CategoryFilter
              categories={categories}
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
            />
            
            {/* Menu Grid */}
            <MenuGrid
              items={menuItems}
              cart={cart}
              onAddToCart={addToCart}
              onRemoveFromCart={removeFromCart}
              selectedCategory={selectedCategory}
            />
          </div>

          {/* Sidebar */}
          <div className="space-y-6" id="order-cart">
            {/* Order Type Selector */}
            <OrderTypeSelector
              selectedType={orderType}
              onTypeChange={setOrderType}
            />
            
            {/* Order Cart */}
            <OrderCart
              cart={cart}
              onAddToCart={addToCart}
              onRemoveFromCart={removeFromCart}
              onClearCart={clearCart}
              onProceedToBill={proceedToBill}
              subtotal={subtotal}
              gst={gst}
              discount={discount}
              total={total}
            />
          </div>
        </div>
      </div>

      {/* Bill Modal */}
      <BillModal
        isOpen={showBillModal}
        onClose={() => setShowBillModal(false)}
        order={currentOrder}
        onPayment={handlePayment}
      />
    </div>
  );
};

export default Index;
