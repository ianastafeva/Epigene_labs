from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/genesets", response_model=List[schemas.Geneset])
def read_all_genesets(db: Session = Depends(get_db)):
    genesets = crud.get_genesets(db)
    return genesets

@app.get("/genesets/search/{pattern}", response_model=List[schemas.Geneset])
def read_match_genesets(pattern: str, db: Session = Depends(get_db)):
    genesets = crud.get_geneset_by_title(db, pattern)
    return genesets


@app.get("/genesets/{geneset_id}", response_model=schemas.Geneset)
def read_geneset(geneset_id: int, db: Session = Depends(get_db)):
    return crud.get_geneset(db, geneset_id)


@app.put("/genesets/{geneset_id}", response_model=schemas.Geneset)
def update_genesets(geneset_id: int, geneset: schemas.GenesetCreate, db: Session = Depends(get_db)):
    return crud.update_geneset(db, geneset_id, geneset.title, geneset.genes)


@app.post("/genesets")
def create_geneset(geneset: schemas.GenesetCreate, db: Session = Depends(get_db)):
    db_geneset = crud.create_geneset_with_genes(db, geneset)
    return db_geneset.id

# addition nb 1
'''Function that allows the user to find a gene based on its name'''

@app.get("/genesets/search/gene/{gene_name}", response_model=List[schemas.Gene])
def read_match_gene( gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_title(db, gene_name)
    return gene   

# addition nb 2
'''Function that allows the user to find a gene based on a title of a geneset and its name'''

@app.get("/genesets/search/geneset/{geneset_title}/gene/{gene_name}", response_model=List[schemas.Gene])
def read_match_gene(geneset_title: str, gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_geneset_and_gene_titles(db, geneset_title, gene_name)
    return gene


# addition nb 3   
'''Function that allows the user to return the name's gene and its genesets titles based on its name'''

@app.get("/genesets/search/{gene_name}/genesets", response_model=List[schemas.GenesetTitle])
def read_gene_sets(gene_name: str, db: Session = Depends(get_db)):
    genesets = crud.get_gene_set(db, gene_name)
    return genesets

# addition nb 4
'''Function that allows the user to choose a slice of data'''

@app.get("/genesets/slice/{slice_st}-{slice_end}", response_model=List[schemas.Geneset])
def read_all_genesets_slice(slice_st: int, slice_end:int, db: Session = Depends(get_db)):
    genesets = crud.get_genesets_slice(db, skip=slice_st, limit=slice_end)
    return genesets

# addition nb 5
'''Function that allows the user to search for genes based in a similarty of input gene name'''

@app.get("/genesets/search/similar-gene-{similarty_threshold}/{gene_name}", response_model=List[schemas.Gene])
def read_similar_gene(similarty_threshold: float, gene_name: str, db: Session = Depends(get_db)):
    genes = crud.get_similar_gene(db, gene_name, similarty_threshold)
    return genes


# addition nb 6
'''Function that allows the user to search for genesset based in a similarty of input geneset title'''

@app.get("/genesets/search/similar-geneset-{similarty_threshold}/{geneset_title}", response_model=List[schemas.Geneset])
def read_similar_genesets(similarty_threshold: float, geneset_title: str, db: Session = Depends(get_db)):
    genesets = crud.get_similar_genesets(db, geneset_title, similarty_threshold)
    return genesets
