import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date


db_config = {
    "host": "localhost",
    "user": "chaymae",  
    "password": "chay",  
    "database": "arbre",  
}

def get_connection():
    return mysql.connector.connect(**db_config)

# model
class PersonCreate(BaseModel):
    name: str
    lastname: str
    birthday: date | None = None
    deathday: date | None = None

class PersonUpdate(BaseModel):
    name: str | None = None
    lastname: str | None = None
    birthday: date | None = None
    deathday: date | None = None

class RelationshipCreate(BaseModel):
    type: str 
    person_id: int
    parent_id: int




app = FastAPI()

#créer une personne
@app.post("/person/")
def create_person(person: PersonCreate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        INSERT INTO person (name, lastname, birthday, deathday)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (person.name, person.lastname, person.birthday, person.deathday))
        connection.commit()
        return {"id": cursor.lastrowid, "message": "Person created successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# crer a relationship
@app.post("/relationship/")
def create_relationship(relationship: RelationshipCreate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        INSERT INTO relationship (type, person_id, parent_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (relationship.type, relationship.person_id, relationship.parent_id))
        connection.commit()
        return {"id": cursor.lastrowid, "message": "Relationship created successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# get person
@app.get("/person/{person_id}")
def get_person(person_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM person WHERE id = %s"
        cursor.execute(query, (person_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Person not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# delete person
@app.delete("/person/{person_id}")
def delete_person(person_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM person WHERE id = %s"
        cursor.execute(query, (person_id,))
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Person not found")
        return {"message": "Person deleted successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# màj 
@app.patch("/person/{person_id}")
def update_person(person_id: int, person: PersonUpdate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        UPDATE person
        SET name = COALESCE(%s, name),
            lastname = COALESCE(%s, lastname),
            birthday = COALESCE(%s, birthday),
            deathday = COALESCE(%s, deathday)
        WHERE id = %s
        """
        cursor.execute(query, (person.name, person.lastname, person.birthday, person.deathday, person_id))
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Person not found")
        return {"message": "Person updated successfully"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()


