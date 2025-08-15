import { Order } from '@/types/restaurant';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Receipt, Download, Printer, CreditCard, Banknote, Smartphone } from 'lucide-react';

interface BillModalProps {
  isOpen: boolean;
  onClose: () => void;
  order: Order | null;
  onPayment: (method: 'cash' | 'card' | 'upi') => void;
}

const BillModal = ({ isOpen, onClose, order, onPayment }: BillModalProps) => {
  if (!order) return null;

  const formatPrice = (price: number) => `₹${price.toFixed(2)}`;
  const formatDate = (date: Date) => {
    return date.toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const getBadgeVariant = (type: string) => {
    return type === 'dine-in' ? 'default' : 'secondary';
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center text-xl">
            <Receipt className="w-5 h-5 mr-2 text-primary" />
            Bill Summary
          </DialogTitle>
        </DialogHeader>

        <Card className="bg-gradient-steel border-border/40 shadow-steel backdrop-blur-sm">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-lg">RestaurantPOS</h3>
                <p className="text-sm text-muted-foreground">Order #{order.id.slice(-6).toUpperCase()}</p>
              </div>
              <Badge variant={getBadgeVariant(order.type)} className="capitalize">
                {order.type}
              </Badge>
            </div>
            <div className="text-xs text-muted-foreground">
              {formatDate(order.createdAt)}
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            {/* Order Items */}
            <div className="space-y-2">
              <h4 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground">Items Ordered</h4>
              {order.items.map((item, index) => (
                <div key={index} className="flex justify-between items-start py-2 border-b border-border/30 last:border-b-0">
                  <div className="flex-1">
                    <div className="font-medium text-sm">{item.menuItem.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {formatPrice(item.menuItem.price)} × {item.quantity}
                    </div>
                  </div>
                  <div className="text-sm font-semibold">
                    {formatPrice(item.menuItem.price * item.quantity)}
                  </div>
                </div>
              ))}
            </div>

            <Separator />

            {/* Bill Calculation */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Subtotal:</span>
                <span>{formatPrice(order.subtotal)}</span>
              </div>
              
              <div className="flex justify-between text-sm">
                <span>GST (18%):</span>
                <span>{formatPrice(order.gst)}</span>
              </div>
              
              {order.discount > 0 && (
                <div className="flex justify-between text-sm text-success">
                  <span>Discount:</span>
                  <span>-{formatPrice(order.discount)}</span>
                </div>
              )}
              
              <Separator />
              
              <div className="flex justify-between font-bold text-lg">
                <span>Total Amount:</span>
                <span className="text-primary">{formatPrice(order.total)}</span>
              </div>
            </div>

            {/* Payment Methods */}
            <div className="space-y-3">
              <h4 className="font-semibold text-sm uppercase tracking-wide text-muted-foreground">Payment Method</h4>
              <div className="grid grid-cols-3 gap-2">
                <Button
                  onClick={() => onPayment('cash')}
                  variant="outline"
                  className="flex-col h-16 space-y-1 hover:bg-primary/10 hover:border-primary/30"
                  size="sm"
                >
                  <Banknote className="w-5 h-5" />
                  <span className="text-xs">Cash</span>
                </Button>
                
                <Button
                  onClick={() => onPayment('card')}
                  variant="outline"
                  className="flex-col h-16 space-y-1 hover:bg-primary/10 hover:border-primary/30"
                  size="sm"
                >
                  <CreditCard className="w-5 h-5" />
                  <span className="text-xs">Card</span>
                </Button>
                
                <Button
                  onClick={() => onPayment('upi')}
                  variant="outline"
                  className="flex-col h-16 space-y-1 hover:bg-primary/10 hover:border-primary/30"
                  size="sm"
                >
                  <Smartphone className="w-5 h-5" />
                  <span className="text-xs">UPI</span>
                </Button>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2 pt-2">
              <Button variant="outline" size="sm" className="flex-1">
                <Printer className="w-4 h-4 mr-1" />
                Print
              </Button>
              <Button variant="outline" size="sm" className="flex-1">
                <Download className="w-4 h-4 mr-1" />
                Export
              </Button>
            </div>
          </CardContent>
        </Card>
      </DialogContent>
    </Dialog>
  );
};

export default BillModal;