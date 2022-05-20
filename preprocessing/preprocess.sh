#https://www.data.gouv.fr/fr/datasets/r/ac59a0f5-fa83-4b82-bf12-3c5806d4f19f
#mv ac59a0f5-fa83-4b82-bf12-3c5806d4f19f data.csv
rm of.sqlite
sqlite3 of.sqlite <<'END_SQL'
.separator ";"
.import data.csv complete
CREATE INDEX idx_complete_id ON complete (numeroDeclarationActivite);
CREATE VIRTUAL TABLE search USING fts5 (denomination, siret, id);
INSERT INTO search (denomination, siret, id) SELECT denomination, siretEtablissementDeclarant, numeroDeclarationActivite FROM complete;
END_SQL
mv of.sqlite ../public/db/of.sqlite