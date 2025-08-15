import { MenuItem, OrderItem } from '@/types/restaurant';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Plus, Minus } from 'lucide-react';

interface MenuGridProps {
  items: MenuItem[];
  cart: OrderItem[];
  onAddToCart: (item: MenuItem) => void;
  onRemoveFromCart: (itemId: string) => void;
  selectedCategory: string;
}

const MenuGrid = ({ items, cart, onAddToCart, onRemoveFromCart, selectedCategory }: MenuGridProps) => {
  const filteredItems = selectedCategory === 'all' 
    ? items 
    : items.filter(item => item.category === selectedCategory);

  const getItemQuantity = (itemId: string) => {
    const cartItem = cart.find(item => item.menuItem.id === itemId);
    return cartItem ? cartItem.quantity : 0;
  };

  const formatPrice = (price: number) => {
    return `₹${price}`;
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      starters: 'bg-accent/20 text-accent border-accent/30',
      mains: 'bg-primary/20 text-primary border-primary/30',
      desserts: 'bg-destructive/20 text-destructive border-destructive/30',
      beverages: 'bg-success/20 text-success border-success/30'
    };
    return colors[category as keyof typeof colors] || 'bg-muted/20 text-muted-foreground border-muted/30';
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {filteredItems.map((item) => {
        const quantity = getItemQuantity(item.id);
        
        return (
          <Card 
            key={item.id} 
            className="group hover:shadow-copper transition-kitchen bg-gradient-steel border-border/40 hover:border-primary/30 animate-slide-up backdrop-blur-sm"
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                    {item.name}
                  </CardTitle>
                  <div className="flex items-center gap-2 mt-1">
                    <Badge variant="secondary" className={getCategoryColor(item.category)}>
                      {item.category}
                    </Badge>
                    {!item.available && (
                      <Badge variant="destructive" className="text-xs">
                        Unavailable
                      </Badge>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-primary">
                    {formatPrice(item.price)}
                  </div>
                </div>
              </div>
              {item.description && (
                <CardDescription className="text-sm text-muted-foreground leading-relaxed">
                  {item.description}
                </CardDescription>
              )}
            </CardHeader>
            
            <CardContent className="pt-0">
              {item.available ? (
                <div className="flex items-center justify-between">
                  {quantity === 0 ? (
                    <Button
                      onClick={() => onAddToCart(item)}
                      className="flex-1 bg-gradient-primary hover:shadow-glow transition-all duration-300"
                      size="sm"
                    >
                      <Plus className="w-4 h-4 mr-1" />
                      Add to Cart
                    </Button>
                  ) : (
                    <div className="flex items-center justify-between w-full">
                      <Button
                        onClick={() => onRemoveFromCart(item.id)}
                        variant="outline"
                        size="sm"
                        className="h-8 w-8 p-0 border-primary/30 hover:bg-destructive hover:text-destructive-foreground"
                      >
                        <Minus className="w-4 h-4" />
                      </Button>
                      
                      <span className="mx-3 font-semibold text-lg bg-primary/10 px-3 py-1 rounded-md text-primary">
                        {quantity}
                      </span>
                      
                      <Button
                        onClick={() => onAddToCart(item)}
                        variant="outline"
                        size="sm"
                        className="h-8 w-8 p-0 border-primary/30 hover:bg-primary hover:text-primary-foreground"
                      >
                        <Plus className="w-4 h-4" />
                      </Button>
                    </div>
                  )}
                </div>
              ) : (
                <Button disabled variant="secondary" className="w-full" size="sm">
                  Currently Unavailable
                </Button>
              )}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};

export default MenuGrid;