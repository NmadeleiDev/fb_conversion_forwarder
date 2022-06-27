import random
from string import ascii_lowercase, digits

from ..utils.utils import generate_random_string


german_cities = ['Berlin', 'Hamburg', 'Munich (München)', 'Cologne (Köln)',
       'Frankfurt am Main', 'Stuttgart', 'Düsseldorf', 'Dortmund',
       'Essen', 'Leipzig', 'Bremen', 'Dresden', 'Hanover (Hannover)',
       'Nuremberg (Nürnberg)', 'Duisburg', 'Bochum', 'Wuppertal',
       'Bielefeld', 'Bonn', 'Münster', 'Karlsruhe', 'Mannheim',
       'Augsburg', 'Wiesbaden', 'Gelsenkirchen', 'Mönchengladbach',
       'Braunschweig', 'Chemnitz', 'Kiel', 'Aachen', 'Halle (Saale)',
       'Magdeburg', 'Freiburg im Breisgau', 'Krefeld', 'Lübeck',
       'Oberhausen', 'Erfurt', 'Mainz', 'Rostock', 'Kassel', 'Hagen',
       'Hamm', 'Saarbrücken', 'Mülheim an der Ruhr', 'Potsdam',
       'Ludwigshafen am Rhein', 'Oldenburg', 'Leverkusen', 'Osnabrück',
       'Solingen', 'Heidelberg', 'Herne', 'Neuss', 'Darmstadt',
       'Paderborn', 'Regensburg', 'Ingolstadt', 'Würzburg', 'Fürth',
       'Wolfsburg', 'Offenbach am Main', 'Ulm', 'Heilbronn', 'Pforzheim',
       'Göttingen', 'Bottrop', 'Trier', 'Recklinghausen', 'Reutlingen',
       'Bremerhaven', 'Koblenz', 'Bergisch Gladbach', 'Jena', 'Remscheid',
       'Erlangen', 'Moers', 'Siegen', 'Hildesheim', 'Salzgitter']

german_names = ['Abraham', 'Achim', 'Adam', 'Adel', 'Adelbert', 'Adolf', 'Adrian', 'Albert', 'Albrecht', 'Alexander', 'Alfred', 'Alois', 'Alvin', 'Alwin', 'Amadeus', 'Andreas', 'Ansgar', 'Anthon', 'Anton', 'Antony', 'Aribert', 'Armin', 'Arndt', 'Arno', 'Arnold', 'Arnulf', 'Artur', 'Arved', 'Arvin', 'August', 'Aurick', 'Axel', 'Baldur', 'Bastian', 'Beat', 'Benedict', 'Berengar', 'Bernd', 'Bernhard', 'Bertram', 'Bertrand', 'Bjorn', 'Bodo', 'Bruno', 'Calvin', 'Carl', 'Carolus', 'Charl', 'Christian', 'Christof', 'Christoph', 'Clemens', 'Conrad', 'Dagobert', 'Daniel', 'David', 'Delbert', 'Derek', 'Detlef', 'Detlev', 'Diederich', 'Diedrich', 'Diepold', 'Dieter', 'Dieterich', 'Dietmar', 'Dietrich', 'Dirk', 'Edmund', 'Egbert', 'Egon', 'Ehren', 'Ehrhard', 'Eibert', 'Eike', 'Eilhard', 'Eitel', 'Ekkehard', 'Elias', 'Elimar', 'Elmar', 'Emil', 'Emmerich', 'Engelbert', 'Erhard', 'Eric', 'Ernst', 'Ewald', 'Fabian', 'Felix', 'Ferdinand', 'Florian', 'Frank', 'Franz', 'Fredrik', 'Fridolf', 'Fridolin', 'Friedemann', 'Frieder', 'Friedrich', 'Friedrich', 'Fritz', 'Gabriel', 'Garibald', 'Gebhard', 'Georg', 'Gerald', 'Gerd', 'Gerhard', 'Gerhardt', 'Gerhold', 'Germar', 'Gernot', 'Gert', 'Gerwin', 'Gilbert', 'Giselbert', 'Giselher', 'Gottfried', 'Gottlieb', 'Gottlob', 'Gottschalk', 'Götz', 'Guido', 'Gunther', 'Günther', 'Gustav', 'Gustl', 'Hanno', 'Hans', 'Hans-Ulrich', 'Hansjörg', 'Harald', 'Harold', 'Hartmut', 'Hasso', 'Hauke', 'Heiko', 'Hein', 'Heine', 'Heiner', 'Heini', 'Heino', 'Heinrich', 'Heinz', 'Helge', 'Hellmuth', 'Helmut', 'Helmuth', 'Henning', 'Henno', 'Herbert', 'Heribert', 'Herman', 'Hermann', 'Herschel', 'Herwig', 'Holger', 'Horst', 'Hubert', 'Hubertus', 'Hugo', 'Ignatz', 'Ignaz', 'Ingo', 'Jacob', 'Jakob', 'Jan', 'Jannik', 'Jerome', 'Joachim', 'Joachim-Friedrich', 'Johann', 'Johannes', 'Jonas', 'Jonathan', 'Jörg', 'Josef', 'Jost', 'Jupp', 'Jürgen', 'Kalli', 'Karl', 'Karl-Heinz', 'Karlheinz', 'Karsten', 'Kaspar', 'Kepler', 'Klaus', 'Klaus-Peter', 'Klemens', 'Knut', 'Konrad', 'Konrad', 'Kuno', 'Kurd', 'Kurt', 'Lars', 'Leon', 'Leopold']

german_surnames = ['Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Schäfer', 'Koch', 'Bauer', 'Richter', 'Klein', 'Wolf', 'Schröder', 'Neumann', 'Schwarz', 'Zimmermann', 'Braun', 'Krüger', 'Hofmann', 'Hartmann', 'Lange', 'Schmitt', 'Werner', 'Schmitz', 'Krause', 'Meier', 'Lehmann', 'Schmid', 'Schulze', 'Maier', 'Köhler', 'Herrmann', 'König', 'Walter', 'Mayer', 'Huber', 'Kaiser', 'Fuchs', 'Peters', 'Lang', 'Scholz', 'Möller', 'Weiß', 'Jung', 'Hahn', 'Schubert', 'Vogel', 'Friedrich', 'Keller', 'Günther', 'Frank', 'Berger', 'Winkler', 'Roth', 'Beck', 'Lorenz', 'Baumann', 'Franke', 'Albrecht', 'Schuster', 'Simon', 'Ludwig', 'Böhm', 'Winter', 'Kraus', 'Martin', 'Schumacher', 'Krämer', 'Vogt', 'Stein', 'Jäger', 'Otto', 'Sommer', 'Groß', 'Seidel', 'Heinrich', 'Brandt', 'Haas', 'Schreiber', 'Graf', 'Schulte', 'Dietrich', 'Ziegler', 'Kuhn', 'Kühn', 'Pohl', 'Engel', 'Horn', 'Busch', 'Bergmann', 'Thomas', 'Voigt', 'Sauer', 'Arnold', 'Wolff', 'Pfeiffer', 'Nowak', 'Noack', 'Pietsch', 'Yilmaz', 'Kaya', 'Nguyen']

genders = ['m', 'f']

    
def random_date_of_birth() -> str:
    year = str(random.randint(1960, 2000))
    month = str(random.randint(1, 12)).rjust(2, '0')
    day = str(random.randint(1, 27)).rjust(2, '0')
    return f'{year}{month}{day}'

def random_email() -> str:
    return f'{generate_random_string(random.randint(6, 14), src_chars=ascii_lowercase)}@gmail.com'

def random_phone_number() -> str:
    return f'+49{generate_random_string(9, src_chars=digits)}'
