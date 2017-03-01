from . import source
from .forms import SourceForm, ConfigGeneralForm

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask.ext.login import current_user, login_required
from foundation.dataservice import project_impl, source_impl, configuration_impl
import requests





@source.route('/add/<pid>', methods=['GET', 'POST'])
@login_required
def add(pid):
    form = SourceForm(request.form)
    form.project.data = pid
    if request.method == 'POST' and form.validate():
        try:
            p = project_impl.get_by_id(form.project.data)

            if form.is_active.data == 'ACTIVE':
                is_active = True
            else:
                is_active = False

            s = source_impl.insert(form.name.data, form.mode.data, is_active, form.status.data,
                               current_user.username, form.project.data, p.name, form.type_spider.data)

            if s:
                source_count = p.source_count + 1
                project_impl.update(form.project.data, p.name, source_count)
                flash('INFO: ADD SOURCE SUCCESSFULL', 'info')
                return redirect(url_for('source.index'))

        except Exception as ex:
            flash('ERROR:' + ex.message, 'danger')
            return redirect(url_for('source.add', pid=pid))

    return render_template('source/add.html', form=form, pid=pid)


@source.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = SourceForm(request.form)
    form.project.choices = [(str(p.id), p.name) for p in project_impl.get_all()]
    if request.method == 'POST' and form.validate():
        try:
            p = project_impl.get_by_id(form.project.data)

            if form.is_active.data == 'ACTIVE':
                is_active = True
            else:
                is_active = False

            s = source_impl.insert(form.name.data, form.mode.data, is_active, form.status.data,
                               current_user.username, form.project.data, p.name,form.type_spider.data)
            if s:
                source_count = p.source_count + 1
                project_impl.update(form.project.data, p.name, source_count)
                flash('INFO: CREATE SOURCE SUCCESSFULL', 'info')
                return redirect(url_for('source.index'))
        except Exception as ex:
            flash('ERROR:' + ex.message, 'danger')
            return redirect(url_for('source.index'))


    if form.errors:
        flash(form.errors, 'danger')

    return render_template('source/create.html', form=form)


@source.route('/edit/<sid>', methods=['GET', 'POST'])
@login_required
def edit(sid):
    source = source_impl.get_by_id(sid)
    form = SourceForm(request.form, obj=source)


    if request.method == 'GET':
        form.project.data = source.project_id

    if source.is_active:
        form.is_active.data = 'ACTIVE'
    else:
        form.is_active.data = 'DEACTIVE'


    if request.method == 'POST' and form.validate():
        try:
            p = project_impl.get_by_id(form.project.data)
            if form.is_active.data == 'ACTIVE':
                is_active = True
            else:
                is_active = False

            s = source_impl.update(sid, form.name.data, form.mode.data, is_active, form.status.data, form.project.data, p.name, form.type_spider.data)


            if source.project_id != form.project.data:
                p = project_impl.get_by_id(source.project_id)
                source_count = p.source_count - 1
                project_impl.update(source.project_id, p.name, source_count)

                p = project_impl.get_by_id(form.project.data)
                source_count = p.source_count + 1
                project_impl.update(form.project.data, p.name, source_count)


            if s:
                flash('INFO: UPDATE SOURCE SUCCESSFULL', 'info')
                return redirect(url_for('source.index'))
        except Exception as ex:
            flash('ERROR:' + ex.message, 'danger')
            return redirect(url_for('source.index'))

    return render_template('source/edit.html', sid=sid, form=form)


@source.route('/', methods=['GET'])
@login_required
def index():
    s = source_impl.get_all()
    return render_template('source/index.html', sources=s)




@source.route('/config/general/<sid>', methods=['GET', 'POST'])
@login_required
def config_general(sid):
    c = configuration_impl.get_config('SOURCE', sid)
    form = ConfigGeneralForm(request.form)
    is_update = False

    if c: #fill data into form, data config exist
        is_update = True
        if request.method == 'GET':
            form.base_url.data = c.config['GENERALS']['base_url']
            form.thread_number.data = c.config['GENERALS']['thread_number']
            form.thread_sleep.data = c.config['GENERALS']['thread_sleep']
            form.max_trying_count.data = c.config['GENERALS']['max_trying_count']


    if request.method == 'POST' and form.validate():
        try:
            if not is_update: #insert new config
                config = dict(GENERALS=dict(
                    base_url=form.base_url.data,
                    thread_number=form.thread_number.data,
                    thread_sleep=form.thread_sleep.data,
                    max_trying_count=form.max_trying_count.data
                ))
                if configuration_impl.insert('SOURCE', sid, config):
                    flash('#INFO: INSERT CONFIG SOURCE SUCCESSFULL', 'info')
                    return redirect(url_for('source.config_general', sid=sid))
            else: #edit new config
                c.config['GENERALS'] = dict(
                    base_url=form.base_url.data,
                    thread_number=form.thread_number.data,
                    thread_sleep=form.thread_sleep.data,
                    max_trying_count=form.max_trying_count.data
                )
                if configuration_impl.update('SOURCE', sid, c.config):
                    flash('#INFO: UPDATE CONFIG SOURCE SUCCESSFULL', 'info')
                    return redirect(url_for('source.config_general', sid=sid))
        except Exception as ex:
            flash('#ERROR:' + ex.message)
            return redirect(url_for('source.config_general', sid=sid))




    return render_template('source/config/general.html', form=form, sid=sid)




@source.route('/config/link/<sid>', methods=['GET', 'POST'])
@login_required
def config_link(sid):
    return render_template('source/config/link.html', sid=sid)




from bs4 import BeautifulSoup
@source.route('/config/link', methods=['GET', 'POST'])
@login_required
def config_link_extract_url():
    try:
        url = request.form['txtBeginLink']
        item = []
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            for links in soup.find_all('a'):
                item.append(links.get('href'))
        return jsonify({'links': item})
    except Exception as ex:
        flash('#ERROR:' + ex.message)




import re
@source.route('/config/link/checkmatch', methods=['GET', 'POST'])
@login_required
def config_link_check_url_match():
    try:
        url = request.form['url']
        urlregex = request.form['urlregex']
        item = []
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href: # if not null
                    objMatch = re.match(urlregex, href, flags=0)
                    if objMatch:
                        item.append(href)
        return jsonify({'links': item})
    except Exception as ex:
        flash('#ERROR:' + str(ex))


@source.route('/config/link/list/<sid>', methods=['GET'])
@login_required
def config_link_list(sid):
    try:
        c = configuration_impl.get_config('SOURCE', sid)
        list_link_config = dict(c.config['PARSERLINKS']['data'])

        return render_template('source/config/list_link.html', sid=sid, data=list_link_config)
    except Exception as ex:
        flash('#INFO: EMPTY LINK CONFIG')
        return render_template('source/config/list_link.html', sid=sid, data=None)


import random
@source.route('/config/link/add', methods=['GET', 'POST'])
@login_required
def config_link_add():
    try:
        is_update = False
        sid = request.form['sid']
        c = configuration_impl.get_config('SOURCE', sid)

        try:
            if c and c.config['PARSERLINKS']['data']:
                is_update = True
        except:
            is_update = False

        url_pattern = request.form['url_pattern']
        pattern_type = request.form['pattern_type']
        link_type = request.form['link_type']

        #key_number = len(c.config['PARSERLINKS']['data']) + 1
        key_number = random.randrange(100, 1000, 3)


        if is_update:
            c.config['PARSERLINKS']['data'][str(key_number)] = dict(
                    url_pattern=url_pattern,
                    pattern_type=pattern_type,
                    link_type=link_type
                )
            if configuration_impl.update('SOURCE', sid, c.config):
                return jsonify({'status': 1, 'message': 'Save Config Link Successfull'})
        else:
            c.config[u'PARSERLINKS'] = dict(
                    data={str(key_number): dict(
                        url_pattern=url_pattern,
                        pattern_type=pattern_type,
                        link_type=link_type
                    )}
                )
            if configuration_impl.update('SOURCE', sid, c.config):
                return jsonify({'status': 1, 'message': 'Save Config Link Successfull'})
    except Exception as ex:
        return jsonify({'status': -1, 'message': ex.message})


@source.route('/config/link/remove', methods=['GET', 'POST'])
@login_required
def config_link_remove():
    try:
        sid = request.form['sid']
        ckey = request.form['cid']
        c = configuration_impl.get_config('SOURCE', sid)
        try:
            if c.config['PARSERLINKS']['data'][ckey]:
                del c.config['PARSERLINKS']['data'][ckey]
                if configuration_impl.update('SOURCE', sid, c.config):
                    return jsonify({'status': 1, 'message': 'Remove Config Link Successfull'})
        except Exception as error:
            return jsonify({'status': -1, 'message': error.message})
    except Exception as ex:
        return jsonify({'status': -1, 'message': ex.message})



@source.route('/config/request/get/html', methods=['GET', 'POST'])
@login_required
def config_request_get_html():
    try:
        url = request.form['txtBeginLink']
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify({'html': response.text})
    except Exception as ex:
        flash('#ERROR:' + ex.message)


@source.route('/config/parser/<sid>', methods=['GET', 'POST'])
@login_required
def config_parser(sid):
    return render_template('source/config/parser.html', sid=sid)


@source.route('/config/field/add', methods=['GET', 'POST'])
@login_required
def config_field_add():
    try:
        is_update = False
        sid = request.form['sid']
        c = configuration_impl.get_config('SOURCE', sid)

        field_name = request.form['field_name']
        start_pattern = request.form['start_pattern']
        end_pattern = request.form['end_pattern']

        try:
            if c and c.config['PARSERFIELDS']['data'][field_name]:
                is_update = True
        except:
            is_update = False



        if is_update:
            key_number = len(c.config['PARSERFIELDS']['data'][field_name]['step']) + 1
            c.config['PARSERFIELDS']['data'][field_name]['pattern_type'] = u'STRING_BETWEEN'
            c.config['PARSERFIELDS']['data'][field_name]['step'][str(key_number)] = dict(
                    start_pattern=start_pattern,
                    end_pattern=end_pattern
                )
            if configuration_impl.update('SOURCE', sid, c.config):
                return jsonify({'status': 1, 'message': 'Save Config Field Successfull'})
        else:

            c.config[u'PARSERFIELDS'] = dict(
                data={str(field_name): dict(pattern_type=u'STRING_BETWEEN',
                                     step={u'1': dict(start_pattern=str(start_pattern),
                                                      end_pattern=str(end_pattern))}
                                     )})
            if configuration_impl.update('SOURCE', sid, c.config):
                return jsonify({'status': 1, 'message': 'Save Config Field Successfull'})
    except Exception as ex:
        return jsonify({'status': -1, 'message': ex.message})


@source.route('/config/field/list/<sid>', methods=['GET'])
@login_required
def config_field_list(sid):
    try:
        c = configuration_impl.get_config('SOURCE', sid)
        list_field_config = c.config['PARSERFIELDS']['data']
        return render_template('source/config/list_field.html', sid=sid, data=list_field_config)
    except Exception as ex:
        flash('#INFO: EMPTY LINK CONFIG')
        return render_template('source/config/list_field.html', sid=sid, data=None)



@source.route('/config/field/remove', methods=['GET', 'POST'])
@login_required
def config_field_remove():
    try:
        sid = request.form['sid']
        ckey = request.form['cid']
        c = configuration_impl.get_config('SOURCE', sid)
        try:
            if c.config['PARSERFIELDS']['data'][ckey]:
                del c.config['PARSERFIELDS']['data'][ckey]
                if configuration_impl.update('SOURCE', sid, c.config):
                    return jsonify({'status': 1, 'message': 'Remove Config Field Successfull'})
        except Exception as error:
            return jsonify({'status': -1, 'message': error.message})
    except Exception as ex:
        return jsonify({'status': -1, 'message': ex.message})