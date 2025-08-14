class BillCalculator:
    @staticmethod
    def calculate_subtotal(items):
        """Calculate subtotal from order items"""
        return sum(item['price'] * item['quantity'] for item in items)
    
    @staticmethod
    def calculate_gst(subtotal, gst_percentage=5.0):
        """Calculate GST amount"""
        return round(subtotal * (gst_percentage / 100), 2)
    
    @staticmethod
    def calculate_discount(subtotal, discount_percentage=0):
        """Calculate discount amount"""
        return round(subtotal * (discount_percentage / 100), 2)
    
    @staticmethod
    def calculate_total(subtotal, gst_amount, discount_amount=0):
        """Calculate final total"""
        return round(subtotal + gst_amount - discount_amount, 2)
    
    @staticmethod
    def process_order(items, discount_percentage=0, gst_percentage=5.0):
        """Process complete order calculations"""
        subtotal = BillCalculator.calculate_subtotal(items)
        gst_amount = BillCalculator.calculate_gst(subtotal, gst_percentage)
        discount_amount = BillCalculator.calculate_discount(subtotal, discount_percentage)
        total = BillCalculator.calculate_total(subtotal, gst_amount, discount_amount)
        
        return {
            'subtotal': subtotal,
            'gst_amount': gst_amount,
            'discount_amount': discount_amount,
            'total': total,
            'items': items
        }