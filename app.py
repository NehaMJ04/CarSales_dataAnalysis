from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (needed for Flutter)

# Load datasets only once when the app starts
car_details = pd.read_csv("car_details_df.csv")
price_cardetails = pd.read_csv("price_cardetails_df.csv")

# Precompute summaries so they don’t get recalculated on every request
summary1 = car_details.describe().to_dict()
summary2 = price_cardetails.describe().to_dict()

@app.route('/analysis', methods=['GET'])
def get_analysis():
    return jsonify({
        "car_details_summary": summary1,
        "price_details_summary": summary2
    })  # Send processed data as JSON

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    app.run(host='0.0.0.0', port=port)  # Run on 0.0.0.0 for external access
