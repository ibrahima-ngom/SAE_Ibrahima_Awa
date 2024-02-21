#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_jean = Blueprint('client_jean', __name__,
                        template_folder='templates')

@client_jean.route('/client/index')
@client_jean.route('/client/jean/show')
def client_jean_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Récupérer la liste des jeans depuis la base de données
    sql = "SELECT * FROM jean"
    mycursor.execute(sql)
    jeans = mycursor.fetchall()

    # Récupérer la liste des coupes de jean
    sql_coupe_jean = "SELECT * FROM coupe_jean"
    mycursor.execute(sql_coupe_jean)
    coupe_jean = mycursor.fetchall()

    # Récupérer les articles du panier (vous devrez implémenter cette partie)
    jeans_panier = []
    sql = " SELECT * FROM     "



    # Calculer le prix total du panier (vous devrez implémenter cette partie)
    prix_total = None

    return render_template('client/boutique/panier_jean.html',
                           jeans=jeans,
                           jeans_panier=jeans_panier,
                           prix_total=prix_total,
                           items_filtre=coupe_jean)

