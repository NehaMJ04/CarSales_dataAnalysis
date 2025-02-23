from flask import Flask, jsonify, render_template
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

app = Flask(__name__)

# Load the data
car_details = pd.read_csv('car_details_df.csv')
price_cardetails = pd.read_csv('price_cardetails_df.csv')
merged_df = pd.merge(car_details, price_cardetails, on='Car_ID', how='inner')

# Helper function to convert plot to base64
def plot_to_base64(plt):
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis1')
def analysis1():
    # 1. Most common car brands
    top_brands = car_details['Brand'].value_counts().head(5).to_dict()
    return jsonify(top_brands)

@app.route('/analysis2')
def analysis2():
    # 2. Brand and its models
    brand_model_df = car_details.groupby("Brand")["Model"].unique().reset_index()
    result = {row['Brand']: row['Model'].tolist() for _, row in brand_model_df.iterrows()}
    return jsonify(result)

@app.route('/analysis3')
def analysis3():
    # 3. Brand and its Transmission Types
    brand_transmission_df = car_details.groupby("Brand")["Transmission"].unique().reset_index()
    result = {row['Brand']: row['Transmission'].tolist() for _, row in brand_transmission_df.iterrows()}
    return jsonify(result)

@app.route('/analysis4')
def analysis4():
    # 4. Most popular brand in each location
    popular_brands_by_location = car_details.groupby(["Location", "Brand"]).size().reset_index(name="Count")
    popular_brands = popular_brands_by_location.loc[popular_brands_by_location.groupby("Location")["Count"].idxmax()]
    result = popular_brands.to_dict(orient='records')
    return jsonify(result)

@app.route('/analysis5')
def analysis5():
    # 5. Average mileage per fuel type
    avg_mileage = car_details.groupby('Fuel_Type')['Mileage_km'].mean().to_dict()
    return jsonify(avg_mileage)

@app.route('/analysis6')
def analysis6():
    # 6. Basic Statistical Summary
    price_summary = price_cardetails.describe().to_dict()
    car_summary = car_details.describe().to_dict()
    return jsonify({"price_summary": price_summary, "car_summary": car_summary})

@app.route('/analysis7')
def analysis7():
    # 7. Most common transmission type in recent years
    recent_transmission = car_details[car_details['Year'] >= 2020]['Transmission'].value_counts().to_dict()
    return jsonify(recent_transmission)

@app.route('/analysis8')
def analysis8():
    # 8. Location with most cars listed
    top_locations = car_details['Location'].value_counts().head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_locations.index, y=top_locations.values, hue=top_locations.index, palette='cividis')
    plt.title('Top 10 Locations with Most Cars Listed')
    plt.xlabel('Location')
    plt.ylabel('Count')
    plt.ylim(4300, max(top_locations.values) + 10)
    plt.xticks(rotation=45)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img})

@app.route('/analysis9')
def analysis9():
    # 9. Count of Cars by Fuel Type
    fuel_counts = merged_df["Fuel_Type"].value_counts().to_dict()
    return jsonify(fuel_counts)

@app.route('/analysis10')
def analysis10():
    # 10. Common price range for each car model
    price_range = merged_df.groupby("Model")["Price_USD"].describe().to_dict()
    return jsonify(price_range)

@app.route('/analysis11')
def analysis11():
    # 11. Most expensive car models
    expensive_models = merged_df.groupby("Model")["Price_USD"].mean().sort_values(ascending=False).head(10).to_dict()
    return jsonify(expensive_models)

@app.route('/analysis12')
def analysis12():
    # 12. Correlation between car age and price
    merged_df["car_Age"] = 2024 - merged_df["Year"]
    correlation = merged_df[["car_Age", "Price_USD"]].corr().to_dict()
    return jsonify(correlation)

@app.route('/analysis13')
def analysis13():
    # 13. Average price of automatic vs manual cars
    avg_price = merged_df.groupby("Transmission")["Price_USD"].mean().to_dict()
    return jsonify(avg_price)

@app.route('/analysis14')
def analysis14():
    # 14. Top 5 brands with highest resale values
    resale_values = merged_df.groupby("Brand")["Price_USD"].median().sort_values(ascending=False).head(5).to_dict()
    return jsonify(resale_values)

@app.route('/analysis15')
def analysis15():
    # 15. Engine size vs average price
    eng = merged_df.groupby("Engine_cc")["Price_USD"].mean()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=eng.index, y=eng.values, palette='cividis', hue=eng.index, legend=False)
    plt.title("Engine Size vs. Average Price")
    plt.xlabel("Engine Size (cc)")
    plt.ylabel("Average Price (USD)")
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img})

@app.route('/analysis16')
def analysis16():
    # 16. Average Resale Value by Fuel Type
    resale_values = merged_df.groupby("Fuel_Type")["Price_USD"].median().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=resale_values.index, y=resale_values.values, palette="cividis", hue=resale_values.index, legend=False)
    plt.title("Average Resale Value by Fuel Type")
    plt.xlabel("Fuel Type")
    plt.ylabel("Median Resale Price (USD)")
    plt.xticks(rotation=45)
    plt.ylim(76500, max(resale_values.values) + 200)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img})

@app.route('/analysis17')
def analysis17():
    # 17. Average price by Car Brand
    price_by_brand = merged_df.groupby("Brand")["Price_USD"].mean().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=price_by_brand.index, y=price_by_brand.values, palette="cividis", hue=price_by_brand.index, legend=False)
    plt.title("Average Price by Car Brand")
    plt.xlabel("Car Brand")
    plt.ylabel("Average Price (USD)")
    plt.xticks(rotation=45)
    plt.ylim(76500, max(price_by_brand.values) + 200)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img})

@app.route('/analysis18')
def analysis18():
    # 18. Transmission Type vs Number of Cars
    transmission_counts = merged_df["Transmission"].value_counts().reset_index()
    transmission_counts.columns = ["Transmission Type", "Number of Cars"]
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Transmission Type", y="Number of Cars", data=transmission_counts, palette="cividis", hue="Transmission Type", legend=False)
    plt.title("Count of Cars Based on Transmission Type")
    plt.xlabel("Transmission Type")
    plt.ylabel("Number of Cars")
    plt.ylim(34000, transmission_counts["Number of Cars"].max() + 200)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img})

@app.route('/analysis19')
def analysis19():
    # 19. Depreciation: Average Price of Cars by Age
    merged_df["Car_Age"] = 2024 - merged_df["Year"]
    avg_price_by_age = merged_df.groupby("Car_Age")["Price_USD"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Car_Age", y="Price_USD", data=avg_price_by_age, palette="cividis", hue="Car_Age", legend=False)
    plt.title("Depreciation: Average Price of Cars by Age")
    plt.xlabel("Car Age (Years)")
    plt.ylabel("Average Price (USD)")
    plt.xticks(rotation=45)
    plt.ylim(74000, avg_price_by_age["Price_USD"].max() + 5000)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img})

@app.route('/analysis20')
def analysis20():
    # 20. Car Brands with the Best Mileage-to-Price Ratio
    merged_df["Mileage_to_Price"] = merged_df["Mileage_km"] / merged_df["Price_USD"].replace(0, 1)
    brand_mileage_price_ratio = merged_df.groupby("Brand")["Mileage_to_Price"].mean().reset_index()
    brand_mileage_price_ratio = brand_mileage_price_ratio.sort_values(by="Mileage_to_Price", ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Brand", y="Mileage_to_Price", data=brand_mileage_price_ratio, palette="cividis", hue="Brand", legend=False)
    plt.title("Car Brands with the Best Mileage-to-Price Ratio")
    plt.xlabel("Car Brand")
    plt.ylabel("Mileage per Unit Price")
    plt.xticks(rotation=45)
    plt.ylim(3.5, brand_mileage_price_ratio["Mileage_to_Price"].max() + 0.01)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img, "data": brand_mileage_price_ratio.to_dict(orient='records')})

@app.route('/analysis21')
def analysis21():
    # 21. Number of cars sold each year
    yearly_sales = car_details["Year"].value_counts().reset_index()
    yearly_sales.columns = ["Year", "Number of Listings"]
    yearly_sales = yearly_sales.sort_values("Year")
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Year", y="Number of Listings", data=yearly_sales, palette="cividis", hue="Year", legend=False)
    plt.title("Number of Cars Sold Each Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Listings")
    plt.xticks(rotation=45)
    plt.ylim(3400, max(yearly_sales["Number of Listings"]) + 50)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img, "data": yearly_sales.to_dict(orient='records')})

@app.route('/analysis22')
def analysis22():
    # 22. Price Trends Over Years
    merged_df["Car_Age"] = 2024 - merged_df["Year"]
    age_price = merged_df.groupby("Car_Age")["Price_USD"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x="Car_Age", y="Price_USD", data=age_price, marker="o", color="green")
    plt.title("Depreciation: Average Price of Cars by Age")
    plt.xlabel("Car Age (Years)")
    plt.ylabel("Average Price (USD)")
    plt.grid(True)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img, "data": age_price.to_dict(orient='records')})

@app.route('/analysis23')
def analysis23():
    # 23. EV in each location
    ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
    ev_by_state = ev_cars["Location"].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(ev_by_state, labels=ev_by_state.index, autopct='%1.1f%%', colors=sns.color_palette("colorblind"))
    plt.title("EV Vehicles Distribution by State")
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img, "data": ev_by_state.to_dict()})

@app.route('/analysis24')
def analysis24():
    # 24. Transmission type in each location
    transmission_by_location = car_details.groupby(["Location", "Transmission"]).size().reset_index(name="Count")
    plt.figure(figsize=(14, 6))
    sns.barplot(x="Location", y="Count", hue="Transmission", data=transmission_by_location, palette="cividis")
    plt.title("Transmission Types in Each Location")
    plt.xlabel("Location")
    plt.ylabel("Number of Cars")
    plt.xticks(rotation=45)
    plt.ylim(400, transmission_by_location["Count"].max() + 100)
    plt.legend(title="Transmission Type")
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img, "data": transmission_by_location.to_dict(orient='records')})

@app.route('/analysis25')
def analysis25():
    # 25. EV listing by year
    ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
    ev_by_year = ev_cars["Year"].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=ev_by_year.index, y=ev_by_year.values, palette="cividis", hue=ev_by_year.index, legend=False)
    plt.title("Electric Vehicles (EV) Listings by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of EV Listings")
    plt.xticks(rotation=45)
    plt.ylim(300, ev_by_year.max() + 50)
    img = plot_to_base64(plt)
    plt.close()
    return jsonify({"image": img, "data": ev_by_year.to_dict()})

if __name__ == '__main__':
    app.run(debug=True)
