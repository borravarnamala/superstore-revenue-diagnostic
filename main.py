# --- IMPORTS ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors

# --- DATA LOADING & CLEANING ---
df = pd.read_csv('superstore.csv')

print("--- First 5 Rows ---")
print(df.head())

print("\n--- Data Structure ---")
df.info()

print("\n--- Missing Values ---")
print(df.isnull().sum())

# Convert dates, remove duplicates, and drop missing values so math works
df['Order Date'] = pd.to_datetime(df['Order Date'])
df = df.drop_duplicates()
df = df.dropna(subset=['Order Date', 'Sales'])

print("\n--- Data Cleaning Complete ---")
print(f"Total rows after removing duplicates and nulls: {len(df)}")


# --- FIG 1: REVENUE TRENDS ---
monthly_sales = df.set_index('Order Date').resample('ME')['Sales'].sum()

print("\n--- Monthly Sales Summary (First 5 Months) ---")
print(monthly_sales.head())

plt.figure(figsize=(10, 5))
monthly_sales.plot(kind='line', marker='o', color='red')

cursor1 = mplcursors.cursor(hover=True)

@cursor1.connect("add")
def on_add(sel):
    sel.annotation.set_text(f"Sales: ${sel.target[1]:,.0f}")


plt.title('Total Revenue Trends Over Time')
plt.xlabel('Order Date')
plt.ylabel('Total Sales ($)')
plt.grid(True)
plt.savefig("figure1_revenue_trend.png", dpi=300, bbox_inches="tight")
plt.show()


# --- FIG 2: TOP CATEGORIES ---
category_summary = df.groupby(['Category', 'Sub-Category']).agg({'Sales': 'sum', 'Profit': 'sum'})
category_summary = category_summary.sort_values(by='Sales', ascending=False)

print("\n--- Top 5 Product Sub-Categories by Sales ---")
print(category_summary.head())

plt.figure(figsize=(10, 6))
top10 = category_summary['Sales'].head(10).sort_values()
top10.plot(kind='barh', color='teal')

cursor2 = mplcursors.cursor(hover=True)

@cursor2.connect("add")
def on_add(sel):
    sel.annotation.set_text(f"Sales: ${sel.target[0]:,.0f}")

plt.title('Top 10 Product Sub-Categories by Sales')
plt.xlabel('Total Sales ($)')
plt.ylabel('Category, Sub-Category')
plt.grid(True, axis='x')
plt.tight_layout() 
plt.savefig("figure2_top_categories.png", dpi=300, bbox_inches="tight")
plt.show()


# --- FIG 3: REGIONAL PROFIT MARGIN ---
region_summary = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'})
region_summary['Profit Margin (%)'] = (region_summary['Profit'] / region_summary['Sales']) * 100

print("\n--- Regional Profit Margin Summary ---")
print(region_summary)

chart_data = region_summary[['Sales', 'Profit Margin (%)']]
chart_data.plot(kind='bar', secondary_y='Profit Margin (%)', figsize=(10,6), color=['skyblue', 'orange'])

cursor3 = mplcursors.cursor(hover=True)
@cursor3.connect("add")
def on_add(sel):
    sel.annotation.set_text(f"Value: {sel.target[1]:,.2f}")

plt.title('Gross Revenue vs. Regional Profit Margin')
plt.xlabel('Region')
plt.ylabel('Total Sales ($)')
plt.tight_layout()
plt.savefig("figure3_regional_profit.png", dpi=300, bbox_inches="tight")
plt.show()


# --- FIG 4: DISCOUNT IMPACT ---
discount_corr = df['Discount'].corr(df['Profit'])

print("\n--- Correlation Analysis ---")
print(f"Correlation between Discount and Profit: {discount_corr:.2f}")

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Discount', y='Profit', alpha=0.5, color='purple')

cursor4 = mplcursors.cursor(hover=True)
@cursor4.connect("add")
def on_add(sel):
    sel.annotation.set_text(f"Discount: {sel.target[0]*100:.0f}%\nProfit: ${sel.target[1]:,.2f}")

plt.axhline(0, color='black', linestyle='--')

plt.title('Impact of Discount on Profitability')
plt.xlabel('Discount Amount')
plt.ylabel('Profit ($)')
plt.grid(True)
plt.tight_layout()
plt.savefig("figure4_discount_profit.png", dpi=300, bbox_inches="tight")
plt.show()