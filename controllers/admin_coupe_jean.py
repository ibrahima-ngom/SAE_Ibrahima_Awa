#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_coupe_jean = Blueprint('admin_coupe_jean', __name__,
                        template_folder='templates')

@admin_coupe_jean.route('/admin/coupe_jean/show')
def show_coupe_jean():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # coupes_jean = mycursor.fetchall()
    coupes_jean=[]
    return render_template('admin/coupe_jean/show_coupe_jean.html', coupes_jean=coupes_jean)

@admin_coupe_jean.route('/admin/coupe_jean/add', methods=['GET'])
def add_coupe_jean():
    return render_template('admin/coupe_jean/add_coupe_jean.html')

@admin_coupe_jean.route('/admin/coupe_jean/add', methods=['POST'])
def valid_add_coupe_jean():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''INSERT INTO coupe_jean (nom_coupe) VALUES (%s)'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'Type ajouté, libellé : ' + libelle
    flash(message, 'alert-success')
    return redirect('/admin/coupe_jean/show')  # ou bien url_for('show_coupe_jean')


@admin_coupe_jean.route('/admin/coupe_jean/delete', methods=['GET'])
def delete_coupe_jean():
    id_coupe_jean = request.args.get('id_coupe_jean', '')
    mycursor = get_db().cursor()
    sql = '''DELETE FROM coupe_jean WHERE id_coupe_jean = %s'''
    mycursor.execute(sql, (id_coupe_jean,))
    get_db().commit()
    flash(u'Suppression de la coupe de jean, ID : ' + id_coupe_jean, 'alert-success')
    return redirect('/admin/coupe_jean/show')


@admin_coupe_jean.route('/admin/coupe_jean/edit', methods=['GET'])
def edit_coupe_jean():
    id_coupe_jean = request.args.get('id_coupe_jean', '')
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM coupe_jean WHERE id_coupe_jean = %s'''
    mycursor.execute(sql, (id_coupe_jean,))
    coupe_jean = mycursor.fetchone()
    return render_template('admin/coupe_jean/edit_coupe_jean.html', coupe_jean=coupe_jean)


@admin_coupe_jean.route('/admin/coupe_jean/edit', methods=['POST'])
def valid_edit_coupe_jean():
    libelle = request.form['libelle']
    id_coupe_jean = request.form.get('id_coupe_jean', '')
    tuple_update = (libelle, id_coupe_jean)
    mycursor = get_db().cursor()
    sql = '''UPDATE coupe_jean SET nom_coupe = %s WHERE id_coupe_jean = %s'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'Coupe de jean modifiée, ID : ' + id_coupe_jean + ", Libellé : " + libelle, 'alert-success')
    return redirect('/admin/coupe_jean/show')









