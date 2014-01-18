STABEN
======
Den nya awsumaste STABEN-hemsidan som kommer BLOWA n0llans skalle AAAAWAY

TODO (x == finished)
======
<dl>
	<dd>[x] Set up a new GitHub-repo for the project</dd>
	<dd>[ ] Set up a new testing account on Johan's server</dd>
</dl>

<dl>
	<dt>SITES TO BE INCLUDED ON WEBSITE</dt>
		<dd>[x] Layout page</dd>
		<dd>[x] Home</dd>
		<dd>[ ] Blog</dd>
		<dd>[x] Gallery</dd>
		<dd>[x] Schedule</dd>
		<dd>[x] Contact information</dd>
		<dd>[-] 'Nolleportalen'</dd>
		<dd>[x] 'Nolleenkäten'</dd>
		<dd>[x] Register</dd>
</dl>

REQUIREMENTS
======
<dl>
	<dd>[in pip] flask</dd>
	<dd>[in pip] flask-bcrypt (https://github.com/maxcountryman/flask-bcrypt)</dd>
	<dd>[in pip] flask-sqlalchemy (be sure to install version 0.16! File in dev/files/)</dd>
	<dd>[in pip] flask-mysql</dd>
	<dd>[in pip] sqlalchemy-migrate</dd>
	<dd>[in pip] flask-mail</dd>
	<dd>[in pip] pillow</dd>
</dl>

PROFILE PAGE
======
Nolleportalen
Info:
	Vart man bor
	Ålder
	Bild
	Fejjan
	Klass
	Kommer ifrån

'NOLLEENKÄT'
======
Danne fixar frågor till databasen.
Måste kunna dela upp på prioritet.
Måste kunna dela upp så att minst (helst) 3 pers från samma klass är i samma grupp.
Alla grupper kommer minst ha 9 pers.

KRAV FÖR 'NOLLEENKÄT'
======
Script som plockar ut nollan till olika grupper.
Den som har minst antal 5:or ska ha först prio på de grupper nollan har valt 5:a på, måste ta till hänsyn att det ska vara minst 3 nollor från samma klass i samma grupp.
Om det blir en ensam nolla från en klass i en grupp ska denna plockas ur och sättas in i en annan grupp, helst via hemsidan, om det skiter sig kan man göra det manuellt.
Ska visa all information på en speciell sida på hemsidan så man ser exakt vart han kan placeras om något skiter sig, ska kunnas skrivas ut enkelt.
Ska kunna välja hur många från varje klass ska vara i en grupp.
Ska kunna via en sida där det finns en massa options kunna välja en massa grejjer, resultatet kommer fram på sidan. Spara ner denna lista i en view så vi kan ändra däri.
Man ska kunna markera en grupp klar, och då ska den inte komma med i kommande 'körningar'.
Ska kunna ändra grupper på användare på sidan.

TODO
======
<dl>
	<dd>Läs på om blueprints och strukturera om koden så den blir mer lättanvänd.</dd>
	<dd>Måste försöka dela upp staben.py</dd>
	<dd>Gör en check för uppladdning att det verkligen är en bild</dd>
	<dd></dd>
</dl>

EER
======
http://www.databasteknik.se/webbkursen/er/

TODO AAAAAFTER
======
- https://github.com/mitsuhiko/flask/tree/website
- http://flask.pocoo.org/docs/blueprints/
- Alembic