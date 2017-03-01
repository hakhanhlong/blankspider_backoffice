from . import project
from .forms import AddForm, EditForm

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, current_user
from foundation.dataservice import project_impl

@project.route('/', methods=['GET'])
@login_required
def index():
    projects = project_impl.get_all()
    return render_template('project/index.html', projects=projects)

@project.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        try:
            project_impl.insert(form.name.data, current_user.username)
            flash('Create new project successful!', 'info')
            return redirect(url_for('project.index'))
        except Exception as ex:
            flash('ERROR:' + ex.message)
            return render_template('project/add.html', form=form)

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('project/add.html', form=form)

@project.route('/edit/<pid>', methods=['GET', 'POST'])
@login_required
def edit(pid):
    p = project_impl.get_by_id(pid)
    form = EditForm(request.form, obj = p)
    if request.method == 'POST' and form.validate():
        try:
            project_impl.update(pid, form.name.data, p.source_count)
            flash('UPDATE SECCESSFULL!')
            return redirect(url_for('project.edit', pid=pid))
        except Exception as ex:
            flash('ERROR:' + ex.message)
            return render_template('project/edit.html', form=form,  project=p)


    if form.errors:
        flash(form.errors, 'danger')

    return render_template('project/edit.html', form=form, project=p)

