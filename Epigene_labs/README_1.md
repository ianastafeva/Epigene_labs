# Candidature of Iana Astafeva for the post of Beckend Developer in Epigene Labs.

# Software Challenge

## 🐍 Track Backend:

### Level 0

Make sure you can query the API. We use Postman at Epigene Labs, but feel free to use the tool you want. Create a couple of Genesets to get more familiar with it. 

I creqted the several gensets in /genesets

Example: 
{"title":"genset1","id":1,"genes":[{"name":"gene1","id":1,"geneset_id":2}]}
{"title":"genset2","id":2,"genes":[{"name":"gene2","id":2,"geneset_id":3}]}
{"title":"genset3","id":3,"genes":[{"name":"gene3","id":3,"geneset_id":4}]}

Check gensets: http://localhost:8000/genesets

### Level 1

Now as a user, let's say you want to retrieve a gene based on its name, and know in which genesets it is present.  Update the API so that we can deliver that new feature.

In main.py add:

# addition nb 1
'''Function that allows the user to find a gene based on the name of the gene'''

@app.get("/genesets/search/gene/gene_name", response_model=List[schemas.Gene])
def read_match_gene( gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_title(db, gene_name)
    return gene 

In crud.py add:

# addition 1 
def get_gene_by_title(db: Session,  gene_name: str):     
    gene = db.query(Gene).filter(Gene.name.like(gene_name)).all()
    return gene    

### Level 2

Sometimes, users don't know the specific name of a gene. They might not be able to retrieve correctly the gene they are looking for thanks to the previous API's update in Level 1. Update the API with a way to allow a user to search for genes.

In crud.py add ("%" + gene_name +"%") - which allow user to serch the gen knowing just a part of the gene's name:

# addition 1 
def get_gene_by_title(db: Session,  gene_name: str):     
    gene = db.query(Gene).filter(Gene.name.like("%" + gene_name +"%")).all()
    return gene


### Level 3

Part 1:

We like to be able to search Geneset by title.Let's say you have a Geneset with title `Great Genes`, you could search and retrieve it with: 

````
127.0.0.1:8000/genesets/search/Great
````
Make sure it works as expected.

In main.py add @app.get("/genesets/search/gene/{gene_name}", response_model=List[schemas.Gene]) - will help user to find gene base on the gene's name from html line:

# addition nb 1
'''Function that allows the user to find a gene based on the name of the gene'''

@app.get("/genesets/search/gene/{gene_name}", response_model=List[schemas.Gene])
def read_match_gene( gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_title(db, gene_name)
    return gene 

Part 2:
Now, we have thousands of users. 

Run `poetry run python populate.py` to populate the database and simulate the number of users. 

Let's check again the endpoint that allow a user to retrieves the full list of genesets. The output doesn't look good, and it's getting slower right ? Suggest a way to improve it.

Im main.py add:

# addition nb 4
'''Function that allows the user to choose the slice of data'''

@app.get("/genesets/{slice_st}-{slice_end}", response_model=List[schemas.Geneset])
def read_all_genesets(slice_st: int, slice_end:int, db: Session = Depends(get_db)):
    genesets = crud.get_genesets(db, skip=slice_st, limit=slice_end)
    return genesets

So users can choolse the slice of data which they want to use.

Theoretical general suggestions to improve the spped:

1. Run Python scripts on SQL Server.

2.  Batches of JSON: send JSON documents containing batches of data and parse and insert them in bulk using the OPENJSON function in SQL Server. 

3. Use the multiprocessing module, dividing the query up and sending it to multiple parallel processes, then concatenating the results. multiprocessing.Pool(processes=10)


### Level 4 - Bonus

Let's be real, this API isn't best in class. How do you think we could improve it ?
The idea here is not to implement any solution. Just think of some improvements we could discuss during the interview.

Improvement 1: Function that allows the user to find a gene based on the name of the gene set and the name of the gene

In main.py add:

# addition nb 2
'''Function that allows the user to find a gene based on the name of the gene set and the name of the gene'''

@app.get("/genesets/search/set/gene/{set_name}/{gene_name}", response_model=List[schemas.Gene])
def read_match_gene(set_name: str, gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_geneset_and_gene_titles(db, set_name, gene_name)
    return gene

In crud.py add:

# addition 2 

def get_gene_by_geneset_and_gene_titles(db: Session, set_name: str, gene_name: str):
    geneset = db.query(Geneset).filter(Geneset.title.like("%" + set_name)).first()    
    gene = db.query(Gene).filter((Gene.geneset_id == geneset.id) & (Gene.name == gene_name)).all()
    return gene

Improvement 2: Function that allows the user return the name's of gene and it geneset based on the name of the gene

In main.py:

# addition nb 3   
'''Function that allows the user return the name's of gene and it geneset based on the name of the gene'''

@app.get("/genesets/search/{gene_name}/genesets", response_model=List[schemas.GenesetTitle])
def read_gene_sets(gene_name: str, db: Session = Depends(get_db)):
    genesets = crud.get_gene_set(db, gene_name)
    return genesets

In crud.py:

# addition 3

def get_gene_set(db: Session, gene_name: str):
    genes = db.query(Gene).filter(Gene.name.like("%" + gene_name + "%")).all()
    set_names = []
    for gene in genes:
        geneset = db.query(Geneset).filter((Geneset.id == gene.geneset_id)).first()
        set_names.append(geneset.title)
    
    output = [{'gene': gene_name, 'genesets': set_names}]
    return output
    
In schemas:

# addition nb 3

class GenesetTitle(BaseModel):
    gene: str
    genesets: List[str] = []
    
    class Config:
        orm_mode = True
        
        
Theoretical Improvement:
    
    
