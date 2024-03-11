from sqlalchemy import Column, ForeignKeyConstraint, Integer, String, DateTime, ForeignKey, Index, UniqueConstraint, BigInteger, Text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FormationCours(Base):
    __tablename__ = 'formation_cours'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    coursID = Column(BigInteger, nullable=False)
    formationID = Column(BigInteger, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    formateurID = Column(BigInteger, nullable=False)
    __table_args__ = (
        Index('formation_cours_coursid_index', 'coursID'),
        Index('formation_cours_formationid_index', 'formationID'),
        Index('formation_cours_formateurid_index', 'formateurID'),
    )

class TagCours(Base):
    __tablename__ = 'tag_cours'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    coursID = Column(BigInteger, nullable=False)
    tagID = Column(BigInteger, nullable=False)
    __table_args__ = (
        Index('tag_cours_coursid_index', 'coursID'),
        Index('tag_cours_tagid_index', 'tagID'),
    )

class RapportFormateur(Base):
    __tablename__ = 'rapport_formateur'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    sessionformationID = Column(BigInteger, nullable=False)
    formateurID = Column(BigInteger, nullable=False)
    description = Column(Text, nullable=False)
    signatureElectronique = Column(Text)
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    sessionID = Column(BigInteger, nullable=False)
    __table_args__ = (
        Index('rapport_formateur_sessionformationid_index', 'sessionformationID'),
        Index('rapport_formateur_formateurid_index', 'formateurID'),
        Index('rapport_formateur_sessionid_index', 'sessionID'),
    )

class AgentEntreprise(Base):
    __tablename__ = 'agent_entreprise'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    entrepriseID = Column(BigInteger, nullable=False)
    nom = Column(Text, nullable=False)
    prenom = Column(Text, nullable=False)
    telephone = Column(Text, nullable=False)
    email = Column(Text)
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    __table_args__ = (
        Index('agent_entreprise_entrepriseid_index', 'entrepriseID'),
        UniqueConstraint('telephone', name='agent_entreprise_telephone_unique'),
        UniqueConstraint('email', name='agent_entreprise_email_unique'),
    )

class Formation(Base):
    __tablename__ = 'formation'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    libelle = Column(Text, nullable=False)
    description = Column(Text)
    imageUrl = Column(Text)
    status = Column(BigInteger, nullable=False, server_default=text("'1'"))
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    formateurID = Column(BigInteger, nullable=False)
    __table_args__ = (
        UniqueConstraint('libelle', name='formation_libelle_unique'),
        Index('formation_formateurid_index', 'formateurID'),
    )

class Session(Base):
    __tablename__ = 'session'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    libelle = Column(Text, nullable=False)
    dateDebut = Column(Date, nullable=False)
    dateFin = Column(Date, nullable=False)
    typeValidite = Column(Text, nullable=False)
    delaiValidite = Column(Integer, nullable=False)
    dateValidite = Column(Date, nullable=False)
    nbreMaxEtudiant = Column(BigInteger, nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False), nullable=True)

class Entreprise(Base):
    __tablename__ = 'entreprise'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    libelle = Column(Text, nullable=False)
    reference = Column(Text, nullable=False)
    nom_responsable = Column(Text, nullable=False)
    email_responsable = Column(Text)
    phone_responsable = Column(Text)
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    __table_args__ = (
        UniqueConstraint('libelle', name='entreprise_libelle_unique'),
    )

class SessionParticipant(Base):
    __tablename__ = 'session_participant'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    agentEntrepriseID = Column(BigInteger, nullable=False)
    sessionID = Column(BigInteger, nullable=False)
    sessionFormationID = Column(BigInteger, nullable=False)
    isGroupe = Column(Boolean, nullable=False)
    isPerso = Column(Boolean, nullable=False)
    __table_args__ = (
        Index('session_participant_agententrepriseid_index', 'agentEntrepriseID'),
        Index('session_participant_sessionid_index', 'sessionID'),
        UniqueConstraint('sessionFormationID', name='session_participant_sessionformationid_unique'),
    )

class SessionFormation(Base):
    __tablename__ = 'session_formation'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    sessionID = Column(BigInteger, nullable=False)
    formationID = Column(BigInteger, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    isGroupe = Column(Boolean, nullable=False)
    prixGroupe = Column(Integer, nullable=False)
    isPerso = Column(Boolean, nullable=False)
    prixPerso = Column(Integer, nullable=False)
    isReductionGroupe = Column(Boolean, nullable=False)
    pourcentageGroupe = Column(Integer, nullable=False)
    valeurReductionGroupe = Column(Integer, nullable=False)
    isReductionPerso = Column(Boolean, nullable=False)
    pourcentagePerso = Column(Integer, nullable=False)
    valeurReductionPerso = Column(Integer, nullable=False)
    __table_args__ = (
        Index('session_formation_sessionid_index', 'sessionID'),
        Index('session_formation_formationid_index', 'formationID'),
    )

class Cours(Base):
    __tablename__ = 'cours'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    libelle = Column(Text, nullable=False)
    categorieID = Column(BigInteger, nullable=False)
    description = Column(Text)
    imageUrl = Column(Text)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    __table_args__ = (
        UniqueConstraint('libelle', name='cours_libelle_unique'),
        Index('cours_categorieid_index', 'categorieID'),
    )

class Categorie(Base):
    __tablename__ = 'categorie'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    libelle = Column(Text, nullable=False)
    createAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    __table_args__ = (
        UniqueConstraint('libelle', name='categorie_libelle_unique'),
    )

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    libelle = Column(Text, nullable=False)
    createAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    __table_args__ = (
        UniqueConstraint('libelle', name='tag_libelle_unique'),
    )

class FichePresence(Base):
    __tablename__ = 'fiche_presence'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    agentEntrepriseID = Column(BigInteger, nullable=False)
    sessionformationID = Column(BigInteger, nullable=False)
    formateurID = Column(BigInteger, nullable=False)
    dateDebut = Column(Date, nullable=False)
    dateFin = Column(Date, nullable=False)
    signatureElectronique = Column(Text, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=False), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=False))
    __table_args__ = (
        Index('fiche_presence_agententrepriseid_index', 'agentEntrepriseID'),
        Index('fiche_presence_sessionformationid_index', 'sessionformationID'),
        Index('fiche_presence_formateurid_index', 'formateurID'),
    )

# Add foreign key constraints to existing models
TagCours.__table_args__ += (
    ForeignKeyConstraint(['tagID'], ['tag.id'], name='tag_cours_tagid_foreign'),
)
SessionParticipant.__table_args__ += (
    ForeignKeyConstraint(['sessionID'], ['session.id'], name='session_participant_sessionid_foreign'),
    ForeignKeyConstraint(['sessionFormationID'], ['session_formation.id'], name='session_participant_sessionformationid_foreign'),
    ForeignKeyConstraint(['agentEntrepriseID'], ['agent_entreprise.id'], name='session_participant_agententrepriseid_foreign'),
)
AgentEntreprise.__table_args__ += (
    ForeignKeyConstraint(['entrepriseID'], ['entreprise.id'], name='agent_entreprise_entrepriseid_foreign'),
)
FichePresence.__table_args__ += (
    ForeignKeyConstraint(['formateurID'], ['formateur.id'], name='fiche_presence_formateurid_foreign'),
    ForeignKeyConstraint(['agentEntrepriseID'], ['agent_entreprise.id'], name='fiche_presence_agententrepriseid_foreign'),
    ForeignKeyConstraint(['sessionformationID'], ['session_formation.id'], name='fiche_presence_sessionformationid_foreign'),
)

FormationCours.__table_args__ += (
    ForeignKeyConstraint(['formateurID'], ['formateur.id'], name='formation_cours_formateurid_foreign'),
    ForeignKeyConstraint(['coursID'], ['cours.id'], name='formation_cours_coursid_foreign'),
)

Formation.__table_args__ += (
    ForeignKeyConstraint(['formateurID'], ['formateur.id'], name='formation_formateurid_foreign'),
)

SessionFormation.__table_args__ += (
    ForeignKeyConstraint(['sessionID'], ['session.id'], name='session_formation_sessionid_foreign'),
    ForeignKeyConstraint(['formationID'], ['formation.id'], name='session_formation_formationid_foreign'),
)

TagCours.__table_args__ += (
    ForeignKeyConstraint(['coursID'], ['cours.id'], name='tag_cours_coursid_foreign'),
)

RapportFormateur.__table_args__ += (
    ForeignKeyConstraint(['sessionID'], ['session.id'], name='rapport_formateur_sessionid_foreign'),
    ForeignKeyConstraint(['sessionformationID'], ['session_formation.id'], name='rapport_formateur_sessionformationid_foreign'),
)

FormationCours.__table_args__ += (
    ForeignKeyConstraint(['formationID'], ['formation.id'], name='formation_cours_formationid_foreign'),
)

SessionParticipant.__table_args__ += (
    ForeignKeyConstraint(['agentEntrepriseID'], ['agent_entreprise.id'], name='session_participant_agententrepriseid_foreign'),
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    roleID = Column(Integer, ForeignKey('role.id'), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    createAt = Column(DateTime, nullable=False)
    updatedAt = Column(Integer, nullable=True)

    role = relationship("Role", back_populates="users")

    __table_args__ = (Index('user_roleid_index', 'roleID'),)

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    libelle = Column(String, nullable=False)
    createAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=True)

    users = relationship("User", back_populates="role")

class Historique(Base):
    __tablename__ = 'historique'

    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('user.id'), nullable=False)
    description = Column(String, nullable=False)
    typeOperation = Column(String, nullable=False)
    createAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=True)

    __table_args__ = (Index('historique_userid_index', 'userID'),)