DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS _date_update_;
DROP TABLE IF EXISTS _date_commentaire_;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS _date_consultation_;
DROP TABLE IF EXISTS declinaison;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS jean;
DROP TABLE IF EXISTS coupe_jean;
DROP TABLE IF EXISTS couleur;

CREATE TABLE couleur(
   id_couleur INT ,
   libelle VARCHAR(255),
   code_couleur INT,
   PRIMARY KEY(id_couleur)
);

CREATE TABLE coupe_jean(
   id_coupe_jean INT ,
   nom_coupe VARCHAR(50),
   PRIMARY KEY(id_coupe_jean)
);

CREATE TABLE jean(
   id_jean INT,
   nom_jean VARCHAR(30),
   prix_jean INT,
   fournisseur VARCHAR(50),
   matiere VARCHAR(50),
   marque VARCHAR(50),
   stock INT,
   description VARCHAR(50),
   id_coupe_jean INT NOT NULL,
   image VARCHAR(50),

   PRIMARY KEY(id_jean),
   FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean)
);

CREATE TABLE taille(
   id_taille INT ,
   libelle VARCHAR(255),
   code_taille INT,
   PRIMARY KEY(id_taille)
);

CREATE TABLE declinaison(
   id_declinaison_jean INT ,
   stock INT,
   prix_declinaison INT,
   image VARCHAR(50),
   id_jean INT NOT NULL,
   id_taille INT NOT NULL,
   id_couleur INT NOT NULL,
   PRIMARY KEY(id_declinaison_jean),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille),
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur)
);

CREATE TABLE _date_consultation_(
   date_consultation DATE,
   PRIMARY KEY(date_consultation)
);

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(255),
   password VARCHAR(255),
   email VARCHAR(255),
   role VARCHAR(255),
   est_actif tinyint(1),
   nom VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE adresse(
   id_adresse INT,
   nom VARCHAR(50),
   rue VARCHAR(50),
   code_postal INT,
   ville VARCHAR(50),
   date_utilisation DATE,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE _date_commentaire_(
   date_publication DATE,
   PRIMARY KEY(date_publication)
);

CREATE TABLE _date_update_(
   date_update DATE,
   PRIMARY KEY(date_update)
);

CREATE TABLE commande(
   id_commande INT,
   date_achat DATE,
   id_utilisateur INT NOT NULL,
   id_adresse INT NOT NULL,
   id_adresse_1 INT NOT NULL,
   id_etat INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_adresse) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_adresse_1) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_panier(
   id_declinaison_jean INT ,
   id_utilisateur INT,
   quantite VARCHAR(50),
   date_ajout VARCHAR(50),
   PRIMARY KEY(id_declinaison_jean, id_utilisateur),
   FOREIGN KEY(id_declinaison_jean) REFERENCES declinaison(id_declinaison_jean),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE commentaire(
   id_jean INT,
   id_utilisateur INT,
   date_publication DATE,
   commentaire VARCHAR(255),
   valider VARCHAR(255),
   PRIMARY KEY(id_jean, id_utilisateur, date_publication),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(date_publication) REFERENCES _date_commentaire_(date_publication)
);

CREATE TABLE historique(
   id_jean INT,
   date_consultation DATE,
   id_utilisateur INT,
   PRIMARY KEY(id_jean, date_consultation, id_utilisateur),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(date_consultation) REFERENCES _date_consultation_(date_consultation),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE liste_envie(
   id_jean INT,
   id_utilisateur INT,
   date_update DATE,
   PRIMARY KEY(id_jean, id_utilisateur, date_update),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(date_update) REFERENCES _date_update_(date_update)
);

CREATE TABLE note(
   id_jean INT,
   id_utilisateur INT,
   note VARCHAR(50),
   PRIMARY KEY(id_jean, id_utilisateur),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   id_declinaison_jean INT,
   id_commande INT,
   quantite INT,
   prix INT,
   PRIMARY KEY(id_declinaison_jean, id_commande),
   FOREIGN KEY(id_declinaison_jean) REFERENCES declinaison(id_declinaison_jean),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);


INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');


-- Insertions dans la table coupe_jean
INSERT INTO coupe_jean (id_coupe_jean, nom_coupe) VALUES
(1, 'Slim'),
(2, 'Droit'),
(3, 'Bootcut'),
(4, 'Skinny');



INSERT INTO taille (id_taille, libelle, code_taille)
VALUES
(1, 'S', 1),
(2, 'M', 2),
(3, 'L', 3),
(4, 'XL', 4);

INSERT INTO couleur (id_couleur, libelle, code_couleur)
VALUES
(1, 'Noir', 1),
(2, 'Bleu', 2),
(3, 'Blanc', 3),
(4, 'Gris', 4);

INSERT INTO jean (id_jean, nom_jean, prix_jean, fournisseur, matiere, marque, stock, description, id_coupe_jean, image)
VALUES
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

INSERT INTO declinaison (id_declinaison_jean, stock, prix_declinaison, image, id_jean, id_taille, id_couleur)
VALUES
(1, 10, 50, 'image_1.jpg', 1, 1, 1),
(2, 15, 60, 'image_2.jpg', 1, 2, 2),
(3, 20, 70, 'image_3.jpg', 2, 1, 3),
(4, 8, 45, 'image_4.jpg', 2, 3, 4);