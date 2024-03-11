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

@app.get("/formations/{formation_id}")
async def get_formation(
    db: db_dependency, 
    formation_id: int,
    ):
    
    result = db.query(models.Formation).filter(models.Formation.id==formation_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La formation n'existe pas !")
    return result


@app.delete("/formations/{formation_id}")
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


@app.put("/formations/{formation_id}")
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


###################################### SESSIONS ######################################
@app.get("/sessions/")
async def get_all_sessions(db: db_dependency):
    
    result = db.query(models.Session).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucune session n'a été ajoutée !")
    return result

@app.get("/sessions/{session_id}")
async def get_session(
    db: db_dependency, 
    session_id: int,
    ):
    
    result = db.query(models.Session).filter(models.Session.id==session_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La session n'existe pas !")
    return result


@app.delete("/sessions/{session_id}")
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


@app.put("/sessions/{session_id}")
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
@app.get("/formation/{formation_id}/courses/")
async def get_all_course_by_formation(db: db_dependency, formation_id: int):
    
    result = db.query(models.FormationCours).filter(models.FormationCours.formationID.id==formation_id).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucun cours n'a été ajouté !")
    
    return result

@app.get("/formation/{formation_id}/courses/{cours_formation_id}")
async def get_all_course_by_formation(db: db_dependency, formation_id: int, cours_formation_id: int):
    
    result = db.query(models.FormationCours).filter(models.FormationCours.formationID.id==formation_id, models.FormationCours.coursID.id==formation_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Aucun cours n'a été ajouté !")
    
    return result

@app.post("/formation/{formation_id}/set_course")
async def set_course_to_formation(db: db_dependency, formation_id:int, course_id: int = Form(), formateur_id: int = Form()):
        
        createdAt = datetime.now()
        db_session = models.FormationCours(
            coursID = course_id,
            formationID = formation_id,
            formateurID = formateur_id,
            createdAt = createdAt,
        )
        
        try:
            # Save the Session object to the database
            db.add(db_session)
            db.commit()
            db.refresh()

            return {"data": db_session}
        except Exception as e:
            print(e)
            return e
        
@app.put("/formation/{formation_id}/set_course")
async def update_course_in_formation(db: db_dependency, formation_id:int, course_id: Optional[int] = Form(None), formateur_id: Optional[int] = Form(None)):
        
        db_session = db.query(models.FormationCours).filter(models.FormationCours.id==formation_id).first()
        
        if course_id:
            db_session.coursID = course_id
        
        if formateur_id:
            db_session.formateurID = formateur_id
        
        updatedAt = datetime.now()
        db_session.updatedAt = updatedAt
        
        try:
            db.commit()
            db.refresh()

            return {"data": db_session}
        except Exception as e:
            print(e)
            return e
        
@app.delete("/formation/{formation_id}/delete")
async def delete_formation(
    db: db_dependency, 
    formation_id: int,
    ):
    
    result = db.query(models.FormationCours).filter(models.FormationCours.id==formation_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="La formation n'existe pas !")
    # print("before delete")
    
    try:
        db.query(models.FormationCours).filter(models.FormationCours.id==formation_id).delete()
        # print("delete")
        db.commit()
    except Exception as e:
        return e
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "formation supprimée !"})

###########################################################################################

########################################### USER ###########################################
@app.get("/users/")
async def get_all_user(db: db_dependency): 

    result = db.query(models.User).all()
    if result:
        return result
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": {'message': "Aucun utilisateur"}})

@app.get("/users/{user_id}")
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

@app.put("/users/{user_id}")
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
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Une erreur s'est produits lors lors de la mise a jour des informations de l'utilisateur !")


@app.delete("/users/{user_id}")
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

@app.get("/roles/{role_id}")
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


@app.put("/roles/{role_id}")
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


@app.delete("/roles/{role_id}")
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

@app.get("/historiques/{historique_id}")
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


@app.put("/history/{history_id}")
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


@app.delete("/history/{history_id}")
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














@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name,  "item_price": item.price, "item_is_offer": item.is_offer, "item_id": item_id}

@app.post("/itemspost")
def post_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_is_offer": item.is_offer, }