import string
import crud, models, schemas
import random

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

letters = string.ascii_lowercase
GENES = [schemas.GeneBase(name=''.join(random.choice(letters) for i in range(4))) for k in range(100)]

db = SessionLocal()

for k in range(1000):
    geneset = schemas.GenesetCreate(title=f"Geneset {k}",genes=random.sample(GENES, 6))
    print(f"Currently populating with geneset {geneset.title}")
    crud.create_geneset_with_genes(db, geneset)


db.close()