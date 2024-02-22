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
    sql = '''SELECT j.id_jean, j.nom_jean, j.coupe_jean_id, j.prix_jean, MAX(d.stock) AS stock_max, COUNT(c.id_jean) AS nb_commentaires_nouveaux, COUNT(DISTINCT d.id_declinaison_jean) AS nb_declinaisons, j.image
FROM jean j
LEFT JOIN commentaire c ON j.id_jean = c.id_jean AND c.valider = 'non'
LEFT JOIN declinaison d ON j.id_jean = d.id_jean
GROUP BY j.id_jean, j.nom_jean, j.coupe_jean_id, j.prix_jean, j.image

        '''
    mycursor.execute(sql)
    jeans = mycursor.fetchall()
    return render_template('admin/jean/show_jean.html', jeans=jeans)






@admin_jean.route('/admin/jean/add', methods=['GET'])
def add_jean():
    mycursor = get_db().cursor()

    return render_template('admin/jean/add_jean.html'
                           #,types_article=type_article,
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

    sql = ''' INSERT INTO jean (nom_jean, image, prix_jean, coupe_jean_id, description) VALUES (%s, %s, %s, %s, %s)'''

    tuple_add = (nom, filename, prix, coupe_jean_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'jean ajouté , nom: ', nom, ' - coupe_jean:', coupe_jean_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'jean ajouté , nom:' + nom + '- coupe_jean:' + coupe_jean_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/jean/show')


@admin_jean.route('/admin/jean/delete', methods=['GET'])
def delete_jean():
    id_jean = request.args.get('id_jean')
    mycursor = get_db().cursor()

    # Requête pour vérifier s'il y a des déclinaisons associées à cet article
    sql_count_declinaisons = '''SELECT COUNT(*) AS nb_declinaison FROM declinaison WHERE id_jean = %s'''
    mycursor.execute(sql_count_declinaisons, (id_jean,))
    nb_declinaison = mycursor.fetchone()

    if nb_declinaison['nb_declinaison'] > 0:
        message = u'Il y a des déclinaisons dans cet article : vous ne pouvez pas le supprimer.'
        flash(message, 'alert-warning')
    else:
        # Requête pour supprimer les commentaires associés à cet article
        sql_delete_comments = '''DELETE FROM commentaire WHERE id_jean = %s'''
        mycursor.execute(sql_delete_comments, (id_jean,))

        # Requête pour récupérer les données de l'article avant la suppression
        sql_get_jean = '''SELECT * FROM jean WHERE id_jean = %s'''
        mycursor.execute(sql_get_jean, (id_jean,))
        jean = mycursor.fetchone()
        image = jean['image']

        # Requête pour supprimer l'article lui-même
        sql_delete_jean = '''DELETE FROM jean WHERE id_jean = %s'''
        mycursor.execute(sql_delete_jean, (id_jean,))
        get_db().commit()

        # Supprimer l'image associée à l'article si elle existe
        if image is not None:
            os.remove(os.path.join('static/images/', image))

        print("Un jean a été supprimé, ID :", id_jean)
        message = u'Un jean a été supprimé, ID : ' + id_jean
        flash(message, 'alert-success')

    return redirect('/admin/jean/show')



@admin_jean.route('/admin/jean/edit', methods=['GET'])
def edit_jean():
    id_jean = request.args.get('id_jean')
    mycursor = get_db().cursor()

    # Requête pour récupérer les données de l'article à éditer
    sql_article = '''SELECT * FROM jean WHERE id_jean = %s'''
    mycursor.execute(sql_article, (id_jean,))
    jean = mycursor.fetchone()

    # Requête pour récupérer les coupes de jean disponibles
    sql_coupes_jean = '''SELECT * FROM coupe_jean'''
    mycursor.execute(sql_coupes_jean)
    coupes_jean = mycursor.fetchall()

    # Requête pour récupérer les déclinaisons de ce jean (variante)
    # sql_declinaisons_jean = '''SELECT * FROM declinaisons WHERE id_jean = %s'''
    # mycursor.execute(sql_declinaisons_jean, (id_jean,))
    # declinaisons_jean = mycursor.fetchall()

    return render_template('admin/jean/edit_jean.html',
                           jean=jean,
                           coupes_jean=coupes_jean)
                           # declinaisons_jean=declinaisons_jean)


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
