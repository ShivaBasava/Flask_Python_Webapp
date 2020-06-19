from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    target_at = db.Column(db.String(10), nullable=False)                         
    
    def __init__(self, name, target_at):
       self.name = name
       self.target_at = target_at
  
    def __repr__(self):
        #return '<Grocery %r>' % self.name
        return "<Grocery(name='%s', target_at='%s')>" % (self.name, self.target_at)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        name2 = request.form['name2']
        new_todo = Grocery(name=name, target_at=name2)
        
        try:
            db.session.add(new_todo)            
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new ToDo stuff."
        finally:
            db.session.close()
    else:
        ToDo_list = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('index.html', ToDo_list=ToDo_list)


@app.route('/delete/<int:id>')
def delete(id):
    ToDo_list = Grocery.query.get_or_404(id)

    try:
        db.session.delete(ToDo_list)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    update_ToDo = Grocery.query.get_or_404(id)

    if request.method == 'POST':
        update_ToDo.name = request.form['name']
        update_ToDo.target_at = request.form['name2']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating ToDo data."

    else:
        title = "Update ToDo Data"
        return render_template('update.html', title=title, ToDo=update_ToDo)

if __name__ == '__main__':
    app.run(debug=True)