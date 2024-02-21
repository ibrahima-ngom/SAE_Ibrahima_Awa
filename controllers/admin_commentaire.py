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
    sql = '''    requête admin_coupe_jean_2   '''
    tuple_delete=(id_utilisateur, id_jean, date_publication)
    get_db().commit()
    return redirect('/admin/jean/commentaires?id_jean='+id_jean)


@admin_commentaire.route('/admin/jean/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_jean = request.args.get('id_jean', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/jean/add_commentaire.html', id_utilisateur=id_utilisateur, id_jean=id_jean, date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_jean = request.form.get('id_jean', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_coupe_jean_3   '''
    get_db().commit()
    return redirect('/admin/jean/commentaires?id_jean='+id_jean)


@admin_commentaire.route('/admin/jean/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_jean = request.args.get('id_jean', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_coupe_jean_4   '''
    get_db().commit()
    return redirect('/admin/article/commentaires?id_jean='+id_jean)