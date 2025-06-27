import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns
import os

# Create charts directory if it doesn't exist
os.makedirs('charts', exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Read the CSV data
df = pd.read_csv('data/progress.csv')
df['date'] = pd.to_datetime(df['date'])

# Sort by date to ensure proper order
df = df.sort_values('date').reset_index(drop=True)

# Calculate cumulative total from daily images
df['total_images'] = df['daily_images'].cumsum()

# Chart 1: Cumulative Progress Line Chart
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['total_images'], marker='o', linewidth=2.5, markersize=4)
plt.title('Satellite Image Collection Progress', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Images Collected', fontsize=12)
plt.grid(True, alpha=0.3)

# Format x-axis dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=45)

# Add some styling
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/cumulative_progress.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: Daily Collection Rate (now using the direct daily_images column)
plt.figure(figsize=(12, 6))
plt.bar(df['date'], df['daily_images'], alpha=0.7, color='skyblue', edgecolor='navy', linewidth=0.5)
plt.title('Daily Image Collection Rate', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Images Collected Per Day', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')

# Format x-axis dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=45)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/daily_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Weekly Summary
df['week'] = df['date'].dt.isocalendar().week
weekly_summary = df.groupby('week').agg({
    'total_images': 'last',  # Take the last (highest) cumulative value for the week
    'daily_images': 'sum'    # Sum daily images for weekly total
}).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(weekly_summary['week'], weekly_summary['total_images'], marker='s', linewidth=3, markersize=8)
plt.title('Weekly Collection Milestones', fontsize=16, fontweight='bold')
plt.xlabel('Week Number', fontsize=12)
plt.ylabel('Total Images', fontsize=12)
plt.grid(True, alpha=0.3)

# Add value labels on points
for i, row in weekly_summary.iterrows():
    plt.annotate(f'{int(row["total_images"]):,}', 
                (row['week'], row['total_images']), 
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center', fontsize=10)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/weekly_summary.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Charts generated successfully!")
print(f"📊 Total images: {df['total_images'].iloc[-1]:,}")
print(f"📅 Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
print(f"📈 Average daily rate: {df['daily_images'].mean():.1f} images/day")
