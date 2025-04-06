import re 
import unidecode


def generate_slug(text):
    vb=unidecode.unidecode(text) 
    chuthuong=vb.lower()
    bokhoangtrang=re.sub(r'\s+','-',chuthuong) 
    bohaigach=re.sub(r'-+','-',bokhoangtrang)
    kytu=re.sub(r'[^a-z0-9-]','',bohaigach)
    chuoi=kytu.strip('-')
    return chuoi