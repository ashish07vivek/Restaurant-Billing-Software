import { Button } from '@/components/ui/button';
import { ShoppingCart, ChefHat, Clock, Flame } from 'lucide-react';

interface RestaurantHeaderProps {
  cartItemsCount: number;
  onViewCart: () => void;
}

const RestaurantHeader = ({ cartItemsCount, onViewCart }: RestaurantHeaderProps) => {
  return (
    <header className="bg-gradient-kitchen border-b border-border/30 shadow-steel sticky top-0 z-50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="w-12 h-12 bg-gradient-copper rounded-lg flex items-center justify-center shadow-copper">
                <ChefHat className="w-7 h-7 text-accent-foreground" />
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-primary rounded-full flex items-center justify-center">
                <Flame className="w-2.5 h-2.5 text-primary-foreground" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold font-inter tracking-tight text-foreground">
                The <span className="text-primary">Bear</span> POS
              </h1>
              <p className="text-muted-foreground text-sm font-medium tracking-wide">
                PROFESSIONAL KITCHEN SYSTEM
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-3 bg-card/50 backdrop-blur-sm px-4 py-2 rounded-lg border border-border/30">
              <Clock className="w-4 h-4 text-accent" />
              <span className="text-sm font-medium text-foreground">
                {new Date().toLocaleTimeString('en-US', {
                  hour12: true,
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
            </div>
            
            <Button
              onClick={onViewCart}
              variant="outline"
              className="relative bg-card/30 backdrop-blur-sm hover:bg-primary/20 text-foreground border-border/50 hover:border-primary/50 transition-kitchen font-medium"
            >
              <ShoppingCart className="w-4 h-4 mr-2" />
              Orders
              {cartItemsCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-primary text-primary-foreground text-xs rounded-full w-5 h-5 flex items-center justify-center animate-pulse-glow font-bold">
                  {cartItemsCount}
                </span>
              )}
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default RestaurantHeader;