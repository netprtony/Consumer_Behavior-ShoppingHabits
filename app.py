from flask import Flask, render_template,request
from pymongo import MongoClient
import pandas as pd
app = Flask(__name__)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['admin']
collection = db['shopping_behavior']

@app.route('/')
def home():
    # sort_by = request.args.get('sort_by', None)
    # order = request.args.get('order', 'asc')
    # bmi_category = request.args.get('bmi_category', None)
    # consumer_disorder = request.args.get('consumer_disorder', None)
    
    # Lấy danh sách dữ liệu
    consumer_data_list = list(collection.find())

    # Lọc theo BMI Category nếu có
    # if bmi_category:
    #     consumer_data_list = [data for data in consumer_data_list if data.get('BMI Category') == bmi_category]
    
    # Lọc theo consumer Disorder nếu có
    # if consumer_disorder:
    #     consumer_data_list = [data for data in consumer_data_list if data.get('consumer Disorder') == consumer_disorder]

    # Nếu có trường sắp xếp, sắp xếp danh sách
    # if sort_by:
    #     reverse = order == 'desc'
    #     consumer_data_list.sort(key=lambda x: x.get(sort_by), reverse=reverse)

    return render_template('consumer_list.html', consumer_data=consumer_data_list)


@app.route('/thongke')
def thongke():
    return render_template('tableau.html')

@app.route('/export_csv')
def export_csv():
    # Lấy dữ liệu từ MongoDB
    consumer_data_list = list(collection.find())
    
    # Tạo DataFrame từ dữ liệu MongoDB
    df = pd.DataFrame(consumer_data_list)
    
    # Xuất dữ liệu ra file CSV
    df.to_csv('consumer_data.csv', index=False)
    
    return "Data exported to CSV!"

if __name__ == '__main__':
    app.run(debug=True)