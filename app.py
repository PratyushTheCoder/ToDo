from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    pri = db.Column(db.String(50),nullable=False)
    check = db.Column(db.Boolean,nullable=True)
    date_created = db.Column(db.DateTime,default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.desc} - {self.pri}"
    

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        todo = ToDo(title=request.form['title'],desc=request.form['desc'],pri=request.form['pri'])
        db.session.add(todo)
        db.session.commit()
    return render_template('create.html')

@app.route('/manage')
def manage():
    allTodo=ToDo.query.all()
    return render_template('manage.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/manage')

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        pri = request.form['pri']
        todo.title = title
        todo.desc = desc
        todo.pri = pri
        db.session.add(todo)
        db.session.commit()
        return redirect('/manage')
    return render_template('update.html', todo=todo)


if __name__ == '__main__': 
    app.run(debug=False, port=8000)