#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql = 'DROP TABLE IF EXISTS ligne_commande, ligne_panier, correspond, est, jean, taille, commande, utilisateur, etat, coupe_jean;'
    mycursor.execute(sql)

    # Création de la table utilisateur
    sql = '''
            CREATE TABLE utilisateur (
                id_utilisateur INT AUTO_INCREMENT,
                login VARCHAR(255),
                password VARCHAR(255),
                role VARCHAR(255),
                est_actif TINYINT(1),
                nom VARCHAR(255),
                email VARCHAR(255),
                PRIMARY KEY(id_utilisateur)
            ) DEFAULT CHARSET utf8mb4;
            '''
    mycursor.execute(sql)

    # Insertions dans la table utilisateur
    sql = '''
            INSERT INTO utilisateur (id_utilisateur, login, email, password, role, nom, est_actif) VALUES
            (1, 'admin', 'admin@admin.fr', 'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf', 'ROLE_admin', 'admin', 1),
            (2, 'client', 'client@client.fr', 'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d', 'ROLE_client', 'client', 1),
            (3, 'client2', 'client2@client2.fr', 'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422', 'ROLE_client', 'client2', 1);
            '''
    mycursor.execute(sql)

    # Création de la table coupe_jean
    sql = '''
            CREATE TABLE coupe_jean (
                id_coupe_jean INT,
                nom_coupe VARCHAR(50),
                PRIMARY KEY(id_coupe_jean)
            ) DEFAULT CHARSET utf8;
            '''
    mycursor.execute(sql)

    # Insertions dans la table coupe_jean
    sql = '''
            INSERT INTO coupe_jean (id_coupe_jean, nom_coupe) VALUES
            (1, 'Slim'),
            (2, 'Droit'),
            (3, 'Bootcut'),
            (4, 'Skinny');
            '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE etat (
            id_etat INT,
            libelle VARCHAR(50),
            PRIMARY KEY(id_etat)
        ) DEFAULT CHARSET=utf8;
        '''
    mycursor.execute(sql)

    # Insertions dans la table etat
    sql = '''
        INSERT INTO etat (id_etat, libelle) VALUES
        (1, 'En cours'),
        (2, 'Expédié'),
        (3, 'Livré');
        '''
    mycursor.execute(sql)
    sql = '''
        CREATE TABLE jean (
            id_jean INT,
            nom_jean VARCHAR(30),
            prix_jean INT,
            fournisseur VARCHAR(50),
            matiere VARCHAR(50),
            marque VARCHAR(50),
            stock INT,
            description VARCHAR(50),
            id_coupe_jean INT NOT NULL,
            image VARCHAR(250),
            PRIMARY KEY(id_jean),
            FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean)
        );
        '''
    mycursor.execute(sql)

    # Insertions dans la table jean
    sql = '''
        INSERT INTO jean (id_jean, nom_jean, prix_jean, fournisseur, matiere, marque, stock, description, id_coupe_jean, image) VALUES
        (1, 'cargo', 50, 'FournisseurA', 'Denim', 'MarqueX', 10, 'Description du jean slim', 1, 'cargo.jpg'),
        (2, 'chino ajuste', 40, 'FournisseurB', 'Coton', 'MarqueY', 5, 'Description du jean droit', 2, 'chino_ajuste.jpg'),
        (3, 'Jean', 60, 'FournisseurC', 'Denim', 'MarqueZ', 8, 'Description du jean skinny', 3, 'jean.jpg'),
        (4, 'Jean motif foudre', 45, 'FournisseurA', 'Coton', 'MarqueX', 9, 'Description du jean bootcut', 4, 'jean_motif_foudre.jpg'),
        (5, 'Jean skinny', 55, 'FournisseurB', 'Denim', 'MarqueY', 11, 'Description du jean large', 1, 'jean_skinny_decontracte.jpg'),
        (6, 'Jean bootcut', 65, 'FournisseurC', 'Coton', 'MarqueZ', 20, 'Description du jean taille haute', 2, 'jean_bootcut_decontracte.jpg'),
        (7, 'Jean slim', 75, 'FournisseurA', 'Denim', 'MarqueX', 13, 'Description du jean déchiré', 3, 'jean_slim.jpg'),
        (8, 'pantalon poche', 80, 'FournisseurB', 'Coton', 'MarqueY', 11, 'Description du jean cargo', 4, 'pantalon_poche.jpg'),
        (9, 'Jogjeans', 70, 'FournisseurC', 'Denim', 'MarqueZ', 4, 'Description du jean à jambes larges', 1, 'jogjeans.jpg'),
        (10, 'Jean droit', 55, 'FournisseurA', 'Coton', 'MarqueX', 5, 'Description du jean à ourlet roulé', 2, 'jean_droit.jpg'),
        (11, 'cargo droit ', 60, 'FournisseurB', 'Denim', 'MarqueY', 3, 'Description du jean skinny noir', 3, 'cargo_droit.jpg'),
        (12, 'Jean ajuste', 75, 'FournisseurC', 'Coton', 'MarqueZ', 7, 'Description du jean vintage', 4, 'jean_ajuste.jpg'),
        (13, 'Jean polyvalent', 85, 'FournisseurA', 'Denim', 'MarqueX', 8, 'Description du jean cargo camouflage', 1, 'Jean_Droit_Polyvalent.jpg'),
        (14, 'Jean à trous dechires', 65, 'FournisseurB', 'Coton', 'MarqueY', 11, 'Description du jean mom', 2, 'jean_Avec_trous_dechires.jpg');
        '''
    mycursor.execute(sql)



    # Création de la table ligne_panier
    sql = '''
        CREATE TABLE ligne_panier (
            id_jean INT,
            id_utilisateur INT,
            quantite INT,
            date_ajout DATE,
            PRIMARY KEY(id_jean, id_utilisateur),
            FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
            FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
        );
        '''
    mycursor.execute(sql)

    # Insertions dans la table ligne_panier
    sql = '''
        INSERT INTO ligne_panier (id_jean, id_utilisateur, quantite, date_ajout) VALUES
        (1, 1, 2, '2024-01-27'),
        (2, 2, 1, '2024-01-27'),
        (3, 1, 3, '2024-01-28'),
        (4, 3, 1, '2024-01-28'),
        (5, 2, 2, '2024-01-29'),
        (6, 1, 1, '2024-01-29');
        '''
    mycursor.execute(sql)



    get_db().commit()
    return redirect('/')
