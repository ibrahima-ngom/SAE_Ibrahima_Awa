#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']

    # Récupérer toutes les commandes
    sql_commandes = '''
            SELECT c.id_commande, u.login, c.date_achat, COUNT(lc.id_declinaison_jean) AS nbr_jeans, SUM(lc.prix) AS prix_total, e.libelle
            FROM commande c
            JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
            JOIN etat e ON c.id_etat = e.id_etat
            LEFT JOIN ligne_commande lc ON c.id_commande = lc.id_commande
            GROUP BY c.id_commande
            ORDER BY c.date_achat DESC
        '''
    mycursor.execute(sql_commandes)
    commandes = mycursor.fetchall()

    # Récupérer les détails de la commande sélectionnée
    id_commande = request.args.get('id_commande', None)
    jeans_commande = None
    commande_adresse = None
    if id_commande:
        sql_details_commande = '''
                SELECT lc.quantite, lc.prix, lc.prix * lc.quantite AS prix_ligne, d.id_declinaison_jean, j.nom_jean, j.image, j.stock, j.description, t.libelle AS libelle_taille, c.libelle AS libelle_couleur
                FROM ligne_commande lc
                JOIN declinaison d ON lc.id_declinaison_jean = d.id_declinaison_jean
                JOIN jean j ON d.id_jean = j.id_jean
                JOIN taille t ON d.id_taille = t.id_taille
                JOIN couleur c ON d.id_couleur = c.id_couleur
                WHERE lc.id_commande = %s
            '''
        mycursor.execute(sql_details_commande, (id_commande,))
        jeans_commande = mycursor.fetchall()

        sql_adresse_commande = '''
                SELECT a.nom AS nom_livraison, a.rue AS rue_livraison, a.code_postal AS code_postal_livraison, a.ville AS ville_livraison,
                       c.nom AS nom_facturation, c.rue AS rue_facturation, c.code_postal AS code_postal_facturation, c.ville AS ville_facturation,
                       CASE WHEN c.id_adresse IS NULL THEN 'adresse_identique' ELSE 'adresse_différente' END AS adresse_identique
                FROM commande cmd
                JOIN adresse a ON cmd.id_adresse = a.id_adresse
                LEFT JOIN adresse c ON cmd.id_adresse_1 = c.id_adresse
                WHERE cmd.id_commande = %s
            '''
        mycursor.execute(sql_adresse_commande, (id_commande,))
        commande_adresse = mycursor.fetchone()

    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           jeans_commande=jeans_commande,
                           commande_adresse=commande_adresse)


@admin_commande.route('/admin/commande/valider', methods=['POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id:
        print(commande_id)
        # Mettre à jour l'état de la commande à "Expédiée" (id_etat = 2)
        sql = '''UPDATE commande SET id_etat = 2 WHERE id_commande = %s'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
    return redirect('/admin/commande/show')

