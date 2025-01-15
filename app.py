from flask import Flask, render_template, request,redirect, url_for, session,flash
from flask_mysqldb import MySQL, MySQLdb
import werkzeug


app = Flask(__name__)
app.secret_key= 'membuatlogin'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mencobamysql'
app.config['MYSQL_DB'] = 'kereta'
mysql= MySQL(app)


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM masuk WHERE email = %s and password = %s",(email,password,))
        user = curl.fetchone()
        curl.close()

        if user is not None and len(user) > 0 :
                session['name'] = user ['name']
                session['email'] = user['email']
                return redirect(url_for('home'))
        else :
            flash("Gagal, User Tidak Ditemukan")
            return redirect(url_for('login'))
    else: 
        return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else :
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO masuk (name,email,password) VALUES (%s,%s,%s)" ,(name, email, password)) 
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route('/package', methods = ['GET', 'POST'])
def package():
    return render_template('package.html')

@app.route('/book', methods = ['GET', 'POST'])
def book():
    # Contoh mengambil data dari database
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        username = request.values.get('namapemesan')
        notelepon = request.values.get('notelepon')
        email = request.values.get('email')
        alamat = request.values.get('alamat')
        tujuan = request.values.get('tujuan')
        orang = request.values.get('orang')
        tanggal = request.values.get('tanggal_perjalanan')
        cursor.execute ('INSERT INTO data_pemesan (namapemesan,notelepon,email,alamat,tujuan,orang,tanggal_perjalanan) VALUES(%s,%s,%s,%s,%s,%s,%s)',(username,notelepon,email,alamat,tujuan,orang,tanggal))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM data_pemesan")
        data = cursor.fetchall()
        cursor.close()
        
        return render_template('tabel.html',data = data)
    else:
        return render_template('book.html')




if __name__ == '__main__':
    app.run(debug=True)
