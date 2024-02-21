#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/jean/commentaires', methods=['GET'])
def admin_jean_details():
    mycursor = get_db().cursor()
    id_jean =  request.args.get('id_jean', None)
    sql = '''    requête admin_coupe_jean_1    '''
    commentaires = {}
    sql = '''   requête admin_coupe_jean_1_bis   '''
    jean = []
    return render_template('admin/jean/show_jean_commentaires.html'
                           , commentaires=commentaires
                           , jean=jean
                           )

@admin_commentaire.route('/admin/jean/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_jean = request.form.get('id_jean', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''DELETE FROM commentaire WHERE id_utilisateur = %s AND id_jean = %s AND date_publication = %s'''
    tuple_delete = (id_utilisateur, id_jean, date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/admin/jean/commentaires?id_jean=' + id_jean)



@admin_commentaire.route('/admin/jean/commentaires/repondre', methods=['POST', 'GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_jean = request.args.get('id_jean', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/jean/add_commentaire.html', id_utilisateur=id_utilisateur, id_jean=id_jean, date_publication=date_publication)

    mycursor = get_db().cursor()
    id_utilisateur_admin = session['id_user']  # Supposons que l'ID de l'administrateur est stocké dans la session sous la clé 'id_user'
    id_jean = request.form.get('id_jean', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''INSERT INTO commentaire (id_jean, id_utilisateur, date_publication, commentaire, valider) VALUES (%s, %s, %s, %s, 'oui')'''
    tuple_reponse = (id_jean, id_utilisateur_admin, date_publication, commentaire)
    mycursor.execute(sql, tuple_reponse)
    get_db().commit()
    return redirect('/admin/jean/commentaires?id_jean=' + id_jean)



@admin_commentaire.route('/admin/jean/commentaires/valider', methods=['POST', 'GET'])
def admin_comment_valider():
    id_jean = request.args.get('id_jean', None)
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''UPDATE commentaire SET valider = 'oui' WHERE id_utilisateur = %s AND id_jean = %s AND date_publication = %s'''
    tuple_valider = (id_utilisateur, id_jean, date_publication)
    mycursor.execute(sql, tuple_valider)
    get_db().commit()
    return redirect('/admin/jean/commentaires?id_jean=' + id_jean)
