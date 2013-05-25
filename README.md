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
		<dd>[ ] Home</dd>
		<dd>[ ] Blog</dd>
		<dd>[ ] Gallery</dd>
		<dd>[ ] Schedule</dd>
		<dd>[-] Contact information</dd>
		<dd>[ ] Sponsor-footer</dd>
		<dd>[ ] Daily secret</dd>
		<dd>[-] 'Nolleportalen'</dd>
		<dd>[ ] 'Nolleenkäten'</dd>
		<dd>[x] Register</dd>
</dl>

REQUIREMENTS
======
[in pip] flask-bcrypt (https://github.com/maxcountryman/flask-bcrypt)
[in pip] flask-sqlalchemy
[in pip] sqlalchemy-migrate

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
	<dd>[ ] Flytta 'Enkät' till Loginmenyn</dd>
	<dd>[ ] (NEW BRANCH) Registrering, kolla i funktionen för TODO!</dd>
	<dd>[ ] (NEW BRANCH) Nolleenkäten</dd>
	<dd>[ ] (NEW BRANCH) 'Lägg till användare' i Adminmenyn (t.ex för klassföreståndare osv)</dd>
	<dd>[ ] (NEW BRANCH) get_user_information(role) - hämtar alla users som har role</dd>
	<dd>[ ] (NEW BRANCH) En resultat sida för nolleenkäten, där man ska kunna se statistik över vilka som är med (klass, vad dom önskar göra osv) och kunna flytta nollor kors och tvärs till andra grupper</dd>
	<dd>[ ] (NEW BRANCH) Fixa alla DB tabeller</dd>
	<dd>[ ] Lägg till kommentarer lite här och var</dd>
</dl>

EER
======
http://www.databasteknik.se/webbkursen/er/
