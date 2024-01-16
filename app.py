from flask import Flask, request, jsonify
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os
import json

app = Flask(__name__)

@app.route('/', methods=["POST"])
def index():
    input_json = request.get_json(force=True)
    print(input_json)
    resp = urlopen('http://api.bestchange.ru/info.zip')
    zipFile = ZipFile(BytesIO(resp.read()))
    zipFile.extract('bm_rates.dat')
    with open("bm_rates.dat", "r", encoding="windows-1251") as data_file:
        lst = []
        for line in data_file:
            lst.append(line.strip().split(';'))
    
    with open('valueArray.json') as f:
        value = json.load(f)
        totalDir = {}
        for item in input_json:
            idSell = 0
            idBuy = 0
            for i in value:
                if (i['key'] == item['give']):
                    idSell = i['id']
            for i in value:
                if (i['key'] == item['get']):
                    idBuy = i['id']
            strValue = []
            
            for i in lst:
                if int(i[0]) == idSell and int(i[1]) == idBuy:
                    strValue.append(i)
            for i in strValue:
                if float(i[3]) > float(i[4]):
                    sortedStrValueDown = sorted(
                    strValue, key=lambda x: (-float(x[4]), float(x[3])))
                    sortedStrValueDown = [i[3 : 5] for i in sortedStrValueDown[:5]]
                    totalDir[item["give"] + '-' + item["get"]] = sortedStrValueDown
                    break
                elif float(i[3]) < float(i[4]):
                    sortedStrValueUp = sorted(
                    strValue, key=lambda x: (-float(x[4]), float(x[3])))
                    sortedStrValueUp = [i[3 : 5] for i in sortedStrValueUp[:5]]
                    totalDir[item["give"] + '-' + item["get"]] = sortedStrValueUp
                    break
    os.remove("./bm_rates.dat")
    print(totalDir)
    return jsonify(totalDir)
    


if __name__ == "__main__":
    app.run(debug=True)
