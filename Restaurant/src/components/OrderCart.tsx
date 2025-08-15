import { OrderItem } from '@/types/restaurant';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Plus, Minus, Trash2, ShoppingBag, CreditCard } from 'lucide-react';

interface OrderCartProps {
  cart: OrderItem[];
  onAddToCart: (item: any) => void;
  onRemoveFromCart: (itemId: string) => void;
  onClearCart: () => void;
  onProceedToBill: () => void;
  subtotal: number;
  gst: number;
  discount: number;
  total: number;
}

const OrderCart = ({
  cart,
  onAddToCart,
  onRemoveFromCart,
  onClearCart,
  onProceedToBill,
  subtotal,
  gst,
  discount,
  total
}: OrderCartProps) => {
  const formatPrice = (price: number) => `₹${price.toFixed(2)}`;

  if (cart.length === 0) {
    return (
      <Card className="bg-gradient-steel border-border/40 shadow-steel backdrop-blur-sm">
        <CardContent className="flex flex-col items-center justify-center py-12 text-center">
          <ShoppingBag className="w-16 h-16 text-muted-foreground mb-4" />
          <CardTitle className="text-xl mb-2 text-muted-foreground">Your order is empty</CardTitle>
          <CardDescription>Add some items from our kitchen!</CardDescription>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-gradient-steel border-border/40 shadow-steel backdrop-blur-sm">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center text-xl">
            <ShoppingBag className="w-5 h-5 mr-2 text-primary" />
            Order Summary
          </CardTitle>
          <Button
            onClick={onClearCart}
            variant="outline"
            size="sm"
            className="text-destructive hover:bg-destructive hover:text-destructive-foreground"
          >
            <Trash2 className="w-4 h-4 mr-1" />
            Clear
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Cart Items */}
        <div className="space-y-3 max-h-80 overflow-y-auto">
          {cart.map((item) => (
            <div key={item.menuItem.id} className="flex items-center justify-between p-3 bg-card/60 rounded-lg border border-border/30">
              <div className="flex-1">
                <div className="font-medium text-foreground">{item.menuItem.name}</div>
                <div className="text-sm text-muted-foreground">
                  {formatPrice(item.menuItem.price)} each
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button
                  onClick={() => onRemoveFromCart(item.menuItem.id)}
                  variant="outline"
                  size="sm"
                  className="h-7 w-7 p-0 border-primary/30"
                >
                  <Minus className="w-3 h-3" />
                </Button>
                
                <Badge variant="secondary" className="min-w-[2rem] justify-center bg-primary/10 text-primary">
                  {item.quantity}
                </Badge>
                
                <Button
                  onClick={() => onAddToCart(item.menuItem)}
                  variant="outline"
                  size="sm"
                  className="h-7 w-7 p-0 border-primary/30"
                >
                  <Plus className="w-3 h-3" />
                </Button>
                
                <div className="text-right min-w-[4rem]">
                  <div className="font-semibold text-primary">
                    {formatPrice(item.menuItem.price * item.quantity)}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <Separator />

        {/* Bill Calculation */}
        <div className="space-y-2 bg-muted/30 p-4 rounded-lg">
          <div className="flex justify-between text-sm">
            <span>Subtotal:</span>
            <span>{formatPrice(subtotal)}</span>
          </div>
          
          <div className="flex justify-between text-sm">
            <span>GST (18%):</span>
            <span>{formatPrice(gst)}</span>
          </div>
          
          {discount > 0 && (
            <div className="flex justify-between text-sm text-success">
              <span>Discount:</span>
              <span>-{formatPrice(discount)}</span>
            </div>
          )}
          
          <Separator />
          
          <div className="flex justify-between font-bold text-lg">
            <span>Total:</span>
            <span className="text-primary">{formatPrice(total)}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-2 pt-2">
          <Button
            onClick={onProceedToBill}
            className="w-full bg-gradient-primary hover:shadow-glow transition-all duration-300"
            size="lg"
          >
            <CreditCard className="w-5 h-5 mr-2" />
            Proceed to Bill
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default OrderCart;