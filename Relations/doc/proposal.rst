Relations: Blaupause
====================

:Author: Daniel Nouri

.. contents::

Problemstellung
---------------
Das Relations Produkt ist ein v�lliges Rewrite des Produkts
*RelationConstraint*, das im Collective_ auf SourceForge.net liegt.

Archetypes_ stellt mit der *ReferenceEngine* die Basis f�r die Verkn�pfung von
Objekten in einem CMF_ Portal bereit. Das Projekt *Relations* setzt auf dieser
Grundlage auf. Es realisiert Regeln f�r Referenzen und setzt auf leichte
Erweiterbarkeit derer.

Bei der Arbeit mit RelationConstraint, dem Vorg�ngerprojekt, gab es ein
schwerwiegendes Problem: Mit jeder neuen, gr��eren Anforderung w�rde sich
die Programmbasis vergr��ern und dadurch die Erweiterbarkeit verloren gehen.

Relations hingegen arbeitet mit austauschbaren Komponenten, welche
unterschiedliche Aufgaben erf�llen. Client- Code kann spezielle Anforderungen
durch eigene Komponenten erf�llen.

.. _collective: http://sf.net/projects/collective
.. _archetypes: http://sf.net/projcets/archetypes
.. _CMF: http://cmf.zope.org

ReferenceJigRegistry
--------------------
* Ist ein Tool, d.h. es existiert einmal im Portal.

* Besitzt die Methoden:

  * registerJig(jig)
        Registriere einen *ReferenceJig*. Die ReferenceJig mu� vom Typ
	*IReferenceable* sein.

  * getJig(id)
        Liefere das ReferenceJig- Objekt mit der Identifikation *id*.

  * getFolder()
        Liefere ein *folderish* Objekt, welches f�r die Speicherung von
	ReferenceJigs geeignet ist.

ReferenceJig
------------
ReferenceJigs existieren global, w�hrend Referenzen (*class Reference*) aus
*Archetypes* eine Verbindung zwischen zwei konkreten Objekten darstellen.

Eine ReferenceJig besitzt eine beliebige Menge an *Implikatoren*,
*Validatoren*, *Finalisierern* und *Vokabulardiensten*.

Zusammen repr�sentieren Implikatoren, Validatoren, Finalisierer und
Vokabulardienste die Eigenschaften einer ReferenceJig. Wir nennen diese
Eigenschaften *ReferenceJig- Komponenten*. Eine solche Komponente kann mehrere
Aufgaben �bernehmen (z.B. gleichzeitig Validator und Vokabulardienst).

Implikatoren und Finalisierer besitzen beide in der Regel eine Verbindungs-
(Postfix *OnConnect*) und eine Trennungsmethode (Postfix *OnDisconnect*).
Der Validator besitzt nur die *validate*- Methode.

Der *Prim�rimplikator* ist derjenige Implikator, der als erstes in der Reihe
der Implikatoren aufgerufen wird: Er ist f�r das Erstellen der Referenz in der
ReferenceEngine zust�ndig.

Vokabulardienste erstellen Listen von m�glichen Zielobjekten. Werden mehrere
Vokabulardienste in Serie geschaltet, wird dem zweiten Dienst das Resultat des
ersten als Argument �bergeben usw. Je nach Strategie werden die vorangegangenen
Resultate dann gefiltert oder erweitert.

Beispiele f�r weitere Implikationen sind Symmetrie und Reflexivit�t. Die
Kardinalit�t ist ein Beispiel eines Validators.

Zusatzprodukte k�nnen weitere ReferenceJig- Komponenten verf�gbar machen, die
sich transparent integrieren.

Eine ReferenceJig l��t sich �ber die Plone Oberfl�che zusammenstellen, d.h. es
k�nnen neue ReferenceJigs erzeugt werden ohne da� *Python- Code* geschrieben
werden mu�.

ReferenceJigs sind serialisierbar. Au�erdem k�nnen sie auch aus Python- Code
heraus erzeugt werden.

ReferenceConnectionProcessor: Ablauf
------------------------------------
0. Benutzer fordert die Erzeugung einer Liste von Referenzen an. Die Quellen
   und Ziele sollen durch bestimmte ReferenceJigs verbunden werden. Der
   *ReferenceConnectionProcessor* arbeitet diese Liste ab.
   
   Der Processor erzeugt die Liste *l* wird erzeugt, die zun�chst leer ist.

1. Die zust�ndige ReferenceJig wird von der ReferenceJigRegistry bezogen.

2. Der Prim�rimplikator verbindet Quelle und Ziel. Hier entsteht das
   Reference Objekt, das in der Folge den weiteren Implikatoren als Argument
   �bergeben werden kann. Das Reference Objekt wird an die Liste *l* angeh�ngt.

   ReferenceJig- Komponenten k�nnen durch einen Hook das Verhalten des
   Reference Objekts mitbestimmen. (Z.B. kann sich eine *CardinalityValidation*
   in den *OFS- Delete- Hook* einklinken.)

3. Die ReferenceJig ruft jeden seiner Implikatoren mit der neuen Referenz auf.

   Die Implikatoren ermitteln eine Menge von weiteren Tripeln (Quelle, Ziel,
   Relationsname). Jedes dieser Tripel bewirkt einen Sprung zu Punkt **1.**.

4. Nachdem die Implikationen stattgefunden haben, wird der neue Zustand durch
   den ReferenceConnectionProcessor validiert. Ist der neue Zustand ung�ltig,
   wird er zur�ckgesetzt auf den Stand zum Zeitpunkt **0.**. (Hier enth�lt die
   Liste *l* die Information �ber die in dieser Anfrage erzeugten, demnach
   aufzul�senden, Referenzen.)

   Validiert werden alle neu erzeugten Referenzen. Die validate() Methode einer
   ReferenceJig kann validate() Methode weiterer Jigs aufrufen.

5. War die Validierung erfolgreich, erreicht der Processor die *finalize*-
   Phase erreicht: F�r jede erzeugte Referenz in der Liste *l* werden die
   entsprechenden Finalizer aufgerufen.
   
   Ein Beispiel f�r ein solches Finalisieren w�re das Anlegen und Referenzieren
   eines Content Objekts, das weitere Information �ber eine oder mehrere
   Verbindungen bereith�lt.

.. image:: relationsdia1.png

Klassendiagramm
---------------
Der Parameter *chain* im Klassendiagramm entspricht der Liste *l* in
`ReferenceConnectionProcessor: Ablauf`_.

.. image:: relationsdia2.png

