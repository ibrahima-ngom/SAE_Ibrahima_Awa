#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_jean= Blueprint('admin_declinaison_jean', __name__,
                         template_folder='templates')


@admin_declinaison_jean.route('/admin/declinaison_jean/add', methods=['GET'])
def add_declinaison_jean():
    id_jean = request.args.get('id_jean')
    mycursor = get_db().cursor()

    # Récupérer les détails du jean
    sql_jean = '''SELECT * FROM jean WHERE id_jean = %s'''
    mycursor.execute(sql_jean, (id_jean,))
    jean = mycursor.fetchone()

    # Récupérer toutes les couleurs disponibles
    sql_couleurs = '''SELECT * FROM couleur'''
    mycursor.execute(sql_couleurs)
    couleurs = mycursor.fetchall()

    # Récupérer toutes les tailles disponibles
    sql_tailles = '''SELECT * FROM taille'''
    mycursor.execute(sql_tailles)
    tailles = mycursor.fetchall()

    # Récupérer une taille unique pour ce jean
    sql_taille_uniq = '''SELECT t.* FROM taille t INNER JOIN jean j ON t.id_taille = j.id_coupe_jean WHERE j.id_jean = %s'''
    mycursor.execute(sql_taille_uniq, (id_jean,))
    d_taille_uniq = mycursor.fetchone()

    # Récupérer une couleur unique pour ce jean
    sql_couleur_uniq = '''SELECT c.* FROM couleur c INNER JOIN jean j ON c.id_couleur = j.id_couleur WHERE j.id_jean = %s'''
    mycursor.execute(sql_couleur_uniq, (id_jean,))
    d_couleur_uniq = mycursor.fetchone()

    return render_template('admin/jean/add_declinaison_jean.html',
                           jean=jean,
                           couleurs=couleurs,
                           tailles=tailles,
                           d_taille_uniq=d_taille_uniq,
                           d_couleur_uniq=d_couleur_uniq)


@admin_declinaison_jean.route('/admin/declinaison_jean/add', methods=['POST'])
def valid_add_declinaison_jean():
    mycursor = get_db().cursor()

    id_jean = request.form.get('id_jean')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')

    # Vérifier si une déclinaison avec la même taille et couleur existe déjà pour ce jean
    sql_check_duplicate = '''SELECT * FROM declinaison WHERE id_jean = %s AND id_taille = %s AND id_couleur = %s'''
    mycursor.execute(sql_check_duplicate, (id_jean, taille, couleur))
    existing_declinaison = mycursor.fetchone()

    if existing_declinaison:
        flash(u'Une déclinaison avec la même taille et couleur existe déjà pour ce jean', 'alert-danger')
    else:
        # Ajouter la nouvelle déclinaison de jean
        sql_add_declinaison = '''INSERT INTO declinaison (id_jean, stock, id_taille, id_couleur) VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql_add_declinaison, (id_jean, stock, taille, couleur))
        get_db().commit()
        flash(u'Nouvelle déclinaison ajoutée avec succès pour ce jean', 'alert-success')

    return redirect('/admin/article/edit?id_jean=' + id_jean)


@admin_declinaison_jean.route('/admin/declinaison_jean/edit', methods=['GET'])
def edit_declinaison_jean():
    id_declinaison_jean = request.args.get('id_declinaison_jean')
    mycursor = get_db().cursor()

    # Récupérer les données de la déclinaison de jean
    sql_declinaison = '''SELECT * FROM declinaison WHERE id_declinaison_jean = %s'''
    mycursor.execute(sql_declinaison, (id_declinaison_jean,))
    declinaison_jean = mycursor.fetchone()

    # Récupérer toutes les couleurs disponibles
    sql_couleurs = '''SELECT * FROM couleur'''
    mycursor.execute(sql_couleurs)
    couleurs = mycursor.fetchall()

    # Récupérer toutes les tailles disponibles
    sql_tailles = '''SELECT * FROM taille'''
    mycursor.execute(sql_tailles)
    tailles = mycursor.fetchall()

    # Récupérer la taille unique de la déclinaison
    sql_taille_uniq = '''SELECT t.* FROM taille t INNER JOIN declinaison d ON t.id_taille = d.id_taille WHERE d.id_declinaison_jean = %s'''
    mycursor.execute(sql_taille_uniq, (id_declinaison_jean,))
    d_taille_uniq = mycursor.fetchone()

    # Récupérer la couleur unique de la déclinaison
    sql_couleur_uniq = '''SELECT c.* FROM couleur c INNER JOIN declinaison d ON c.id_couleur = d.id_couleur WHERE d.id_declinaison_jean = %s'''
    mycursor.execute(sql_couleur_uniq, (id_declinaison_jean,))
    d_couleur_uniq = mycursor.fetchone()

    return render_template('admin/jean/edit_declinaison_jean.html',
                           tailles=tailles,
                           couleurs=couleurs,
                           declinaison_jean=declinaison_jean,
                           d_taille_uniq=d_taille_uniq,
                           d_couleur_uniq=d_couleur_uniq)



@admin_declinaison_jean.route('/admin/declinaison_jean/edit', methods=['POST'])
def valid_edit_declinaison_jean():
    id_declinaison_jean = request.form.get('id_declinaison_jean', '')
    id_jean = request.form.get('id_jean', '')
    stock = request.form.get('stock', '')
    taille_id = request.form.get('id_taille', '')
    couleur_id = request.form.get('id_couleur', '')
    mycursor = get_db().cursor()

    sql = '''UPDATE declinaison SET stock = %s, id_taille = %s, id_couleur = %s WHERE id_declinaison_jean = %s'''
    tuple_update = (stock, taille_id, couleur_id, id_declinaison_jean)
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    message = u'Déclinaison de jean modifiée, ID : ' + str(id_declinaison_jean) + ' - Stock : ' + str(stock) + ' - Taille ID : ' + str(taille_id) + ' - Couleur ID : ' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/jean/edit?id_jean=' + str(id_jean))



@admin_declinaison_jean.route('/admin/declinaison_jean/delete', methods=['GET'])
def admin_delete_declinaison_jean():
    id_declinaison_jean = request.args.get('id_declinaison_jean', '')
    id_jean = request.args.get('id_jean', '')

    mycursor = get_db().cursor()
    sql = '''DELETE FROM declinaison WHERE id_declinaison_jean = %s'''
    mycursor.execute(sql, (id_declinaison_jean,))
    get_db().commit()

    flash(u'Déclinaison supprimée, ID déclinaison : ' + str(id_declinaison_jean), 'alert-success')
    return redirect('/admin/jean/edit?id_jean=' + str(id_jean))

