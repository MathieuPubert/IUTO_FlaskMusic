from .app import manager, db

# création des tables
@manager.command
def syncdb():
	db.create_all()

# Ajout d'un nouvel utilisateur
@manager.command
def newUser(username,password):
	from .models import User
	from hashlib import sha256
	m = sha256()
	m.update(password.encode())
	u = User(username=username , password=m.hexdigest())
	db.session.add(u)
	db.session.commit()

# Modification du mot de passe
@manager.command
def changePass(username,oldpassword,newpassword):
	from .models import User
	from hashlib import sha256
	old = sha256()
	old.update(oldpassword.encode())
	u = User.query.get(username)
	if old.hexdigest()==u.password:
		new = sha256()
		new.update(newpassword.encode())
		u.password = new.hexdigest()
		db.session.commit()
		print("Votre mot de passe est bien modifié")
	else:
		print("Votre ancien mot de passe est incorrect")


@manager.command
def loaddb(filename):
    # création de toutes les tables
    db.create_all()

    import yaml
    albums = yaml.load(open(filename))

    # import des modèles
    from .models import Artiste,Album,Avoir_genre,Genre

    #Création des artistes
    artistes = {}
    for album in albums:
        artiste = album["by"]
        if artiste not in artistes:
            o = Artiste(nom_artiste=artiste)
            db.session.add(o)
            artistes[a] = o
    db.session.commit()

	# #Création des Genres
    # genres = {}
    # for album in albums:
    #     artiste = album["by"]
    #     if artiste not in artistes:
    #         o = Artiste(nom_artiste=artiste)
    #         db.session.add(o)
    #         artistes[a] = o
    # db.session.commit()

    # création de tous les albums
    for album in albums:
        artiste = artistes[album["by"]]
        o = Book(titre_album = b["title"],
                 annee_album = b["releaseYear"],
                 img_album   = b["img"],
                 id_artiste   = b["by"])
        db.session.add(o)
    db.session.commit()
