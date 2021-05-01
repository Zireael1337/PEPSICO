from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class MainForm(FlaskForm):
    upload_file = FileField()
    upload_submit = SubmitField(render_kw={"value": "Загрузить"})
