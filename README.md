READ ME

Sovellukseksi valitsin esimerkki-aiheista Ravintolasovelluksen:

Lopullisen sovelluksen toiminnot
	
	- Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.
 
	- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 
	- Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolaa, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
 
	- Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
 
	- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
 
	- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on tietty sana.
 
	- Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
 
	- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
 
	- Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.




!HUOMIO
sairastuin aika pahasti tällä viikolla joten sovellus on hyvin yksinkertainen tällä hetkellä.

tämän hetken toiminnot:
	
	- Sivusto, johon voi kirjautua.
 
	- "Näytä ravintolat" -nappi, josta aukeaa lista ravintoloista (nimi, kuvaus, aukioloajat).
 
	- "Takaisin" -nappi, jolla pääsee pois ravintolalistasta.


------------------------------------------------------------------------------------------
Käynnistysohje:

aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:

	python3 -m venv venv
	source venv/bin/activate
	pip install -r ./requirements

Määritä vielä tietokannan skeema komennolla:

	psql < schema.sql
	
voit käynnistää sovelluksen komennolla:
	
	flask run
	
	

