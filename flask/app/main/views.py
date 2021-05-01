from . import main
from flask import render_template, redirect, url_for, request, flash
from .forms import MainForm
from app.extensions import read_csv
from .models import SAPModel


@main.route('/', methods=['GET', 'POST'])
def home_get():
    if request.method == 'GET':
        form = MainForm()
        return render_template('home.html', form=form)
    elif request.method == 'POST':
        if request.form.get('upload_submit') and request.files['upload_file'].filename:
            file = request.files['upload_file'].stream._file
            data = read_csv(file)

            SAPModel.save_sap(data)




        form = MainForm()
        return render_template('home.html', form=form)
