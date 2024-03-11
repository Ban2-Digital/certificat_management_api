CREATE TABLE "formation_cours"(
    "id" BIGSERIAL PRIMARY KEY,
    "coursID" BIGINT NOT NULL,
    "formationID" BIGINT NOT NULL,
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "formateurID" BIGINT NOT NULL
);
CREATE INDEX "formation_cours_coursid_index" ON "formation_cours"("coursID");
CREATE INDEX "formation_cours_formationid_index" ON "formation_cours"("formationID");
CREATE INDEX "formation_cours_formateurid_index" ON "formation_cours"("formateurID");

CREATE TABLE "tag_cours"(
    "id" BIGSERIAL PRIMARY KEY,
    "coursID" BIGINT NOT NULL,
    "tagID" BIGINT NOT NULL
);
CREATE INDEX "tag_cours_coursid_index" ON "tag_cours"("coursID");
CREATE INDEX "tag_cours_tagid_index" ON "tag_cours"("tagID");

CREATE TABLE "rapport_formateur"(
    "id" BIGSERIAL PRIMARY KEY,
    "sessionformationID" BIGINT NOT NULL,
    "formateurID" BIGINT NOT NULL,
    "description" TEXT NOT NULL,
    "signatureElectronique" TEXT NULL,
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "sessionID" BIGINT NOT NULL
);
CREATE INDEX "rapport_formateur_sessionformationid_index" ON "rapport_formateur"("sessionformationID");
CREATE INDEX "rapport_formateur_formateurid_index" ON "rapport_formateur"("formateurID");
CREATE INDEX "rapport_formateur_sessionid_index" ON "rapport_formateur"("sessionID");

CREATE TABLE "agent_entreprise"(
    "id" BIGSERIAL PRIMARY KEY,
    "entrepriseID" BIGINT NOT NULL,
    "nom" TEXT NOT NULL,
    "prenom" TEXT NOT NULL,
    "telephone" TEXT NOT NULL,
    "email" TEXT NULL,
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
CREATE INDEX "agent_entreprise_entrepriseid_index" ON "agent_entreprise"("entrepriseID");
ALTER TABLE "agent_entreprise" ADD CONSTRAINT "agent_entreprise_telephone_unique" UNIQUE("telephone");
ALTER TABLE "agent_entreprise" ADD CONSTRAINT "agent_entreprise_email_unique" UNIQUE("email");

CREATE TABLE "formation"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "description" TEXT NULL,
    "imageUrl" TEXT NULL,
    "status" BIGINT NOT NULL DEFAULT '1',
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "formateurID" BIGINT NOT NULL
);
ALTER TABLE "formation" ADD CONSTRAINT "formation_libelle_unique" UNIQUE("libelle");
CREATE INDEX "formation_formateurid_index" ON "formation"("formateurID");

CREATE TABLE "session"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "dateDebut" DATE NOT NULL,
    "dateFin" DATE NOT NULL,
    "typeValidite" TEXT NOT NULL,
    "delaiValidite" INTEGER NOT NULL,
    "dateValidite" DATE NOT NULL,
    "nbreMaxEtudiant" BIGINT NOT NULL,
    "status" INTEGER NOT NULL DEFAULT '1',
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE "entreprise"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "reference" TEXT NOT NULL,
    "nom_responsable" TEXT NOT NULL,
    "email_responsable" TEXT NULL,
    "phone_responsable" TEXT NULL,
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE "entreprise" ADD CONSTRAINT "entreprise_libelle_unique" UNIQUE("libelle");

CREATE TABLE "session_participant"(
    "id" BIGSERIAL PRIMARY KEY,
    "agentEntrepriseID" BIGINT NOT NULL,
    "sessionID" BIGINT NOT NULL,
    "sessionFormationID" BIGINT NOT NULL,
    "isGroupe" BOOLEAN NOT NULL,
    "isPerso" BOOLEAN NOT NULL
);
CREATE INDEX "session_participant_agententrepriseid_index" ON "session_participant"("agentEntrepriseID");
CREATE INDEX "session_participant_sessionid_index" ON "session_participant"("sessionID");
ALTER TABLE "session_participant" ADD CONSTRAINT "session_participant_sessionformationid_unique" UNIQUE("sessionFormationID");

CREATE TABLE "session_formation"(
    "id" BIGSERIAL PRIMARY KEY,
    "sessionID" BIGINT NOT NULL,
    "formationID" BIGINT NOT NULL,
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "isGroupe" BOOLEAN NOT NULL,
    "prixGroupe" INTEGER NOT NULL,
    "isPerso" BOOLEAN NOT NULL,
    "prixPerso" INTEGER NOT NULL,
    "isReductionGroupe" BOOLEAN NOT NULL,
    "pourcentageGroupe" INTEGER NOT NULL,
    "valeurReductionGroupe" INTEGER NOT NULL,
    "isReductionPerso" BOOLEAN NOT NULL,
    "pourcentagePerso" INTEGER NOT NULL,
    "valeurReductionPerso" INTEGER NOT NULL
);
CREATE INDEX "session_formation_sessionid_index" ON "session_formation"("sessionID");
CREATE INDEX "session_formation_formationid_index" ON "session_formation"("formationID");

CREATE TABLE "cours"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "categorieID" BIGINT NOT NULL,
    "description" TEXT NULL,
    "imageUrl" TEXT NULL,
    "status" INTEGER NOT NULL DEFAULT '1',
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE "cours" ADD CONSTRAINT "cours_libelle_unique" UNIQUE("libelle");
CREATE INDEX "cours_categorieid_index" ON "cours"("categorieID");

CREATE TABLE "categorie"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "createAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE "categorie" ADD CONSTRAINT "categorie_libelle_unique" UNIQUE("libelle");

CREATE TABLE "tag"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "createAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE "tag" ADD CONSTRAINT "tag_libelle_unique" UNIQUE("libelle");

CREATE TABLE "fiche_presence"(
    "id" BIGSERIAL PRIMARY KEY,
    "agentEntrepriseID" BIGINT NOT NULL,
    "sessionformationID" BIGINT NOT NULL,
    "formateurID" BIGINT NOT NULL,
    "dateDebut" DATE NOT NULL,
    "dateFin" DATE NOT NULL,
    "signatureElectronique" TEXT NOT NULL,
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
CREATE INDEX "fiche_presence_agententrepriseid_index" ON "fiche_presence"("agentEntrepriseID");
CREATE INDEX "fiche_presence_sessionformationid_index" ON "fiche_presence"("sessionformationID");
CREATE INDEX "fiche_presence_formateurid_index" ON "fiche_presence"("formateurID");

CREATE TABLE "formateur"(
    "id" BIGSERIAL PRIMARY KEY,
    "nom" TEXT NOT NULL,
    "prenom" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "email" TEXT NULL DEFAULT '""',
    "createdAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE "formateur" ADD CONSTRAINT "formateur_phone_unique" UNIQUE("phone");
ALTER TABLE "formateur" ADD CONSTRAINT "formateur_email_unique" UNIQUE("email");

CREATE TABLE "user"(
    "id" BIGSERIAL PRIMARY KEY,
    "username" TEXT NOT NULL,
    "nom" TEXT NOT NULL,
    "prenom" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "roleID" BIGINT NOT NULL,
    "status" INTEGER NOT NULL DEFAULT '1',
    "createAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" BIGINT NOT NULL
);
ALTER TABLE "user" ADD CONSTRAINT "user_username_unique" UNIQUE("username");
ALTER TABLE "user" ADD CONSTRAINT "user_phone_unique" UNIQUE("phone");
ALTER TABLE "user" ADD CONSTRAINT "user_email_unique" UNIQUE("email");
CREATE INDEX "user_roleid_index" ON "user"("roleID");

CREATE TABLE "role"(
    "id" BIGSERIAL PRIMARY KEY,
    "libelle" TEXT NOT NULL,
    "createAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE "historique"(
    "id" BIGSERIAL PRIMARY KEY,
    "userID" BIGINT NOT NULL,
    "description" TEXT NOT NULL,
    "typeOperation" TEXT NOT NULL,
    "createAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
