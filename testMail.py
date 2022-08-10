import smtplib

# Configuration SMTP | Ici ajusté pour fonctionné avec Gmail
host_smtp = "smtp.live.com"
port_smtp = 587
email_smtp = "talao.analytics@outlook.fr" # Mon email Gmail
mdp_smtp = "Talao123"  # Mon mot de passe

# Configuration du mail
prenom = "Julien"
formule_p = "Des bises :-*"
email_destinataire = "achillerondo@gmail.com"
mail_content = f'Bonjour {prenom}, tu viens de recevoir mon premier mail, envoyé avec Python ! {formule_p}'

# Création de l'objet mail
mail = smtplib.SMTP(host_smtp, port_smtp) # cette configuration fonctionne pour gmail
mail.ehlo() # protocole pour SMTP étendu
mail.starttls() # email crypté
mail.login(email_smtp, mdp_smtp)
mail.sendmail(email_smtp, email_destinataire, mail_content)
mail.close()