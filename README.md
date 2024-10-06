READ ME

Sovellukseksi valitsin esimerkki-aiheista Ravintolasovelluksen:

Lopullisen sovelluksen toiminnot
 
	- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 
	- Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
 
	- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
 
	- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on tietty sana.
 
	- Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
 
	- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
 
	- Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

tämän hetken toiminnot:
	
	- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 
	- Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
 
	- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
 
	- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on tietty sana.
 
	- Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
 
	- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.


------------------------------------------------------------------------------------------
Asennus ja käynnistysohje:
	
Postgresql asennusohjeet:

Voit luoda vertaisarviointia varten Postgresiin oman tietokannan seuraavasti

$ psql
user=# CREATE DATABASE <testi-tietokannan-nimi>;

Kloonaa repositorio omalle koneellesi komennolla

- https://github.com/BjornKhermik10/Ravintolasovellus-Harjoitusty-.git

Luo myös oma .env tietosto tähän paikalliseen repositorioon, johon pitää laittaa oma salainen avain seuraavasti:

SECRET_KEY=(oma salaavain)

Lisää .env kansioon myös tekemäsi tietokannan osoite seuraavasti:

tietokannan osoitteeksi postgresql:///oman_tietokannan_nimi.

DATABASE_URL=postgresql:///oman_tietokannan_nimi

Luo schemat tietokantaan ensin ja sitten virtuaaliympäristö komennoilla:

psql -d (oman_tietokannan_nimi) < schema.sql

Aktivoi virtuaaliympäristö

source venv/bin/activate

Asenna riippuvuudet komennolla

pip install -r requirements

Käynnistä sovellus

flask run
