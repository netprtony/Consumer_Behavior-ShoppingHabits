from flask import Flask, render_template,request
from pymongo import MongoClient
import pandas as pd
app = Flask(__name__)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['database']
collection = db['Sleep_Heathy']

@app.route('/')
def home():
    sort_by = request.args.get('sort_by', None)
    order = request.args.get('order', 'asc')
    bmi_category = request.args.get('bmi_category', None)
    sleep_disorder = request.args.get('sleep_disorder', None)
    
    # Lấy danh sách dữ liệu
    sleep_data_list = list(collection.find())

    # Lọc theo BMI Category nếu có
    if bmi_category:
        sleep_data_list = [data for data in sleep_data_list if data.get('BMI Category') == bmi_category]
    
    # Lọc theo Sleep Disorder nếu có
    if sleep_disorder:
        sleep_data_list = [data for data in sleep_data_list if data.get('Sleep Disorder') == sleep_disorder]

    # Nếu có trường sắp xếp, sắp xếp danh sách
    if sort_by:
        reverse = order == 'desc'
        sleep_data_list.sort(key=lambda x: x.get(sort_by), reverse=reverse)

    return render_template('sleep_list.html', sleep_data=sleep_data_list)


@app.route('/thongke')
def thongke():
    return render_template('tableau.html')

@app.route('/export_csv')
def export_csv():
    # Lấy dữ liệu từ MongoDB
    sleep_data_list = list(collection.find())
    
    # Tạo DataFrame từ dữ liệu MongoDB
    df = pd.DataFrame(sleep_data_list)
    
    # Xuất dữ liệu ra file CSV
    df.to_csv('sleep_data.csv', index=False)
    
    return "Data exported to CSV!"

if __name__ == '__main__':
    app.run(debug=True)