from sqlalchemy.orm import Session
from typing import List


from models import Gene, Geneset
from schemas import GenesetCreate, GeneCreate




def get_geneset(db: Session, geneset_id: int):

    return db.query(Geneset).filter(Geneset.id == geneset_id).first()

def update_geneset(db: Session, geneset_id: int, title: str, genes: List[str]):

    geneset = db.query(Geneset).filter(Geneset.id == geneset_id).first()
    geneset.title = title

    db.query(Gene).filter(Gene.geneset_id == geneset_id).delete()
    for gene in genes:
        geneset.genes.append(Gene(name=gene.name))

    db.commit()
    return geneset



def get_geneset_by_title(db: Session, pattern: str):
    return db.query(Geneset).filter(Geneset.title.like( "%" + pattern + "%")).all()


def get_genesets(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Geneset).offset(skip).limit(limit).all()


def create_geneset_with_genes(db: Session, geneset: GenesetCreate):
    db_geneset = Geneset(title=geneset.title)
    db.add(db_geneset)

    for gene in geneset.genes:
        db_geneset.genes.append(Gene(name=gene.name))

    db.commit()
    db.refresh(db_geneset)
    return db_geneset

def create_geneset(db: Session, geneset: GenesetCreate):
    db_geneset = Geneset(title=geneset.title)
    db.add(db_geneset)
    db.commit()
    db.refresh(db_geneset)
    return db_geneset



def get_genes(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Gene).offset(skip).limit(limit).all()



def create_geneset_item(db: Session, item: GeneCreate, geneset_id: int):
    db_gene = Gene(**item.dict(), geneset_id=geneset_id)
    db.add(db_gene)
    db.commit()
    db.refresh(db_gene)
    return db_gene

# addition 1 
def get_gene_by_title(db: Session,  gene_name: str):     
    gene = db.query(Gene).filter(Gene.name.like("%" + gene_name +"%")).all()
    return gene

# addition 2 

def get_gene_by_geneset_and_gene_titles(db: Session, set_name: str, gene_name: str):
    geneset = db.query(Geneset).filter(Geneset.title.like("%" + set_name)).first()    
    gene = db.query(Gene).filter((Gene.geneset_id == geneset.id) & (Gene.name.like("%" + gene_name +"%"))).all()
    return gene

# addition 3

def get_gene_set(db: Session, gene_name: str):
    genes = db.query(Gene).filter(Gene.name.like("%" + gene_name + "%")).all()
    set_names = []
    for gene in genes:
        geneset = db.query(Geneset).filter((Geneset.id == gene.geneset_id)).first()
        set_names.append(geneset.title)
    
    output = [{'gene': gene_name, 'genesets': set_names}]
    return output

# addition 4

def get_genesets_slice(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Geneset).offset(skip).limit(limit-skip).all()
