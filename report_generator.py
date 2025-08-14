import sqlite3
import pandas as pd
from datetime import datetime, timedelta

class ReportGenerator:
    @staticmethod
    def generate_daily_sales_report(date=None):
        """Generate daily sales report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect('db/restaurant.db')
        query = """
        SELECT 
            o.order_id,
            o.order_date,
            o.order_type,
            o.subtotal,
            o.gst_amount,
            o.discount,
            o.total,
            o.payment_method,
            COUNT(oi.order_item_id) as item_count
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE date(o.order_date) = ?
        GROUP BY o.order_id
        """
        
        df = pd.read_sql_query(query, conn, params=(date,))
        conn.close()
        
        if not df.empty:
            summary = {
                'total_orders': len(df),
                'total_sales': df['total'].sum(),
                'average_order_value': df['total'].mean(),
                'payment_method_distribution': df['payment_method'].value_counts().to_dict(),
                'order_type_distribution': df['order_type'].value_counts().to_dict()
            }
            
            report = {
                'date': date,
                'details': df.to_dict('records'),
                'summary': summary
            }
            
            # Save to CSV
            df.to_csv(f"data/daily_sales_report_{date}.csv", index=False)
            
            return report
        return None
    
    @staticmethod
    def generate_top_items_report(days=7, limit=5):
        """Generate report of top selling items"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        conn = sqlite3.connect('db/restaurant.db')
        query = """
        SELECT 
            mi.name,
            mi.category,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * oi.price) as total_sales
        FROM order_items oi
        JOIN menu_items mi ON oi.item_id = mi.item_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE date(o.order_date) BETWEEN ? AND ?
        GROUP BY mi.item_id
        ORDER BY total_quantity DESC
        LIMIT ?
        """
        
        df = pd.read_sql_query(query, conn, params=(start_date.strftime('%Y-%m-%d'), 
                                                   end_date.strftime('%Y-%m-%d'), 
                                                   limit))
        conn.close()
        
        if not df.empty:
            # Save to CSV
            df.to_csv(f"data/top_items_report_{days}days.csv", index=False)
            
            return df.to_dict('records')
        return None