## Arbeitsauftrag
Entwickeln Sie eine objektorientierte Anwendung, die ein Adressverzeichnis mit den folgenden Anforderungen realisiert:
- - - 
- #### Eingabe von Adressen 
- #### Löschen von Einträgen
- #### Ändern bestehender Einträge
- #### Ausgabe der vollständigen Adressliste
- #### Suche nach Adressen anhand von Namen, Namensanfängen, Geburtsdaten, Telefonnummern und E-Mail Adressen
- #### Angabe der heutigen Geburtstage
- #### Serialisierung der Adressen (z.B. in einer geeigneten SQLite Datenbank)
- - -
## Datenbankaufbau
Für jeden Eintrag sollen als Daten id, firstname, lastname, street,  number, postal-code, place, birthday, phone-number und email in einem Datensatz erfasst werden. Dabei sollen auch unvollständige Einträge erfasst werden können. Mindestens erforderlich soll lastname und firstname sein.

Jedem Eintrag soll eine eindeutige id zugeordnet werden, die bei der Ausgabe mit ausgegeben wird und für Lösch- und Änderungsvorgänge verwendet werden soll.
- - -
## Nutzerschnittstelle CRUD
### Hinzufügen (Create)
Bei der Verwendung des Kommandozeilenschalters --add soll ein Eintrag hinzugefügt werden. Die Attribute werden mit den Kommandozeilenschaltern wie folgt angegeben:

--firstname -> Vorname

--lastname -> Nachname

--street -> Straße

--number -> Hausnummer

--postal_code -> Postleitzahl

--place -> Ort

--birthday -> Das Geburtsdatum im Format YYYY-MM-DD

--phone -> Mobiltelefonnummer

--email -> E-Mail Adresse

## Ausgabe (Read)
Mittels Parameter soll eine Ausgabe erfolgen. Dabei gibt --list das gesamte Verzeichnis aus, --search sucht nach Einträgen, die bestimmten Kriterien entsprechen. Hierbei werden die Kriterien mit den unter Hinzufügen Parametern für das jeweilige Attribut angegeben. Der Asterisk * soll für alle Felder. Get ruft einen Eintrag anhand einer eindeutigen Identifikationsnummer ab.

Die Ausgabe soll auf verschiedene Arten möglich sein:

--list
Ausgabe alle Felder für jeden Eintrag in der Form <Beschreibung>: <Wert>.

--get<id>
          Ausgabe des kompleten Datensatzes für den Eintrag mit der <id>.
--search <searchstring> | [--fieldname <searchstring>]*
suche nach einem Wert. Kann um Feldnamen ergänzt werden.

Sortiert werden die Ausgaben nach Nach- und Vorname.

Ändern (Update)
Mit dem Parameter --update sollen Änderungen möglich sein. Hierbei wird dem Parameter --update die Nummer des betroffenen Eintrags mitgegeben und die im Format wie oben angegebeben Werte werden aktualisiert.

Löschen (Delete)
Mit dem Parameter --del soll ein über seine Identifikationsnummer bezeichneter Eintrag entfernt werden.

Geburtstag heute
Mit dem Parameter --today sollen alle Einträge, deren Geburtstag heute ist, ausgewählt und ausgegeben werden.

 

Beispiele

python myaddrbook.py --get 14

Gibt alle Daten für den Eintrag 14 aus.

python myaddrbook.py --get 12
Gibt die Telefonnummer für Eintrag 12 aus.

python myaddrbook.py --search --mail *@schule.bremen.de --lastname m*
Gibt Nummer, Name und Vorname (default) der Einträge aus, deren E-Mail Adresse auf @schule.bremen.de endet und deren Nachname mit m beginnt.

python myaddrbook.py --add phone=0173-35467 firstname=Tom lastname=Black

Legt einen neuen Datensatz an.

python myaddrbook.py --del 14

Löscht den Datensatz 14 (nach Nachfrage).

python myaddrbook.py --update 14 lastname=White number=13

Ändert den Datensatz 14.

Klassenstruktur
Verwenden Sie midenstens folgenden zwei Klassen:

Address
Die Klasse Address soll die Daten für eine Adresse in ihren Attributen aufnehmen. Sie soll Methoden enthalten, die die erforderlichen Ausgaben des Programms als Zeichenketten zurückliefern (mit return).

AddressDatabase
Die Klasse AddressDatabase soll die Serialisierung kapseln. Außerhalb der Klasse soll kein SQL Syntax verwendet werden. Es sollen geeignete Methoden entwickelt werden, die das Hinzufügen, Abfragen, Ändern und Löschen der Datensätze ermöglicht. Die Methoden der Klasse sollen die Daten in Form von Address Objekten erhalten bzw. liefern. Abfragen und Suchen auf den Daten sollen kann in der SQL Version mittels SQL realisiert werden.

Bearbeitung
Bearbeiten Sie dieses Projekt in Partnerarbeit. Sollte eine Dreiergruppe erforderlich sein, ist zusätzlich ein Mechanismus zum Im- und Export von CSV Dateien in und aus der Datenbak zu entwickeln (Parameter --import und --export).

Dokumentieren und Kommentieren Sie hinreichend und berücksichtigen Sie die einschlägigen Informationen zur Programmierung aus dem Unterricht. Fertigen Sie außerdem ein entsprechendes Protokoll nach den bekannten Vorgaben an, welches unter anderem auch ein Klassendiagramm enthält.