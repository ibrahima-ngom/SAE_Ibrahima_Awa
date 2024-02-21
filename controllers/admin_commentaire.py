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
    id_jean = request.args.get('id_jean', None)
    sql = '''SELECT utilisateur.id_utilisateur, utilisateur.login AS nom, commentaire.date_publication, commentaire.commentaire, commentaire.valider
             FROM commentaire
             JOIN utilisateur ON commentaire.id_utilisateur = utilisateur.id_utilisateur
             WHERE commentaire.id_jean = %s
             ORDER BY commentaire.date_publication ASC'''
    if id_jean:
        mycursor.execute(sql, (id_jean,))
        commentaires = mycursor.fetchall()
        # Récupérer les détails du jean
        sql_j = '''SELECT nom_jean FROM jean WHERE id_jean = %s'''
        mycursor.execute(sql_j, (id_jean,))
        jean = mycursor.fetchone()
        return render_template('admin/jean/show_jean_commentaires.html',
                               commentaires=commentaires,
                               jean=jean)
    else:
        # Si l'id du jean n'est pas fourni, gérer ce cas selon vos besoins
        return "ID du jean non fourni."


@admin_commentaire.route('/admin/jean/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur')
    id_jean = request.form.get('id_jean')
    date_publication = request.form.get('date_publication')

    if id_utilisateur and id_jean and date_publication:
        sql = '''DELETE FROM commentaire WHERE id_utilisateur = %s AND id_jean = %s AND date_publication = %s'''
        tuple_delete = (id_utilisateur, id_jean, date_publication)

        try:
            mycursor.execute(sql, tuple_delete)
            get_db().commit()
            return redirect('/admin/jean/commentaires?id_jean=' + id_jean)
        except Exception as e:
            # Gérer l'erreur ici (par exemple, journalisation ou affichage d'un message d'erreur)
            print(f"Erreur lors de la suppression du commentaire : {e}")
            return "Une erreur s'est produite lors de la suppression du commentaire."
    else:
        return "Paramètres manquants pour supprimer le commentaire."


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




@admin_commentaire.route('/admin/jean/commentaires/valider', methods=['POST'])
def admin_comment_valider():
    id_jean = request.form.get('id_jean', None)
    id_utilisateur = request.form.get('id_utilisateur', None)
    date_publication = request.form.get('date_publication', None)
    if id_jean is None or id_utilisateur is None or date_publication is None:
        # Gérer le cas où les paramètres requis ne sont pas fournis
        # Vous pouvez rediriger vers une page d'erreur ou renvoyer un message d'erreur
        return "Paramètres manquants", 400

    mycursor = get_db().cursor()
    sql = '''UPDATE commentaire SET valider = 'oui' WHERE id_utilisateur = %s AND id_jean = %s AND date_publication = %s'''
    tuple_valider = (id_utilisateur, id_jean, date_publication)
    mycursor.execute(sql, tuple_valider)
    get_db().commit()
    return redirect('/admin/jean/commentaires?id_jean=' + id_jean)

