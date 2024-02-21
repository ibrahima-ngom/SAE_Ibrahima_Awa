#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_jean = Blueprint('admin_jean', __name__,
                          template_folder='templates')


@admin_jean.route('/admin/jean/show')
def show_jean():
    mycursor = get_db().cursor()
    sql = '''  requête admin_jean_1
    '''
    mycursor.execute(sql)
    jeans = mycursor.fetchall()
    return render_template('admin/jean/show_jean.html', jeans=jeans)


@admin_jean.route('/admin/jean/add', methods=['GET'])
def add_jean():
    mycursor = get_db().cursor()

    return render_template('admin/jean/add_jean.html'
                           #,coupe_jean=coupe_jean,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_jean.route('/admin/jean/add', methods=['POST'])
def valid_add_jean():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    coupe_jean_id = request.form.get('coupe_jean_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_jean_2 '''

    tuple_add = (nom, filename, prix, coupe_jean_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - coupe_jean:', coupe_jean_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'jean ajouté , nom:' + nom + '- type_article:' + coupe_jean_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/jean/show')


@admin_jean.route('/admin/jean/delete', methods=['GET'])
def delete_jean():
    id_jean=request.args.get('id_jean')
    mycursor = get_db().cursor()
    sql = ''' requête admin_jean_3 '''
    mycursor.execute(sql, id_jean)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_article_4 '''
        mycursor.execute(sql, id_jean)
        jean = mycursor.fetchone()
        print(jean)
        image = jean['image']

        sql = ''' requête admin_article_5  '''
        mycursor.execute(sql, id_jean)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un jean supprimé, id :", id_jean)
        message = u'un jean supprimé, id : ' + id_jean
        flash(message, 'alert-success')

    return redirect('/admin/jean/show')


@admin_jean.route('/admin/jean/edit', methods=['GET'])
def edit_jean():
    id_jean=request.args.get('id_jean')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_jean_6    
    '''
    mycursor.execute(sql, id_jean)
    jean = mycursor.fetchone()
    print(jean)
    sql = '''
    requête admin_jean_7
    '''
    mycursor.execute(sql)
    coupes_jean = mycursor.fetchall()

    # sql = '''
    # requête admin_jean_6
    # '''
    # mycursor.execute(sql, id_jean)
    # declinaisons_jean = mycursor.fetchall()

    return render_template('admin/jean/edit_jean.html'
                           ,jean=jean
                           ,coupes_jean=coupes_jean
                         #  ,declinaisons_jean=declinaisons_jean
                           )


@admin_jean.route('/admin/jean/edit', methods=['POST'])
def valid_edit_jean():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_jean = request.form.get('id_jean')
    image = request.files.get('image', '')
    coupe_jean_id = request.form.get('coupe_jean_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_jean_8
       '''
    mycursor.execute(sql, id_jean)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_jean_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, coupe_jean_id, description, id_jean))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'jean modifié , nom:' + nom + '- coupe_jean :' + coupe_jean_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/jean/show')







@admin_jean.route('/admin/jean/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    jean=[]
    commentaires = {}
    return render_template('admin/jean/show_avis.html'
                           , jean=jean
                           , commentaires=commentaires
                           )


@admin_jean.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    jean_id = request.form.get('idJean', None)
    userId = request.form.get('idUser', None)

    return admin_avis(jean_id)
