# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file we define instances of the class Movie

import media
import fresh_tomatoes

f_metal_jacket = media.Movie("Full Metal Jacket",
	"A view from a U.S. Marine showing the process from bootcamp to the Vietnam War",
	"https://upload.wikimedia.org/wikipedia/en/9/99/Full_Metal_Jacket_poster.jpg",
	"https://www.youtube.com/watch?v=3j3_iPskjxk",
	1988)

w_warcraft = media.Movie("Warcraft",
	'''As an Orc horde invades the planet Azeroth using a magic portal, a few human heroes 
	and dissenting Orcs must attempt to stop the true evil behind this war''',
	"https://upload.wikimedia.org/wikipedia/en/5/56/Warcraft_Teaser_Poster.jpg",
	"https://www.youtube.com/watch?v=RhFMIRuHAL4",
	2016)

lord_rings = media.Movie("Lord of the Rings",
	'''A meek Hobbit from the Shire and eight companions set out on a journey 
	to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.''',
	"https://images-na.ssl-images-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SY999_CR0,0,673,999_AL_.jpg",
	"https://www.youtube.com/watch?v=RjO5v4Kq1hs",
	2001)

gladiator = media.Movie("Gladiator",
	'''When a Roman General is betrayed, and his family murdered by an emperor's corrupt son, 
	he comes to Rome as a gladiator to seek revenge.''',
	"https://upload.wikimedia.org/wikipedia/en/8/8d/Gladiator_ver1.jpg",
	"https://www.youtube.com/watch?v=owK1qxDselE",
	2000)

akira = media.Movie("Akira",
	"A secret military project endangers Neo-Tokyo....",
	"https://upload.wikimedia.org/wikipedia/en/5/5d/AKIRA_%281988_poster%29.jpg",
	"https://www.youtube.com/watch?v=ZHkCdsW_42I",
	1992)

grand_torino = media.Movie("Grand Torino",
	'''Disgruntled Korean War veteran Walt Kowalski sets out to reform his neighbor, 
	a Hmong teenager who tried to steal Kowalski's prized possession: a 1972 Gran Torino.''',
	"https://upload.wikimedia.org/wikipedia/en/c/c6/Gran_Torino_poster.jpg",
	"https://www.youtube.com/watch?v=9ecW-d-CBPc",
	2009)

# List of movies created
movies = [f_metal_jacket,w_warcraft,lord_rings,gladiator,akira,grand_torino]

# Create web page with all movies
fresh_tomatoes.open_movies_page(movies)
