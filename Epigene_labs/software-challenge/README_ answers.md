# Candidature of Iana Astafeva for the position of backend developer at Epigene Labs.

# Software Challenge

## 🐍 Track Backend:

### Level 0

Make sure you can query the API. We use Postman at Epigene Labs, but feel free to use the tool you want. Create a couple of Genesets to get more familiar with it. 

###### Answering: 
I have created several gene sets in /genesets

Example: 
{"title":"genset1","id":1,"genes":[{"name":"gene1","id":1,"geneset_id":2}]}
{"title":"genset2","id":2,"genes":[{"name":"gene2","id":2,"geneset_id":3}]}
{"title":"genset3","id":3,"genes":[{"name":"gene3","id":3,"geneset_id":4}]}

Check gensets: http://localhost:8000/genesets

## Level 1

Now as a user, let's say you want to retrieve a gene based on its name, and know in which genesets it is present.  Update the API so that we can deliver that new feature.

###### Answering: 
I created a function that allows the user to find a gene based on the name of the gene. To do this:

In the main.py file I added:

### Addition 1

````
@app.get("/genesets/search/gene/gene_name", response_model=List[schemas.Gene])
'''Function that allows the user to find a gene based on the name of the gene'''
def read_match_gene( gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_title(db, gene_name)
    return gene 
````
In crud.py:

### Addition 1 
````
def get_gene_by_title(db: Session,  gene_name: str):     
    gene = db.query(Gene).filter(Gene.name.like(gene_name)).all()
    return gene    
````
## Level 2

Sometimes, users don't know the specific name of a gene. They might not be able to retrieve correctly the gene they are looking for thanks to the previous API's update in Level 1. Update the API with a way to allow a user to search for genes.

###### Answering:

In crud.py in the get_gene_by_title function, replace (gene_name) with ("%" + gene_name + "%") - this allows the user to search for a gene knowing only part of the gene name. Thus, the function should look like this:

### Addition 1 
````
def get_gene_by_title(db: Session,  gene_name: str):     
    gene = db.query(Gene).filter(Gene.name.like("%" + gene_name +"%")).all()
    return gene
````

## Level 3

Part 1:

We like to be able to search Geneset by title.Let's say you have a Geneset with title `Great Genes`, you could search and retrieve it with: 

````
127.0.0.1:8000/genesets/search/Great
````
Make sure it works as expected.

###### Answering: 

The designated python functions (read_match_genesets in main.py, get_geneset_by_title in crud.py) kept as they are because to answer Level 1 & 2, we made sure that the endpoint "/genesets/search/gene/{gene_name}" won't conflict with the endpoint of this search "/genesets/search/{pattern}" by adding the step "/gene/" to level 1 & 2 endpoint before the input argument "{gene_name}".

As for ensuring the retrieval based on part of the geneset title or from an html string, the function get_geneset_by_title in crud.py is already written to handle partial genesets titles (patterns) through the use of the pattern option of the query ("%" + pattern + "%").  

Part 2:

Now, we have thousands of users. 
Run `poetry run python populate.py` to populate the database and simulate the number of users. Let's check again the endpoint that allow a user to retrieves the full list of genesets. The output doesn't look good, and it's getting slower right ? Suggest a way to improve it.

###### Answering: 

The output doesn't look good because the function that reads all the genesets in crud.py returns by default only a slice limited to the first 100 genesets in the database and its analogous in main.py is coded not to take inputs that overwrite this default

I suggest a function that allows the user to select a slice of data

In main.py: 

### Addition 4

````
@app.get("/genesets/slice/{slice_st}-{slice_end}", response_model=List[schemas.Geneset])
'''Function that allows the user to choose the slice of data'''
def read_all_genesets_slice(slice_st: int, slice_end:int, db: Session = Depends(get_db)):
    genesets = crud.get_genesets_slice(db, skip=slice_st, limit=slice_end)
    return genesets
````

In crud.py:

### Addition 4
````
def get_genesets_slice(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Geneset).offset(skip).limit(limit-skip).all()
````

So users can choose the slice of data which they want to use.

Theoretical general suggestions for improving speed:

1. Run Python scripts on SQL Server.

2.  Batches of JSON: send JSON documents containing batches of data and parse and insert them in bulk using the OPENJSON function in SQL Server. 

3. Use the multiprocessing module, dividing the query up and sending it to multiple parallel processes, then concatenating the results. multiprocessing.Pool(processes=10)


## Level 4 - Bonus

Let's be real, this API isn't best in class. How do you think we could improve it ?
The idea here is not to implement any solution. Just think of some improvements we could discuss during the interview.

###### Answers: 

Improvement 1: A function that allows the user to find a gene based on a title of a geneset and its name

To do this in main.py:

### Addition 2

````
@app.get("/genesets/search/geneset/{geneset_title}/gene/{gene_name}", response_model=List[schemas.Gene])
'''Function that allows the user to find a gene based on the name of the gene set and the name of the gene'''
def read_match_gene(geneset_title: str, gene_name: str, db: Session = Depends(get_db)):
    gene = crud.get_gene_by_geneset_and_gene_titles(db, geneset_title, gene_name)
    return gene
````
In crud.py add:

### Addition 2 
````
def get_gene_by_geneset_and_gene_titles(db: Session, geneset_title: str, gene_name: str):
    geneset = db.query(Geneset).filter(Geneset.title.like("%" + geneset_title + "%")).first()    
    gene = db.query(Gene).filter((Gene.geneset_id == geneset.id) & (Gene.name.like("%" + gene_name +"%"))).all()
    return gene
````


Improvement 2: A function that allows the user to return the name's gene and its genesets titles based on its name

In main.py:

### Addition 3   

````
@app.get("/genesets/search/{gene_name}/genesets", response_model=List[schemas.GenesetTitle])
'''Function that allows the user return the name's of gene and it geneset based on the name of the gene'''
def read_gene_sets(gene_name: str, db: Session = Depends(get_db)):
    genesets = crud.get_gene_set(db, gene_name)
    return genesets
````
In crud.py:

### Addition 3
````
def get_gene_set(db: Session, gene_name: str):
    genes = db.query(Gene).filter(Gene.name.like("%" + gene_name + "%")).all()
    set_names = []
    for gene in genes:
        geneset = db.query(Geneset).filter((Geneset.id == gene.geneset_id)).first()
        set_names.append(geneset.title)
    
    output = [{'gene': gene_name, 'genesets': set_names}]
    return output
````    
In schemas:

### Addition 3
````
class GenesetTitle(BaseModel):
    gene: str
    genesets: List[str] = []
    
    class Config:
        orm_mode = True
        
````        
Theoretical Improvement:

1. Implement Security options (user ID, email, password)
2. Implement Cookies features to keep track of users activities 
    

