
from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId
client = MongoClient('mongodb+srv://nur12:nur1234@cluster0.ume0s1e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client.dbfruit


app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    fruit = list(db.fruit.find({}))

    return render_template('dashboard.html',fruit=fruit)


@app.route('/fruit',methods=['GET','POST'])
def fruit():
    fruit = list(db.fruit.find({}))

    return render_template('index.html', fruit=fruit)


@app.route('/addFruit',methods=['GET','POST'])
def addfruit():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        if  nama_gambar :
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            print(nama_file_asli)
            file_path = f'static/assets/img/{nama_file_gambar}'
            nama_gambar.save(file_path)
        else :
            nama_gambar = None

        doc ={
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi,
            'gambar': nama_file_gambar
        }

        db.fruit.insert_one(doc)
        return redirect(url_for('fruit'))


    return render_template('AddFruit.html')


@app.route('/edit/<_id>',methods=['GET','POST'])
def edit(_id):
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        doc ={
            'nama ' :nama,
            'harga': harga,
            'deskripsi': deskripsi
        }
        
        if  nama_gambar :
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            print(nama_file_asli)
            file_path = f'static/assets/img/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambar'] = nama_file_gambar
            

        db.fruit.update_one({'_id': ObjectId(id)}, {'$set': doc })
        return redirect(url_for('fruit'))
    
    id = ObjectId(_id)
    data=list(db.fruit.find({'_id': id}))
    print(data)
    return render_template('EditFruit.html', data=data)

@app.route('/delete/<_id>',methods=['GET','POST'])
def delete(_id):
    db.fruit.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('fruit'))


if __name__ == '__main__':
    app.run(port=5000,debug=True)
