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




@admin_commande.route('/admin/commande/show', methods=['GET', 'POST'])
def admin_commande_show():
    db = get_db()
    admin_id = session['id_user']
    id_commande = request.args.get('id_commande', None)

    if id_commande is not None:
        # Récupération des détails de la commande et des adresses
        cursor = db.cursor()
        cursor.execute('''
            SELECT 
            j.nom_jean,
            lc.quantite,
            lc.prix,
            (lc.quantite * lc.prix) AS prix_ligne
        FROM
            ligne_commande AS lc
                INNER JOIN
            declinaison AS d ON lc.id_declinaison_jean = d.id_declinaison_jean
                INNER JOIN
            jean AS j ON d.id_jean = j.id_jean
        WHERE
            lc.id_commande = %s;

        ''', (id_commande, id_commande))
        jeans_commande = cursor.fetchall()

        cursor.execute('''
            SELECT 
                u.login,
                c.date_achat,
                COUNT(lc.id_declinaison_jean) AS nbr_jeans,
                SUM(lc.prix) AS prix_total,
                e.libelle
            FROM
                commande AS c
                    INNER JOIN
                utilisateur AS u ON c.id_utilisateur = u.id_utilisateur
                    INNER JOIN
                ligne_commande AS lc ON c.id_commande = lc.id_commande
                    INNER JOIN
                etat AS e ON c.id_etat = e.id_etat
            WHERE
                c.id_commande = %s
            GROUP BY u.login, c.date_achat, e.libelle;
        ''', (id_commande,))
        commandes = cursor.fetchall()

        return render_template('admin/commandes/show.html',
                               commandes=commandes,
                               jeans_commande=jeans_commande)
    else:
        return "ID de commande non spécifié"


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

