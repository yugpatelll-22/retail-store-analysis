import pandas as pd
import numpy as np

def generate_inventory_data():
    print("Loading cleaned_retail_data.csv...")
    # Load the cleaned retail data
    df = pd.read_csv(r'C:\Users\yugpa\OneDrive\Computer\Desktop (1)\retail\data_cleaning\data\cleaned_retail_data.csv')

    # Ensure InvoiceDate is a datetime object
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Calculate total days the store has been active to find daily averages
    date_min = df['InvoiceDate'].min()
    date_max = df['InvoiceDate'].max()
    days_active = (date_max - date_min).days
    if days_active == 0: 
        days_active = 1

    print("Aggregating sales data per product...")
    # Aggregate data per product
    inventory_df = df.groupby('Description').agg(
        Total_Sold=('Quantity', 'sum')
    ).reset_index()

    # Rename to ProductName to match the dashboard's requirements
    inventory_df.rename(columns={'Description': 'ProductName'}, inplace=True)

    # Filter out returned/negative items to keep the inventory clean
    inventory_df = inventory_df[inventory_df['Total_Sold'] > 0].copy()

    # Calculate Average Daily Demand
    inventory_df['Avg_Daily_Demand'] = inventory_df['Total_Sold'] / days_active

    # ==========================================
    # INVENTORY MATH (Lead Time & Safety Stock)
    # ==========================================
    # Assume a standard supplier lead time of 7 days
    lead_time = 7

    # Safety Stock Formula: (Max Daily Sales x Max Lead Time) - (Avg Daily Sales x Avg Lead Time)
    # For simplicity and robust dashboard numbers, we will use a 1.5x safety multiplier
    inventory_df['SafetyStock'] = np.ceil(inventory_df['Avg_Daily_Demand'] * lead_time * 1.5)

    # Reorder Point Formula: (Avg Daily Demand * Lead Time) + Safety Stock
    inventory_df['ReorderPoint'] = np.ceil((inventory_df['Avg_Daily_Demand'] * lead_time) + inventory_df['SafetyStock'])

    # ==========================================
    # SIMULATE REALISTIC CURRENT STOCK LEVELS
    # ==========================================
    print("Simulating current stock distributions...")
    np.random.seed(42)
    
    # 70% of products are Healthy, 20% need Restock, 10% are Overstocked
    conditions = np.random.choice(['healthy', 'restock', 'overstock'], size=len(inventory_df), p=[0.7, 0.2, 0.1])

    def simulate_stock(row, condition):
        rop = row['ReorderPoint']
        if rop < 5: 
            rop = 10 # Baseline minimum for slow-moving items
        
        if condition == 'restock':
            # Current stock is critically below the Reorder Point
            return np.random.randint(0, int(rop) + 1)
        elif condition == 'healthy':
            # Current stock is safely above the Reorder Point but not excessive
            return np.random.randint(int(rop) + 1, int(rop) * 3 + 1)
        else: 
            # Overstock: Current stock is way too high (>3x Reorder Point)
            return np.random.randint(int(rop) * 3 + 1, int(rop) * 5 + 1)

    # Apply the simulation
    inventory_df['CurrentStock'] = [simulate_stock(row, cond) for row, cond in zip(inventory_df.to_dict('records'), conditions)]

    # Finalize columns for the dashboard
    final_inventory = inventory_df[['ProductName', 'CurrentStock', 'ReorderPoint', 'SafetyStock', 'Avg_Daily_Demand']]

    # Export to CSV
    output_filename = r'C:\Users\yugpa\OneDrive\Computer\Desktop (1)\retail\data\inventory_recommendations_new.csv'
    final_inventory.to_csv(output_filename, index=False)
    
    print(f"✅ Success! Generated {len(final_inventory)} inventory records.")
    print(f"💾 Saved as: {output_filename}")

if __name__ == "__main__":
    generate_inventory_data()