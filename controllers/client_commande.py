#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Étape 1 : Sélection des articles du panier
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    # Calcul du prix total du panier
    prix_total = sum(item['prix_jean'] * item['quantite'] for item in articles_panier)

    # Étape 2 : Sélection des adresses
    # À compléter : Ajoutez le code pour récupérer les adresses (livraison et facturation) de l'utilisateur

    return render_template('client/boutique/panier_validation_adresses.html',
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           validation=1
                           #, adresses=adresses
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # Choix de(s) (l')adresse(s)
    id_client = session['id_user']

    # Sélection du contenu du panier de l'utilisateur
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    # Si le panier est vide, redirigez l'utilisateur vers la page d'affichage des articles
    if not items_ligne_panier:
        flash(u'Pas d\'jeans dans le panier', 'alert-warning')
        return redirect('/client/jean/show')

    # Création de la commande
    date_achat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = '''INSERT INTO commande (id_client, date_achat) VALUES (%s, %s)'''
    mycursor.execute(sql, (id_client, date_achat))

    # Récupération du numéro de la dernière commande
    sql = '''SELECT LAST_INSERT_ID() AS last_insert_id'''
    mycursor.execute(sql)
    last_insert_id = mycursor.fetchone()['last_insert_id']

    # Suppression du panier et ajout des articles dans la commande
    for item in items_ligne_panier:
        # Suppression d'une ligne de panier
        sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_declinaison_jean = %s'''
        mycursor.execute(sql, (id_client, item['id_jean']))

        # Ajout d'une ligne de commande
        sql = '''INSERT INTO ligne_commande (id_jean, id_commande, prix, quantite)
                 VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql, (item['id_jean'], last_insert_id, item['prix_jean'], item['quantite']))

    get_db().commit()
    flash(u'Commande ajoutée', 'alert-success')
    return redirect('/client/jean/show')


@client_commande.route('/client/commande/show', methods=['get', 'post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Sélection des commandes ordonnées par état puis par date d'achat descendant
    sql = '''SELECT * FROM commande WHERE id_client = %s ORDER BY id_etat, date_achat DESC'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None

    id_commande = request.args.get('id_commande', None)
    if id_commande is not None:
        # Sélection du détail d'une commande
        sql = '''SELECT * FROM ligne_commande WHERE id_commande = %s'''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

