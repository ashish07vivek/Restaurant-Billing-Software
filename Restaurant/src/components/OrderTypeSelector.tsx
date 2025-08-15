import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { UtensilsCrossed, Package } from 'lucide-react';

interface OrderTypeSelectorProps {
  selectedType: 'dine-in' | 'takeaway';
  onTypeChange: (type: 'dine-in' | 'takeaway') => void;
}

const OrderTypeSelector = ({ selectedType, onTypeChange }: OrderTypeSelectorProps) => {
  return (
    <Card className="bg-gradient-steel border-border/40 shadow-steel backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="text-center text-lg">Order Type</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3">
          <Button
            onClick={() => onTypeChange('dine-in')}
            variant={selectedType === 'dine-in' ? 'default' : 'outline'}
            className={`
              h-20 flex-col space-y-2 transition-all duration-300
              ${selectedType === 'dine-in' 
                ? 'bg-gradient-primary shadow-warm text-primary-foreground' 
                : 'bg-card/80 hover:bg-primary/10 hover:border-primary/30'
              }
            `}
          >
            <UtensilsCrossed className="w-6 h-6" />
            <span className="text-sm font-medium">Dine-In</span>
          </Button>
          
          <Button
            onClick={() => onTypeChange('takeaway')}
            variant={selectedType === 'takeaway' ? 'default' : 'outline'}
            className={`
              h-20 flex-col space-y-2 transition-all duration-300
              ${selectedType === 'takeaway' 
                ? 'bg-gradient-primary shadow-warm text-primary-foreground' 
                : 'bg-card/80 hover:bg-primary/10 hover:border-primary/30'
              }
            `}
          >
            <Package className="w-6 h-6" />
            <span className="text-sm font-medium">Takeaway</span>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default OrderTypeSelector;