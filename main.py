from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired
from send import Postman
from draw import Mixer


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'journal'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///people.db"

db = SQLAlchemy()
db.init_app(app)
info_dict = {}
mixed = []


class Person(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    groupid: Mapped[int] = mapped_column(Integer, nullable=False)


with app.app_context():
    db.create_all()


class MainForm(FlaskForm):
    date = DateField(label='When the Secret Santa meeting will be?', validators=[DataRequired()])
    place = StringField(label='Where will it be?', validators=[DataRequired()])
    max_price = IntegerField(label='What is the max price?', validators=[DataRequired()])
    add_participants = SubmitField(label='Add participants')


class SantaForm(FlaskForm):
    name = StringField('Name')
    email = StringField('E-mail address')
    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/info', methods=['GET', 'POST'])
def info():
    form = MainForm()
    if form.validate_on_submit():
        global info_dict
        info_dict = {
            "date": request.form['date'],
            "place": request.form['place'],
            "price": request.form['max_price']
        }
        return redirect(url_for('add_users'))
    return render_template("info.html", form=form)


@app.route('/add', methods=['GET', 'POST'])
def add_users():
    form = SantaForm()
    if request.method == "POST":
        names = request.form.getlist('name')
        emails = request.form.getlist('email')
        new_group_id = 1
        if Person.query.first() is not None:
            last_group_id = Person.query.order_by(Person.id.desc()).first().groupid
            new_group_id = last_group_id+1
        for i in range(len(emails)):
            new_person = Person(name=names[i],
                                email=emails[i],
                                groupid=new_group_id)
            db.session.add(new_person)
            db.session.commit()
            i += 1
        result = db.session.execute(db.select(Person).where(Person.groupid == new_group_id).order_by(Person.id))
        participants_to_pick = result.scalars().all()
        mixer = Mixer(participants_to_pick)
        global mixed
        mixed = mixer.mix_and_pick()
        return redirect(url_for('review', group_id=new_group_id))
    return render_template("add.html", form=form)


@app.route('/review', methods=['GET', 'POST'])
def review():
    global info_dict
    group_id = request.args.get('group_id')
    result = db.session.execute(db.select(Person).where(Person.groupid == group_id).order_by(Person.id))
    all_participants = result.scalars().all()
    if request.method == "POST":
        i = 0
        for participant in all_participants:
            post = Postman(
                email=participant.email,
                msg=f"Subject: Secret Santa Party!\n\n"
                    f"Ho! Ho! Ho! Hello {participant.name}!\n"
                    f"Get a present ready for {mixed[i].name}! "
                    f"The Secret Santa Party will take place in {info_dict['place']} on {info_dict['date']}."
                    f"Maximal price of the presents was set to {info_dict['price']} \n"
                    f"{request.form['message']}"
            )
            post.send_msg()
            i += 1
        return redirect(url_for('thank'))
    return render_template("review.html", info=info_dict, participants=all_participants, group_id=group_id)


@app.route('/thank', methods=['GET', 'POST'])
def thank():
    return render_template('thank.html')


if __name__ == '__main__':
    app.run(debug=True)
