# Post sur le développement technique

Dans le cadre de mon travail chez Etalab en tant que Data Engineer, notamment auprès de la plateforme [data.gouv.fr](https://data.gouv.fr), mes collègues de l’équipe Accompagnement et Edito m’ont signalé qu’un jeu de donnée ayant un succès important générait pas mal de support et de questions d’utilisateurs qui avaient du mal à utiliser les données.

Il s’agit du jeu de données sur la [Liste Publique des Organismes de Formation](https://www.data.gouv.fr/fr/datasets/liste-publique-des-organismes-de-formation-l-6351-7-1-du-code-du-travail/) publié par le Ministère du travail. Le fichier principal est au format csv et d’un poids certain : 28Mo. Difficile donc pour la part des utilisateurs peu familier avec l’informatique d’ouvrir ce csv, de le formater dans son tableur favoris et de trouver l’information qu’il souhaite rapidement. 

Vient alors l’idée des réutilisations de données, super fonctionnalité de la plateforme data.gouv.fr qui consiste à référencer une réutilisation d’un jeu de donnée brut. Cette réutilisation peut être de divers types : site, visualisation, application, document… Nous envisageons alors que l’idéal pour ce cas d’usage est un simple site web de type moteur de recherche, nous permettant de retrouver rapidement l’organisme de formation recherché et ses informations associées.

Je me décide donc à réfléchir au développement d’une telle réutilisation sur mon temps perso. Celle-ci sera bien entendue non officielle.

Premier problème : le poids de la base de donnée : 28Mo. Ce n’est pas très lourd mais on ne peut pas envisager de charger l’entièreté de la base au chargement du site. Cela limite donc le choix d’architecture de l’applicatif. Le choix qui s’impose par défaut est la création d’une API, mais cela implique le développement d’un backend, et par conséquent un maintien applicatif plus conséquent avec notamment l’utilisation d’un serveur pour servir l’API (et donc des coûts supplémentaires).

Ce n’est pas complètement satisfaisant dans le cadre d’une simple réutilisation de donnée.

Data Engineer de formation, je ne connais pas spécialement toutes les possibilités de dévéloppement frontend, et je me pose alors la question saugrenue : peut-on développer un site statique capable de requêter une base de donnée locale ? Je découvre donc le [package javascript sql.js](https://github.com/sql-js/sql.js/) qui répond à cette question en embarquant une base de donnée sqlite et permettant de la requêter. Bien sûr, impossible d’insérer de nouvelle donnée avec une telle architecture, la base de donnée n’est accessible qu’en lecture. Mais c’est précisément notre cas d’usage, on souhaite uniquement lire notre fichier, pas l’enrichir.

Cette solution permet de me passer d’un backend mais ne résout pas le principal problème : limité la volumétrie du site à son chargement. En effet, cette solution impose de charger entièrement la base de donnée sqlite, puis de la requêter par la suite.

Serait-il donc possible d’avoir une librairie permettant d’embarquer une base de donnée mais de ne charger en mémoire que le poids de la réponse à une requête, et pas être obligé de charger toute la base d’un seul coup ? 

En continuant mes recherches, je découvre la librairie [sql.js-httpvfs](https://github.com/phiresky/sql.js-httpvfs) qui semble faire la même chose que la librairie sql.js mais rajoute un wrapper autour de Sqlite utilisant du Web Assembly. Cela permet de déporter une partie du traitement de la gestion de la base de donnée auprès du navigateur web, et permet donc de pouvoir requêter la base sans avoir à la charger entièrement. C’est exactement la solution que je recherche. Le développeur de la librairie a d’ailleurs rédigé un [article très clair et très intéressant que je vous invite à lire](https://phiresky.github.io/blog/2021/hosting-sqlite-databases-on-github-pages/).

Attention, partir sur cette solution implique que les utilisateurs de mon application aient des navigateurs web modernes. C’est une limitation indéniable de cette architecture. Mais cela a le mérite de résoudre mon problème : être capable de développer un site web statique autoportant tout en n’explosant pas le volume de donnée chargé lors de l’utilisation du site.

Ne reste plus qu’implémenter cette architecture à notre cas d’usage. Plus familier avec le vuejs, je cherche des exemples d’utilisation de cette librairie sql.js-httpvfs en vue et je trouve [cet exemple](https://github.com/7110/vue-sql.js-httpvfs) me permettant de démarrer mon projet. 

Premier boulot : convertir mon fichier CSV en base sqlite optimisé pour mon cas d’usage :

```
# Récupération de la ressource CSV sur data.gouv
wget https://www.data.gouv.fr/fr/datasets/r/ac59a0f5-fa83-4b82-bf12-3c5806d4f19f
# Renaming
mv ac59a0f5-fa83-4b82-bf12-3c5806d4f19f data.csv
# Remove old database
rm of.sqlite
# Execute script sqlite3
sqlite3 of.sqlite <<'END_SQL'
# separator of data.csv is ';'
.separator ";"
# import file into table named complete
.import data.csv complete
...
```

Nous avons donc désormais une table complete contenant l'ensemble des données. Après avoir explorer la base, je vois que la colonne `numeroDeclarationActivite` est la clé primaire de la table. Je créé donc un index sur cette colonne (cela me permettra de requêter efficacement toutes les informations d'un organisme particulier).

```
CREATE INDEX idx_complete_id ON complete (numeroDeclarationActivite);
```

Pour la recherche des organismes de formation, la colonne la plus adequat est la `denomination` de l'organisme. Au départ, je créé un simple index sur cette table pour pouvoir la requêter. Problème, faire du full-text search avec une simple colonne `string` peut être gourmand en performance. 

Typiquement, si mon organisme de formation s'appelle `MON ORGANISME DE FORMATION`, ma recherche `MON ORGANISME` pourrait être : 

```
SELECT * FROM complete WHERE denomination LIKE 'MON ORGANISME%';
```

Celle-ci sera efficiente car elle utilisera l'index créé précédemment. Par contre, dans la vraie vie, on requêtera plutôt avec les termes `ORGANISME` plutôt que `MON ORGANISME`. La requête sera donc celle-ci :

```
SELECT * FROM complete WHERE denomination LIKE '%ORGANISME%';
```

Comme on recherche un terme dans une string sans que ces termes soient obligatoirement le début de cette string, sqlite n'utilisera pas l'index et la performance de la requête sera par conséquent très réduite. La base de donnée risque d'être entièrement parcourue et donc entrainerait une explosion de la volumétrie téléchargée sur le site. Il faut donc trouver une autre solution.

En cherchant encore un peu, je trouve qu'il est possible de faire de la [recherche full-text sur une base sqlite](https://www.sqlite.org/fts5.html). Cela consiste à utiliser un module de table virtuelle sqlite proposant ce type de requête full-text. Ni une, ni deux, j'applique cela à mon cas d'usage en créant une table virtuelle dans ma base :

```
CREATE VIRTUAL TABLE search USING fts5 (denomination, siret, id);
INSERT INTO search (denomination, siret, id) SELECT denomination, siretEtablissementDeclarant, numeroDeclarationActivite FROM complete;
```

L'identifiant fourni dans cette table correspond au numéro de déclaration d'activité de l'organisme, qui est unique dans la table. Je pourrai probablement me passer du numéro de siret, lui non unique (un même établissement peut avoir plusieurs déclaration d'activité dans la table), mais je le garde au cas où...

Ainsi, je peux donc requêter efficacement cette table virtuelle de la façon suivante : 

```
SELECT * FROM search WHERE search MATCH 'ORGANISME*' LIMIT 10;
```

Cette requête est très efficiente et récupère sans très grand volume chargé les résultats d'une recherche. A noter, le * qui permet de gérer tous les mots commençant par les termes. On aurait donc rechercher `ORGA`, on aurait quand même trouver le résultat.

Une fois tout cela préparé dans la base sqlite, le logique est assez simple à implémenter dans le développement vuejs. Je vous laisse parcourir le code source pour voir comment vuejs interagit avec sqlite. 

Au final, j'ai développé 3 pages sur ce site, [une page d'accueil](https://organismes-formation.datatouilleur.fr/), très légère, une [page de recherche](https://organismes-formation.datatouilleur.fr/recherche/opencl/page/1) listant les résultats d'une recherche, et une [page d'organisme](https://organismes-formation.datatouilleur.fr/organisme/11755205675) recensant l'ensemble des informations de celui-ci.

Enfin, l'ensemble du site statique est hébergé sur un github pages gratuitement et automatiquement buildé par la CI de github qui est également schedulé pour publier des mises à jour régulières.

Dernier caprice, pour fournir une API des organismes de formation sur ce site, et en se passant d'un backend, j'ai pris la décision de générer un fichier json par record. Cela correspond donc à la génération de 115000 fichiers json qui peuvent donc être requêter par un tiers pour récupérer des informations sur l'organisme ([Exemple](https://organismes-formation.datatouilleur.fr/siren/834199309.json)).  Le process est assez long et dure 40min mais c'est envisageable pour une mise à jour des données peu régulière et surtout traitement pris en charge gratuitement par Github CI ;).

En conclusion, j'ai bien conscience que cette solution technique reste originale et n'est pas adaptée à de nombreux cas d'usage : maintien performant d'une API, moteur de recherche complexe etc. Mais dans le cadre d'une réutilisation de donnée sans grand moyen, cette solution me paraît plutôt séduisante.

Merci de m'avoir lu ;)
