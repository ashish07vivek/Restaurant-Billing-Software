import { Button } from '@/components/ui/button';
import { MenuCategory } from '@/types/restaurant';

interface CategoryFilterProps {
  categories: (MenuCategory | 'all')[];
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

const CategoryFilter = ({ categories, selectedCategory, onCategoryChange }: CategoryFilterProps) => {
  const categoryLabels = {
    all: 'All Items',
    starters: 'Starters',
    mains: 'Main Course',
    desserts: 'Desserts',
    beverages: 'Beverages'
  };

  const categoryIcons = {
    all: '🍽️',
    starters: '🥗',
    mains: '🍖',
    desserts: '🍰',
    beverages: '🥤'
  };

  return (
    <div className="flex flex-wrap gap-3 p-5 bg-gradient-steel rounded-xl border border-border/30 shadow-steel backdrop-blur-sm">
      {categories.map((category) => (
        <Button
          key={category}
          onClick={() => onCategoryChange(category)}
          variant={selectedCategory === category ? "default" : "outline"}
          className={`
            transition-kitchen hover:scale-105 font-medium tracking-wide
            ${selectedCategory === category 
              ? 'bg-gradient-copper shadow-copper text-accent-foreground border-none' 
              : 'bg-card/40 hover:bg-primary/15 hover:border-primary/40 text-foreground border-border/40 backdrop-blur-sm'
            }
          `}
          size="sm"
        >
          <span className="mr-2 text-base">
            {categoryIcons[category as keyof typeof categoryIcons]}
          </span>
          <span className="font-semibold">
            {categoryLabels[category as keyof typeof categoryLabels]}
          </span>
        </Button>
      ))}
    </div>
  );
};

export default CategoryFilter;