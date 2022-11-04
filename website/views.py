from flask_login import login_required, current_user
from .models import Pendings, Person, Form_1, Item, Last, User, Cvs
from . import ALLOWED_EXTENSIONS, db, UPLOAD_FOLDER
from flask import render_template, request, redirect, url_for, flash, Blueprint, send_from_directory
from datetime import date
from werkzeug.utils import secure_filename
import os

# IMPORTANT
# change the path in __init__, UPLOAD_FOLDER

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    query = Person.query.join(Last, Person.id == Last.person_id)\
        .add_columns(Person.id, Person.first_name, Person.last_name, Person.uniqueID, Last.date)
    return render_template("index.html", query=query, user=current_user)


@views.route('/addperson', methods=['POST'])
@login_required
def addperson():

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        uniqueID = request.form['uniqueID']

        new_person = Person.query.filter_by(uniqueID=uniqueID).first()
        if new_person:
            flash('Person already loaded', 'error')
        else:
            new_person = Person(first_name=fname, last_name=lname, uniqueID=uniqueID)
            db.session.add(new_person)
            db.session.commit()
            person = Person.query.filter_by(uniqueID=uniqueID).first()
            # person = person.query.order_by(person.id.desc()).first()
            today = date.today()
            todaydate = today.strftime("%Y-%m-%d")
            new_last = Last(person_id=person.id, date=todaydate)
            db.session.add(new_last)
            db.session.commit()
            flash('Person Added!', 'success')
            return redirect(url_for('views.home'))
    return redirect(url_for('views.home'))


# not curretly in use
@views.route('/page_1', methods=['POST'])
@login_required
def page_1():
    if request.method == 'POST':
        person_id = person.query.order_by(person.id.desc()).first()
        person_id = person_id.id
        nacionality = request.form['nacionality']
        address = request.form['address']
        b_day = request.form['b_day']
        civil_status = request.form['civil_status']
        education = request.form['education']
        profession = request.form['profession']
        new_person_form_1 = Form_1(nationality=nationality, address=address,
                                      b_day=fecha_nac, civil_status=civil_status,
                                      education=education, profession=profession, person_id=person_id)
        db.session.add(new_person_form_1)
        db.session.commit()
        return render_template("index.html", user=current_user)



@views.route('/person/<id>', methods=['POST', 'GET'])
@login_required
def indice(id):
    person = Person.query.filter_by(id=id).first()
    page_1 = Form_1.query.filter_by(person_id=id).first()
    return render_template('person.html', person=person, page_1=page_1, user=current_user)


@views.route('/items/<id>', methods=['POST', 'GET'])
@login_required
def items(id):
    person = Person.query.filter_by(id=id).first()
    items = Item.query.filter_by(person_id=id)
    return render_template('items.html', person=person, query=items, id=id, user=current_user)


@views.route('/add_item/<id>', methods=['POST', 'GET'])
@login_required
def additem(id):
    person = Person.query.filter_by(id=id).first()
    item = Item.query.filter_by(person_id=id)
    if request.method == 'POST':
        item = request.form['items']
        assistant = request.form['assistant']
        date = request.form['date']
        new_item = Item(person_id=id, items=item, assistant=assistant, date=date)
        lastTime = Last.query.filter_by(person_id=id).first()
        if lastTime:
            update_date = Last.query.filter_by(person_id=id).update(dict(date=date))
        else:
            lastTime = Last(person_id=id, date=date)
            db.session.add(lastTime)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/items/' + str(person.id))
    return redirect(url_for('views.home'))


@views.route('/edit/<id>', methods=['POST', 'GET'])
@login_required
def get_person(id):
    # load all personl data from person
    person = Person.query.filter_by(id=id).first()
    page_1 = Form_1.query.filter_by(person_id=id).first()
    return render_template('edit.html', person=person, page_1=page_1, user=current_user)


@views.route('/update/<id>', methods=['POST'])
@login_required
def update_person(id):
    if request.method == 'POST':

        fname = request.form['name']
        lname = request.form['last_name']
        uniqueID = request.form['uniqueID']

        nationality = request.form['nationality']
        address = request.form['address']
        b_day = request.form['b_day']
        civil_status = request.form['civil_status']
        education = request.form['education']
        profession = request.form['profession']

        update_page_1 = Form_1.query.filter_by(person_id=id).first()

        if update_page_1:
            update_person = Person.query.filter_by(id=id).update(dict(first_name=fname, last_name=lname, uniqueID=uniqueID))
            person_id = id
            nationality = request.form['nationality']
            address = request.form['address']
            b_day = request.form['b_day']
            civil_status = request.form['civil_status']
            education = request.form['education']
            profession = request.form['profession']

            update_page_1 = Form_1.query.filter_by(person_id=id).update(dict(nationality=nationality,
                                                                                address=address, b_day=b_day,
                                                                                civil_status=civil_status,
                                                                                education=education,
                                                                                profession=profession))

            db.session.commit()

            flash('Actualizado!')

        else:
            update_person = Person.query.filter_by(id=id).update(dict(first_name=fname, last_name=lname, uniqueID=uniqueID))
            person_id = id
            nationality = request.form['nationality']
            address = request.form['address']
            b_day = request.form['b_day']
            civil_status = request.form['civil_status']
            education = request.form['education']
            profession = request.form['profession']


            new_person_form_1 = Form_1(nationality=nationality, address=address,
                                          b_day=b_day, civil_status=civil_status,
                                          education=education, profession=profession, person_id=person_id)


            db.session.add(new_person_form_1)
            db.session.commit()
            flash('Updated!')

        return redirect(url_for('views.home'))


@views.route('/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_person(id):
    delete = Person.query.filter_by(id=id).delete()
    page_1 = Form_1.query.filter_by(person_id=id).delete()
    item = Item.query.filter_by(person_id=id).delete()
    last = Last.query.filter_by(person_id=id).delete()
    db.session.commit()
    flash('Deleted')
    return redirect(url_for('views.home'))


@views.route('/delete/item/<item_id>', methods=['POST', 'GET'])
@login_required
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    id = item.person_id
    delete = Item.query.filter_by(id=item_id).delete()
    db.session.commit()
    flash('Deleted')
    return redirect('/items/' + str(id))


@views.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if current_user.id != 1:
        return render_template("unathorized.html")
    else:
        users = User.query.all()
        pending = Pendings.query.all()
        return render_template("admin.html", users=users, pending=pending)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/job/<id>', methods=['POST', 'GET'])
@login_required
def job(id):
    
    list = os.scandir(UPLOAD_FOLDER)
    archivos = []
    
    person = Person.query.filter_by(id=id).first()

    loaded_cvs = Cvs.query.filter_by(person_id=id)

    for archivo in list:
        archivos.append(archivo.name)


    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!')
            return redirect('/job/' + str(id))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            for index, archivo in enumerate(archivos):
                if os.path.isfile(UPLOAD_FOLDER + '/' + filename):
                    name = filename.split('.')
                    name2 = name[0]
                    name2 = name2.split('(')
                    filename = name2[0] + '(' + str(index) + ').' + name[1]     
            
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            person = Person.query.filter_by(id=id).first()
            name = filename
            today_date = date.today()
            cv = Cvs(name=name, date=today_date, person_id=id)
            db.session.add(cv)
            db.session.commit()

            return render_template('job.html', id=id, loaded=loaded_cvs, person=person)
    return render_template('job.html', id=id, loaded=loaded_cvs, person=person)


@views.route('/delete/job/<cv_id>', methods=['POST', 'GET'])
@login_required
def delete_cv(cv_id):
    cv = Cvs.query.filter_by(id=cv_id).first()
    if os.path.exists(UPLOAD_FOLDER + '/' + cv.name):
        os.remove(UPLOAD_FOLDER + '/' + cv.name)
        flash('Cv deleted!')
    else:
        flash('Cv already deleted')
    
    id = cv.person_id
    delete = Cvs.query.filter_by(id=cv_id).delete()
    db.session.commit()
    
    return redirect('/job/' + str(id))


@views.route('/download/<filename>', methods=['POST', 'GET'])
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)