from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union
from fastapi import  File, UploadFile


class FormationCoursBase(BaseModel):
    coursID : int
    formationID : int
    createAt : datetime
    updatedAt : datetime
    formateurID : int
    

class TagCoursBase(BaseModel):
    coursID : int
    tagID : int

class RapportFormateurBase(BaseModel):
    sessionformationID : int
    formateurID : int
    description : str
    signatureElectronique : str
    createAt : datetime
    updatedAt : datetime
    sessionID : int

class AgentEntrepriseBase(BaseModel):
    entrepriseID : int
    nom : str
    prenom : str
    telephone : str
    email : str
    createAt : datetime
    updatedAt : datetime
    

class FormationBase(BaseModel):
    libelle : str
    description : str
    imageUrl: UploadFile
    status : int
    createAt : datetime
    updatedAt : datetime
    formateurID : int

class SessionBase(BaseModel):
    libelle : str
    dateDebut : str
    dateFin : int
    typeValidite : str
    delaiValidite : int
    dateValidite : str
    nbreMaxEtudiant : int
    status : int
    createAt : datetime
    updatedAt : datetime

class EntrepriseBase(BaseModel):
   
    libelle : str
    reference : str
    nom_responsable : str
    email_responsable : str
    phone_responsable : str
    createAt : datetime
    updatedAt : datetime
    
class SessionParticipantBase(BaseModel):
    
    agentEntrepriseID : int
    sessionID : int
    sessionFormationID : int
    isGroupe : bool
    isPerso : bool

class SessionFormationBase(BaseModel):
    
    sessionID : int
    formationID : int
    createAt : datetime
    updatedAt : datetime
    isGroupe : bool
    prixGroupe : int
    isPerso : bool
    prixPerso : int
    isReductionGroupe : bool
    pourcentageGroupe : int
    valeurReductionGroupe : int
    isReductionPerso : bool
    pourcentagePerso : int
    valeurReductionPerso : int
   
class CoursBase(BaseModel):
    libelle : str
    categorieID : int
    description : str
    imageUrl : str
    status : int
    createAt : datetime
    updatedAt : datetime

class CategorieBase(BaseModel):
    libelle : str
    createAt : datetime
    updatedAt : datetime
    
class TagBase(BaseModel):
    libelle : str
    createAt : datetime
    updatedAt : datetime
    

class FichePresenceBase(BaseModel):
    agentEntrepriseID : int
    sessionformationID : int
    formateurID : int
    dateDebut : str 
    dateFin : str 
    signatureElectronique : str 
    createAt : datetime 
    updatedAt : datetime 

class UserBase(BaseModel):
    username : str
    nom : str
    prenom : str
    phone : str
    email : str
    roleID : int
    status : int
    createAt : datetime
    updatedAt : datetime

class RoleBase(BaseModel):
    libelle : str
    createAt : datetime
    updatedAt : datetime
    
class HistoriqueBase(BaseModel):
    userID : int
    description : str
    typeOperation : str
    createAt : datetime
    updatedAt : datetime