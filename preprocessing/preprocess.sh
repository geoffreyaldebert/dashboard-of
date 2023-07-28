#curl -k "https://www.monactiviteformation.emploi.gouv.fr/mon-activite-formation/public/listePubliqueOF?format=csv" > data.csv
rm of.sqlite
sqlite3 of.sqlite <<'END_SQL'
.separator ";"
.import data.csv complete
CREATE INDEX idx_complete_id ON complete (numeroDeclarationActivite);
CREATE VIRTUAL TABLE search USING fts5 (denomination, siret, id);
INSERT INTO search (denomination, siret, id) SELECT denomination, siretEtablissementDeclarant, numeroDeclarationActivite FROM complete;
pragma journal_mode = delete;
pragma page_size = 1024;
insert into search(search) values ('optimize');
vacuum;
END_SQL
mv of.sqlite ../public/db/of.sqlite