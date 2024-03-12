import datetime
from datetime import date
from typing import Annotated, Union
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, Form, status
from database_sys import models
from database_sys.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from database_sys.base_models import *
from settings.config import MEDIA_ROOT
from fastapi.staticfiles import StaticFiles
from utils.manage_file import *
from fastapi.responses import JSONResponse

#####################################################################
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Mount the directory for static files
app.mount("/medias", StaticFiles(directory=MEDIA_ROOT), name="media")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
#####################################################################


@app.get("/")
async def read_root():
    return {"Hello": "World"}

###################################### FORMATIONS ######################################
@app.get("/formations/")
async def get_all_formations(db: db_dependency):
    
    result = db.query(models.Formation).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucune formation n'a été ajoutée !")
    return result

@app.get("/formations/{formation_id}/")
async def get_formation(
    db: db_dependency, 
    formation_id: int,
    ):
    
    result = db.query(models.Formation).filter(models.Formation.id==formation_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La formation n'existe pas !")
    return result


@app.delete("/formations/{formation_id}/")
async def delete_formation(
    db: db_dependency, 
    formation_id: int,
    ):
    
    result = db.query(models.Formation).filter(models.Formation.id==formation_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La formation n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Formation).filter(models.Formation.id==formation_id).delete()
        # print("delete")
        db.commit()
    except Exception as e:
        return e
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Formation supprimée !"})


@app.post("/formations/")
async def create_formation(
    db: db_dependency, 
    libelle: str = Form(...),
    description: str = Form(...),
    status: int = Form(...),
    formateurID: int = Form(...),
    imageUrl: UploadFile = File(...)
    ):
    
    upload_to = "formations"
    # Save the uploaded file and get the URL
    url = await save_upload_file(imageUrl, upload_to)

    today_date = datetime.now()
    # print("the image url :", url)
    db_formation = models.Formation(
        libelle=libelle,
        description=description,
        imageUrl=url,
        status=status,
        createdAt=today_date,
        formateurID=formateurID
    )
    try:
        # Save the Formation object to the database
        db.add(db_formation)
        db.commit()
        db.refresh()

        return {"data": db_formation}
    except Exception as e:
        return e


@app.put("/formations/{formation_id}/")
async def update_formation(
    db: db_dependency, 
    formation_id: int,
    libelle: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: Optional[int] = Form(None),
    formateurID: Optional[int] = Form(None),
    imageUrl: Optional[UploadFile] = File(None),
    ):
    
    db_formation = db.query(models.Formation).filter(models.Formation.id==formation_id).first()
    
    if db_formation:
        upload_to = "formations"
        if imageUrl:
            # Save the uploaded file and get the URL
            url = await save_upload_file(imageUrl, upload_to)
        else:
            url = ""

        today_date = datetime.now()
        # print("the image url :", url)
        if libelle:
            db_formation.libelle=libelle
        if description:
            db_formation.description=description
        if url:
            db_formation.imageUrl=url
        if status:
            db_formation.status=status
        if formateurID:
            db_formation.formateurID=formateurID
        
        db_formation.updatedAt=today_date

        try:
            # Save the Formation object to the database
            db.commit()
            db.refresh()
            
            return {"data": db_formation,}
        except Exception as e:
            return e
    else:
        raise HTTPException(status_code=404, detail="La formation n'existe pas !")
    
###########################################################################################


###################################### COURS ######################################
@app.get("/cours/")
async def get_all_courses(db: db_dependency):
    
    result = db.query(models.Cours).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucun cours n'a été ajoutée !")
    return result

@app.get("/cours/{cours_id}/")
async def get_course(
    db: db_dependency, 
    cours_id: int,
    ):
    
    result = db.query(models.Cours).filter(models.Cours.id==cours_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Le cours n'existe pas !")
    return result


@app.delete("/cours/{cours_id}/")
async def delete_course(
    db: db_dependency, 
    cours_id: int,
    ):
    
    result = db.query(models.Cours).filter(models.Cours.id==cours_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Le cours n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Cours).filter(models.Cours.id==cours_id).delete()
        # print("delete")
        db.commit()
    except Exception as e:
        return e
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Cours supprimé !"})


@app.post("/cours/")
async def create_course(
    db: db_dependency, 
    libelle: str = Form(...),
    description: str = Form(...),
    status: int = Form(...),
    categorieID: int = Form(...),
    imageUrl: UploadFile = File(...)
    ):
    
    upload_to = "cours"
    # Save the uploaded file and get the URL
    url = await save_upload_file(imageUrl, upload_to)

    today_date = datetime.now()
    # print("the image url :", url)
    db_cours = models.Cours(
        libelle=libelle,
        description=description,
        imageUrl=url,
        status=status,
        createdAt=today_date,
        categorieID=categorieID
    )
    try:
        # Save the Formation object to the database
        db.add(db_cours)
        db.commit()
        db.refresh()

        return {"data": db_cours}
    except Exception as e:
        return e


@app.put("/cours/{cours_id}/")
async def update_course(
    db: db_dependency, 
    cours_id: int,
    libelle: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: Optional[int] = Form(None),
    categorieID: Optional[int] = Form(None),
    imageUrl: Optional[UploadFile] = File(None),
    ):
    
    db_course = db.query(models.Cours).filter(models.Cours.id==cours_id).first()
    
    if db_course:
        upload_to = "cours"
        if imageUrl:
            # Save the uploaded file and get the URL
            url = await save_upload_file(imageUrl, upload_to)
        else:
            url = ""

        today_date = datetime.now()
        # print("the image url :", url)
        if libelle:
            db_course.libelle=libelle
        if description:
            db_course.description=description
        if url:
            db_course.imageUrl=url
        if status:
            db_course.status=status
        if categorieID:
            db_course.categorieID=categorieID
        
        db_course.updatedAt=today_date

        try:
            # Save the Formation object to the database
            db.commit()
            db.refresh()
            
            return {"data": db_course,}
        except Exception as e:
            return e
    else:
        raise HTTPException(status_code=404, detail="Le cours n'existe pas !")
    
###########################################################################################


###################################### SESSIONS ######################################
@app.get("/sessions/")
async def get_all_sessions(db: db_dependency):
    
    result = db.query(models.Session).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucune session n'a été ajoutée !")
    return result

@app.get("/sessions/{session_id}/")
async def get_session(
    db: db_dependency, 
    session_id: int,
    ):
    
    result = db.query(models.Session).filter(models.Session.id==session_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La session n'existe pas !")
    return result


@app.delete("/sessions/{session_id}/")
async def delete_session(
    db: db_dependency, 
    session_id: int,
    ):
    
    result = db.query(models.Session).filter(models.Session.id==session_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La session n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Session).filter(models.Session.id==session_id).delete()
        # print("delete")
        db.commit()
    except Exception as e:
        return e
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Session supprimée !"})


@app.post("/sessions/")
async def create_session(
    db: db_dependency, 
    libelle: str = Form(...),
    dateDebut: date = Form(...),
    dateFin: date = Form(...),
    session_status: int = Form(...),
    typeValidite: str = Form(...),
    delaiValidite: int = Form(...),
    dateValidite: str = Form(...),
    nbreMaxEtudiant: int = Form(...),
    ): 

    today_date = datetime.now()
    # print("the image url :", url)
    db_session = models.Session(
        libelle=libelle,
        dateDebut=dateDebut,
        dateFin=dateFin,
        status=session_status,
        createdAt=today_date,
        typeValidite=typeValidite,
        delaiValidite=delaiValidite,
        dateValidite=dateValidite,
        nbreMaxEtudiant=nbreMaxEtudiant,
    )
    try:
        # Save the Session object to the database
        db.add(db_session)
        db.commit()
        db.refresh()

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": db_session})
    except Exception as e:
        print(e)
        return e


@app.put("/sessions/{session_id}/")
async def update_session(
    db: db_dependency, 
    session_id: int,
    libelle: Optional[str] = Form(None),
    dateDebut: Optional[datetime] = Form(None),
    dateFin: Optional[datetime] = Form(None),
    status: Optional[int] = Form(None),
    typeValidite: Optional[str] = Form(None),
    delaiValidite: Optional[int] = Form(None),
    dateValidite: Optional[str] = Form(None),
    nbreMaxEtudiant: Optional[int] = Form(None),
    ):
    
    db_session = db.query(models.Session).filter(models.Session.id==session_id).first()
    
    if db_session:
        

        today_date = datetime.now()
        # print("the image url :", url)
        if libelle:
            db_session.libelle=libelle
        if dateDebut:
            db_session.dateDebut=dateDebut
        if dateFin:
            db_session.dateFin=dateFin
        if status:
            db_session.status=status
        if typeValidite:
            db_session.typeValidite=typeValidite
        if delaiValidite:
            db_session.delaiValidite=delaiValidite
        if dateValidite:
            db_session.dateValidite=dateValidite
        if nbreMaxEtudiant:
            db_session.nbreMaxEtudiant=nbreMaxEtudiant
        
        db_session.updatedAt=today_date

        try:
            # Save the Formation object to the database
            db.commit()
            db.refresh()
            
            return {"data": db_session,}
        except Exception as e:
            return e
    else:
        raise HTTPException(status_code=404, detail="La session n'existe pas !")
    
###########################################################################################

###################################### FORMATION COURS ######################################
# @app.get("/formation/{formation_id}/courses/")
# async def get_all_course_by_formation(db: db_dependency, formation_id: int):
    
#     result = db.query(models.FormationCours).filter(models.FormationCours.formationID.id==formation_id).all()
    
#     if not result:
#         raise HTTPException(status_code=404, detail="Aucun cours n'a été ajouté !")
    
#     return result

# @app.get("/formation/{formation_id}/courses/{cours_formation_id}/")
# async def get_all_course_by_formation(db: db_dependency, formation_id: int, cours_formation_id: int):
    
#     result = db.query(models.FormationCours).filter(models.FormationCours.formationID.id==formation_id, models.FormationCours.coursID.id==formation_id).first()
    
#     if not result:
#         raise HTTPException(status_code=404, detail="Aucun cours n'a été ajouté !")
    
#     return result

# @app.post("/formation/{formation_id}/set_course")
# async def set_course_to_formation(db: db_dependency, formation_id:int, course_id: int = Form(), formateur_id: int = Form()):
        
#         createdAt = datetime.now()
#         db_session = models.FormationCours(
#             coursID = course_id,
#             formationID = formation_id,
#             formateurID = formateur_id,
#             createdAt = createdAt,
#         )
        
#         try:
#             # Save the Session object to the database
#             db.add(db_session)
#             db.commit()
#             db.refresh()

#             return {"data": db_session}
#         except Exception as e:
#             print(e)
#             return e
        
# @app.put("/formation/{formation_id}/set_course")
# async def update_course_in_formation(db: db_dependency, formation_id:int, course_id: Optional[int] = Form(None), formateur_id: Optional[int] = Form(None)):
        
#         db_session = db.query(models.FormationCours).filter(models.FormationCours.id==formation_id).first()
        
#         if course_id:
#             db_session.coursID = course_id
        
#         if formateur_id:
#             db_session.formateurID = formateur_id
        
#         updatedAt = datetime.now()
#         db_session.updatedAt = updatedAt
        
#         try:
#             db.commit()
#             db.refresh()

#             return {"data": db_session}
#         except Exception as e:
#             print(e)
#             return e
        
# @app.delete("/formation/{formation_id}/delete")
# async def delete_formation(
#     db: db_dependency, 
#     formation_id: int,
#     ):
    
#     result = db.query(models.FormationCours).filter(models.FormationCours.id==formation_id).first()
    
#     if not result:
#         raise HTTPException(status_code=404, detail="La formation n'existe pas !")
#     # print("before delete")
    
#     try:
#         db.query(models.FormationCours).filter(models.FormationCours.id==formation_id).delete()
#         # print("delete")
#         db.commit()
#     except Exception as e:
#         return e
    
#     return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "formation supprimée !"})

###########################################################################################

######################################## TAG ########################################
@app.get("/tags/")
async def get_all_tags(db: db_dependency):
    result = db.query(models.Tag).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucun tag"}})

@app.get("/tags/{tag_id}/")
async def get_tag(db: db_dependency, tag_id: int): 

    result = db.query(models.Tag).filter(models.Tag.id==tag_id).first()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "le tag n'existe pas !"}})

@app.post("/tags/")
async def create_tag(db: db_dependency, 
    libelle: str = Form(...),
    ): 

    today_date = datetime.now()
    db_tag = models.Tag(
        libelle=libelle,
        createAt=today_date,
    )
    try:
        # Save  object to the database
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)

        return db_tag 
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la creation du tag !")


@app.put("/tags/{tag_id}/")
async def update_tag(
    db: db_dependency,
    tag_id: int, 
    libelle: str = Form(),
    ): 

    db_tag = db.query(models.Tag).filter(models.Tag.id==tag_id).first()
    today_date = datetime.now()

    if db_tag:
        if libelle:
            db_tag.libelle=libelle        
        db_tag.updatedAt=today_date
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="le tag n'existe pas !")
    try:
        # Save  object to the database
        db.commit()
        db.refresh(db_tag)

        return db_tag
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la mise a jour des informations du tag !")


@app.delete("/tags/{tag_id}/")
async def delete_tag(db: db_dependency, tag_id: int): 

    result = db.query(models.Tag).filter(models.Tag.id==tag_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Le tag n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Tag).filter(models.Tag.id==tag_id).delete()
        # print("delete")
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="Le tag à été supprimé !")
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produite lors de la suppression du tag")

############################################################################################

######################################## CATEGORIE ########################################
@app.get("/categories/")
async def get_all_categories(db: db_dependency):
    result = db.query(models.Categorie).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucune catégorie"}})

@app.get("/categories/{cat_id}/")
async def get_category(db: db_dependency, cat_id: int): 

    result = db.query(models.Categorie).filter(models.Categorie.id==cat_id).first()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "la catégorie n'existe pas !"}})

@app.post("/categories/")
async def create_category(db: db_dependency, 
    libelle: str = Form(...),
    ): 

    today_date = datetime.now()
    db_cat = models.Categorie(
        libelle=libelle,
        createAt=today_date,
    )
    try:
        # Save  object to the database
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)

        return db_cat 
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la creation de la catégorie !")


@app.put("/categories/{cat_id}/")
async def update_category(
    db: db_dependency,
    cat_id: int, 
    libelle: str = Form(),
    ): 

    db_tag = db.query(models.Categorie).filter(models.Categorie.id==cat_id).first()
    today_date = datetime.now()

    if db_tag:
        if libelle:
            db_tag.libelle=libelle        
        db_tag.updatedAt=today_date
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="la catégorie n'existe pas !")
    try:
        # Save  object to the database
        db.commit()
        db.refresh(db_tag)

        return db_tag
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la mise a jour des informations la catégorie !")


@app.delete("/categories/{cat_id}/")
async def delete_category(db: db_dependency, cat_id: int): 

    result = db.query(models.Categorie).filter(models.Categorie.id==cat_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La categorie n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Categorie).filter(models.Categorie.id==cat_id).delete()
        # print("delete")
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="La catégorie à été supprimé !")
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produite lors de la suppression de la categorie")

############################################################################################

###################################### FICHE PRESENCE ######################################
@app.get("/fiche_presences/")
async def get_all_attendance_sheet(db: db_dependency):
    
    result = db.query(models.FichePresence).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucune fiche de présence n'a été ajoutée !")
    return result

@app.get("/fiche_presences/{sheet_id}/")
async def get_attendance_sheet(
    db: db_dependency, 
    sheet_id: int,
    ):
    
    result = db.query(models.FichePresence).filter(models.FichePresence.id==sheet_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La fiche de présence n'existe pas !")
    return result


@app.delete("/fiche_presences/{sheet_id}/")
async def delete_attendance_sheet(
    db: db_dependency, 
    sheet_id: int,
    ):
    
    result = db.query(models.FichePresence).filter(models.FichePresence.id==sheet_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La fiche de présence n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.FichePresence).filter(models.FichePresence.id==sheet_id).delete()
        # print("delete")
        db.commit()
    except Exception as e:
        return e
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "La fiche de présence à été supprimée !"})


@app.post("/fiche_presences/{sheet_id}/")
async def create_attendance_sheet(
    db: db_dependency, 
    agentEntrepriseID: int = Form(...),
    sessionformationID: int = Form(...),
    formateurID: int = Form(...),
    dateDebut: datetime = Form(...),
    dateFin: datetime = Form(...),
    signatureElectronique: UploadFile = File(...),
    ):

    upload_to = "formateur/signatures"
    # Save the uploaded file and get the URL
    url = await save_upload_file(signatureElectronique, upload_to)
    
    today_date = datetime.now()
    # print("the image url :", url)
    db_attendance = models.FichePresence(
        agentEntrepriseID=agentEntrepriseID,
        sessionformationID=sessionformationID,
        formateurID=formateurID,
        dateDebut=dateDebut,
        dateFin=dateFin,
        signatureElectronique=url,
        createdAt=today_date
    )
    try:
        # Save the Formation object to the database
        db.add(db_attendance)
        db.commit()
        db.refresh()

        return {"data": db_attendance}
    except Exception as e:
        return e


@app.put("/fiche_presences/{sheet_id}/")
async def update_attendance_sheet(
    db: db_dependency, 
    sheet_id: int,
    agentEntrepriseID: Optional[int] = Form(None),
    sessionformationID: Optional[int] = Form(None),
    formateurID: Optional[int] = Form(None),
    dateDebut: Optional[datetime] = Form(None),
    dateFin: Optional[datetime] = Form(None),
    signatureElectronique: Optional[UploadFile] = File(None),
    ):
    
    db_attendance_sheet = db.query(models.FichePresence).filter(models.FichePresence.id==sheet_id).first()
    
    if db_attendance_sheet:
        upload_to = "formations"
        if signatureElectronique:
            # Save the uploaded file and get the URL
            url = await save_upload_file(signatureElectronique, upload_to)
        else:
            url = ""

        today_date = datetime.now()
        # print("the image url :", url)
        if agentEntrepriseID:
            db_attendance_sheet.agentEntrepriseID=agentEntrepriseID
        if sessionformationID:
            db_attendance_sheet.sessionformationID=sessionformationID
        if url:
            db_attendance_sheet.imageUrl=url
        if dateDebut:
            db_attendance_sheet.dateDebut=dateDebut
        if dateFin:
            db_attendance_sheet.dateFin=dateFin
        if formateurID:
            db_attendance_sheet.formateurID=formateurID
        
        db_attendance_sheet.updatedAt=today_date

        try:
            # Save the Formation object to the database
            db.commit()
            db.refresh()
            
            return {"data": db_attendance_sheet,}
        except Exception as e:
            return e
    else:
        raise HTTPException(status_code=404, detail="La fiche de présence n'existe pas !")
 
############################################################################################

########################################### USER ###########################################
@app.get("/users/")
async def get_all_user(db: db_dependency): 

    result = db.query(models.User).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucun utilisateur"}})

@app.get("/users/{user_id}/")
async def get_user(db: db_dependency, user_id: int): 

    result = db.query(models.User).filter(models.User.id==user_id).first()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "l'utilisateur n'existe pas !"}})

@app.post("/users/")
async def create_user(db: db_dependency, 
    username: str = Form(...),
    nom: str = Form(...),
    prenom: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    roleID: int = Form(...),
    user_status: int = Form(...),
    ): 

    today_date = datetime.now()
    db_user = models.User(
        username=username,
        nom=nom,
        prenom=prenom,
        phone=phone,
        email=email,
        roleID=roleID,
        status=user_status,
        createAt=today_date,
    )
    try:
        # Save  object to the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": db_user})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la creation de l'utilisateur !")

@app.put("/users/{user_id}/")
async def update_user(
    db: db_dependency,
    user_id: int, 
    username: Optional[str] = Form(None),
    nom: Optional[str] = Form(None),
    prenom: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    roleID: Optional[int] = Form(None),
    user_status: Optional[int] = Form(None),
    ): 

    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    today_date = datetime.now()

    if db_user:
        if username:
            db_user.username=username
        if nom:
            db_user.nom=nom
        if prenom:
            db_user.prenom=prenom
        if phone:
            db_user.phone=phone
        if email:
            db_user.email=email
        if roleID:
            db_user.roleID=roleID
        if user_status:
            db_user.status=user_status
        
        db_user.updatedAt=today_date
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="l'utilisateur n'existe pas !")
    try:
        # Save  object to the database
        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la mise a jour des informations de l'utilisateur !")


@app.delete("/users/{user_id}/")
async def delete_user(db: db_dependency, user_id: int): 

    result = db.query(models.User).filter(models.User.id==user_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.User).filter(models.User.id==user_id).delete()
        # print("delete")
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="L'utilisateur à été supprimé !")
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produite lors de la suppression de l'utilisateur")

###########################################################################################################################

############################################## ROLE ##############################################
@app.get("/roles/")
async def get_all_roles(db: db_dependency):
    result = db.query(models.Role).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucun role"}})

@app.get("/roles/{role_id}/")
async def get_role(db: db_dependency, role_id: int): 

    result = db.query(models.Role).filter(models.Role.id==role_id).first()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "le role n'existe pas !"}})

@app.post("/roles/")
async def create_role(db: db_dependency, 
    libelle: str = Form(...),
    ): 

    today_date = datetime.now()
    db_role = models.Role(
        libelle=libelle,
        createAt=today_date,
    )
    try:
        # Save  object to the database
        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        return db_role 
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la creation du role !")


@app.put("/roles/{role_id}/")
async def update_role(
    db: db_dependency,
    role_id: int, 
    libelle: str = Form(),
    ): 

    db_role = db.query(models.Role).filter(models.Role.id==role_id).first()
    today_date = datetime.now()

    if db_role:
        if libelle:
            db_role.libelle=libelle        
        db_role.updatedAt=today_date
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="le role n'existe pas !")
    try:
        # Save  object to the database
        db.commit()
        db.refresh(db_role)

        return db_role
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la mise a jour des informations du role !")


@app.delete("/roles/{role_id}/")
async def delete_role(db: db_dependency, role_id: int): 

    result = db.query(models.Role).filter(models.Role.id==role_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Le role n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Role).filter(models.Role.id==role_id).delete()
        # print("delete")
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="Le role à été supprimé !")
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produite lors de la suppression du role")

#######################################################################################################################

################################################## HISTORIQUE ##################################################
@app.get("/historiques/")
async def get_all_history(db: db_dependency):
    result = db.query(models.Historique).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucun historique"}})

@app.get("/historiques/{historique_id}/")
async def get_history(db: db_dependency, history_id: int): 

    result = db.query(models.Historique).filter(models.Historique.id==history_id).first()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "l'historique n'existe pas !"}})

@app.post("/historiques/")
async def create_history(db: db_dependency, 
    userID: int = Form(...),
    description: str = Form(...),
    typeOperation: str = Form(...),
    ): 

    today_date = datetime.now()
    db_history = models.Historique(
        userID=userID,
        description=description,
        typeOperation=typeOperation,
        createAt=today_date,
    )
    try:
        # Save  object to the database
        db.add(db_history)
        db.commit()
        db.refresh(db_history)

        return db_history 
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la creation de l'historique !")


@app.put("/history/{history_id}/")
async def update_history(
    db: db_dependency,
    history_id: int, 
    userID: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    typeOperation: Optional[str] = Form(None),
    ): 

    db_history = db.query(models.Historique).filter(models.Historique.id==history_id).first()
    today_date = datetime.now()

    if db_history:
        if userID:
            db_history.userID=userID        
        if description:
            db_history.description=description        
        if typeOperation:
            db_history.typeOperation=typeOperation        
        db_history.updatedAt=today_date
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="l'historique n'existe pas !")
    try:
        # Save  object to the database
        db.commit()
        db.refresh(db_history)

        return db_history
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la mise a jour des informations de l'historique !")


@app.delete("/history/{history_id}/")
async def delete_role(db: db_dependency, history_id: int): 

    result = db.query(models.Historique).filter(models.Historique.id==history_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="L'historique n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Historique).filter(models.Historique.id==history_id).delete()
        # print("delete")
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="L'historique à été supprimé !")
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produite lors de la suppression de l'historique.")

############################################################################################################


########################################### ENTREPRISE ###########################################
@app.get("/entreprises/")
async def get_all_enterprise(db: db_dependency): 

    result = db.query(models.Entreprise).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucune entreprise"}})

@app.get("/entreprises/{entreprise_id}/")
async def get_enterprise(db: db_dependency, entreprise_id: int): 

    result = db.query(models.Entreprise).filter(models.Entreprise.id==entreprise_id).first()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "l'entreprise n'existe pas !"}})

@app.post("/entreprises/")
async def create_user(db: db_dependency, 
    libelle: str = Form(...),
    reference: str = Form(...),
    nom_responsable: str = Form(...),
    email_responsable: str = Form(...),
    phone_responsable: str = Form(...),
    ): 

    today_date = datetime.now()
    db_enterprise = models.Entreprise(
        libelle=libelle,
        reference=reference,
        nom_responsable=nom_responsable,
        email_responsable=email_responsable,
        phone_responsable=phone_responsable,
        createdAt=today_date,
    )
    try:
        # Save  object to the database
        db.add(db_enterprise)
        db.commit()
        db.refresh(db_enterprise)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": db_enterprise})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la creation de l'entreprise !")

@app.put("/entreprises/{entreprise_id}/")
async def update_user(
    db: db_dependency,
    entreprise_id: int, 
    libelle: Optional[str] = Form(None),
    reference: Optional[str] = Form(None),
    nom_responsable: Optional[str] = Form(None),
    email_responsable: Optional[str] = Form(None),
    phone_responsable: Optional[str] = Form(None),
    ): 

    db_enterprise = db.query(models.Entreprise).filter(models.Entreprise.id==entreprise_id).first()
    today_date = datetime.now()

    if db_enterprise:
        if libelle:
            db_enterprise.libelle=libelle
        if reference:
            db_enterprise.reference=reference
        if nom_responsable:
            db_enterprise.nom_responsable=nom_responsable
        if email_responsable:
            db_enterprise.email_responsable=email_responsable
        if phone_responsable:
            db_enterprise.phone_responsable=phone_responsable
        
        db_enterprise.updatedAt=today_date
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="l'entreprise n'existe pas !")
    try:
        # Save  object to the database
        db.commit()
        db.refresh(db_enterprise)

        return db_enterprise
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors de la mise a jour des informations de l'entreprise !")


@app.delete("/entreprises/{entreprise_id}/")
async def delete_enterprise(db: db_dependency, entreprise_id: int): 

    result = db.query(models.Entreprise).filter(models.Entreprise.id==entreprise_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="L'entreprise n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.Entreprise).filter(models.Entreprise.id==entreprise_id).delete()
        # print("delete")
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="L'entreprise à été supprimé !")
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produite lors de la suppression de l'entreprise")

###########################################################################################################################











@app.get("/items/{item_id}/")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}/")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name,  "item_price": item.price, "item_is_offer": item.is_offer, "item_id": item_id}

@app.post("/itemspost")
def post_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_is_offer": item.is_offer, }