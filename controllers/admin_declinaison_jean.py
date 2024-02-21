#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_jean= Blueprint('admin_declinaison_jean', __name__,
                         template_folder='templates')


@admin_declinaison_jean.route('/admin/declinaison_jean/add')
def add_declinaison_jean():
    id_article=request.args.get('id_jean')
    mycursor = get_db().cursor()
    jean=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/jean/add_declinaison_jean.html'
                           , jean=jean
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_jean.route('/admin/declinaison_jean/add', methods=['POST'])
def valid_add_declinaison_jean():
    mycursor = get_db().cursor()

    id_jean = request.form.get('id_jean')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    # attention au doublon
    get_db().commit()
    return redirect('/admin/article/edit?id_jean=' + id_jean)


@admin_declinaison_jean.route('/admin/declinaison_jean/edit', methods=['GET'])
def edit_declinaison_jean():
    id_declinaison_jean = request.args.get('id_declinaison_jean')
    mycursor = get_db().cursor()
    declinaison_jean=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/jean/edit_declinaison_jean.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_article=declinaison_jean
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_jean.route('/admin/declinaison_jean/edit', methods=['POST'])
def valid_edit_declinaison_jean():
    id_declinaison_jean = request.form.get('id_declinaison_jean','')
    id_jean = request.form.get('id_jean','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_jean modifié , id:' + str(id_declinaison_jean) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/jean/edit?id_jean=' + str(id_jean))


@admin_declinaison_jean.route('/admin/declinaison_jean/delete', methods=['GET'])
def admin_delete_declinaison_jean():
    id_declinaison_jean = request.args.get('id_declinaison_jean','')
    id_jean = request.args.get('id_jean','')

    flash(u'declinaison supprimée, id_declinaison_jean : ' + str(id_declinaison_jean),  'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_jean))
