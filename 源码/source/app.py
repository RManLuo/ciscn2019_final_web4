# coding=utf8
from flask import Flask, flash, send_file
import random
from datetime import datetime
import zipfile

# init app
app = Flask(__name__)
app.secret_key = ''.join(random.choice("il1I|") for i in range(40))
print(app.secret_key)

from flask import Response
from flask import request, session
from flask import redirect, url_for, safe_join, abort
from flask import render_template_string

from data import data

post_storage = data
site_title = "A Flask Message Board"
site_description = "Just leave what you want to say."

# %% tf/load.py
import tensorflow as tf
from tensorflow.python import pywrap_tensorflow


def init(model_path):
    '''
    This model is given by a famous hacker !
    '''
    new_sess = tf.Session()
    meta_file = model_path + ".meta"
    model = model_path
    saver = tf.train.import_meta_graph(meta_file)
    saver.restore(new_sess, model)
    return new_sess


def renew(sess, model_path):
    sess.close()
    return init(model_path)


def predict(sess, x):
    '''
    :param x: input number x
        sess: tensorflow session
    :return: b'You are: *'
    '''
    y = sess.graph.get_tensor_by_name("y:0")
    y_out = sess.run(y, {"x:0": x})
    return y_out


tf_path = "tf/detection_model/detection"
sess = init(tf_path)


# %% tf end

def check_bot(input_str):
    r = predict(sess, sum(map(ord, input_str)))
    return r if isinstance(r, str) else r.decode()


def render_template(filename, **args):
    with open(safe_join(app.template_folder, filename), encoding='utf8') as f:
        template = f.read()
    name = session.get('name', 'anonymous')[:10]
    # Someone call me to add a remembered_name function
    # But I'm just familiar with PHP !!!

    # return render_template_string(
    #     template.replace('$remembered_name', name)
    #         .replace('$site_description', site_description)
    #         .replace('$site_title', site_title), **args)
    return render_template_string(
        template.replace('$remembered_name', name), site_description=site_description, site_title=site_title, **args)


@app.route('/')
def index():
    global post_storage
    session['admin'] = session.get('admin', False)
    if len(post_storage) > 20:
        post_storage = post_storage[-20:]
    return render_template('index.html', posts=post_storage)


@app.route('/post', methods=['POST'])
def add_post():
    title = request.form.get('title', '[no title]')
    content = request.form.get('content', '[no content]')
    name = request.form.get('author', 'anonymous')[:10]
    try:
        check_result = check_bot(content)
        if not check_result.endswith('Human'):
            flash("reject because %s or hacker" % (check_result))
            return redirect('/')
        post_storage.append(
            {'title': title, 'content': content, 'author': name, 'date': datetime.now().strftime("%B %d, %Y %X")})
        session['name'] = name
    except Exception as e:
        flash('Something wrong, contact admin.')

    return redirect('/')


@app.route('/admin/model_download')
def model_download():
    '''
    Download current model.
    '''
    if session.get('admin', True):
        try:
            with zipfile.ZipFile("temp.zip", 'w') as z:
                for e in ['detection.meta', 'detection.index', 'detection.data-00000-of-00001']:
                    z.write('tf/detection_model/' + e, arcname=e)
            return send_file("temp.zip", as_attachment=True, attachment_filename='model.zip')
        except Exception as e:
            flash(str(e))
            return redirect('/admin')
    else:
        return "Not a admin **session**. <a href='/'>Back</a>"


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global site_description, site_title, sess
    if session.get('admin', False):
        print('admin session.')
        if request.method == 'POST':
            if request.form.get('site_description'):
                site_description = request.form.get('site_description')
            if request.form.get('site_title'):
                site_title = request.form.get('site_title')
            if request.files.get('modelFile'):
                file = request.files.get('modelFile')
                # print(file, type(file))
                try:
                    z = zipfile.ZipFile(file=file)
                    for e in ['detection.meta', 'detection.index', 'detection.data-00000-of-00001']:
                        open('tf/detection_model/' + e, 'wb').write(z.read(e))
                    sess = renew(sess, tf_path)
                    flash("Reloaded successfully")
                except Exception as e:
                    flash(str(e))
        return render_template('admin.html')
    else:
        return "Not a admin **session**. <a href='/'>Back</a>"


@app.route('/admin/source') # <--here ♂ boy next door
def get_source():
    return open('app.py', encoding='utf8').read()


@app.route('/admin/source_thanos')
def get_source_broken():
    '''
    Thanos is eventually resurrected,[21] and collects the Infinity Gems once again.[22]
    He uses the gems to create the Infinity Gauntlet, making himself omnipotent,
    and erases half the living things in the universe to prove his love to Death.
    '''
    t = open('app.py', encoding='utf8').read()
    tt = [t[i] for i in range(len(t))]
    ll = list(range(len(t)))
    random.shuffle(ll)
    for i in ll[:len(t) // 2]:
        if tt[i] != '\n': tt[i] = ' '
    return "".join(tt)
