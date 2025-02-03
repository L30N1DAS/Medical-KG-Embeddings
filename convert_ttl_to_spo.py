# import rdflib
from rdflib import Graph, URIRef
import os
import re

import warnings

## print(rdflib.__version__)

# Load the TTL data
# ttl_dir = "ttl_dir/ImagingDaily"
# ttl_file = "output-ID-185761679-31.ttl"
ttl_dir = "output-ttl"
ttl_file = "output-PA-99472304-70.ttl"
ttl_path = os.path.join(ttl_dir, ttl_file)

# Output TSV file path
tsv_dir = "tsv_dir"
os.makedirs(tsv_dir, exist_ok=True)  # Ensure output directory exists

def strip_punctuation(string):
    string = re.sub(' ', '_', string)
    string = re.sub(r'\.','_',string)
    string = re.sub(r'%','_percent',string)
    string = re.sub(r'\(|\)','_',string)
    string = re.sub(r'\+','_',string)
    string = re.sub(r'-','_',string)
    string = re.sub(r'\[|\]','_',string)
    string = re.sub(r'\/','_',string)
    string = re.sub(r'_{2,}','_',string)
    return string

def convert_graph(ttl_path):
    # Load the TTL file into a graph
    g = Graph()

    # Reset warnings to the default behavior
    #warnings.filterwarnings("default")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ValueError)

    try:
        g.parse(ttl_path, format="ttl")

    except ValueError as e:

        if e == "ValueError: XSD Date string must contain at least two dashes":
            print("HERE")
        #print(f"UnicodeEncodeError: {e}")

    # Function to extract the local part of a URI
    def get_local_part(uri):
        if isinstance(uri, URIRef):
            uri_clean = str(uri)[str(uri).rfind("/") + 1:]

            if re.search('#', uri_clean):
                return uri_clean.split('#')[-1]
            else:
                return uri_clean
        return str(uri)

    # Open file in text mode to avoid byte encoding issues
    with open(tsv_path, "a", encoding="utf-8") as f:
    
        # Write each triple in the graph
        for subj, pred, obj in g:

            # Extract local parts of subject, predicate, and object
            subj_str = get_local_part(subj).replace("\t", " ").replace("\n", " ")
            subj_str = strip_punctuation(subj_str)
            pred_str = get_local_part(pred).replace("\t", " ").replace("\n", " ")
            pred_str = strip_punctuation(pred_str)
            obj_str = get_local_part(obj).replace("\t", " ").replace("\n", " ")
            obj_str = strip_punctuation(obj_str)

            f.write(f"{file}\t{subj_str}\t{pred_str}\t{obj_str}\n")

    print("TSV conversion complete. Data written to", tsv_path)



print('-'*200)
tsv_file = "patient_output_data.tsv"
tsv_path = os.path.join(tsv_dir, tsv_file)

# Open file in text mode to avoid byte encoding issues
with open(tsv_path, "w", encoding="utf-8") as f:
    # Write the header
    f.write("File\tSubject\tPredicate\tObject\n")
    f.close()

patient_data = os.path.join(ttl_dir, "PatientAbstract")
patient_data_list = os.listdir(patient_data)

for file in patient_data_list:
    print(file)
    ttl_path = os.path.join(patient_data, file)
    convert_graph(ttl_path)

print('-'*200)
tsv_file = "imaging_output_data.tsv"
tsv_path = os.path.join(tsv_dir, tsv_file)

# Open file in text mode to avoid byte encoding issues
with open(tsv_path, "w", encoding="utf-8") as f:
    # Write the header
    f.write("File\tSubject\tPredicate\tObject\n")
    f.close()

imaging_data = os.path.join(ttl_dir, "ImagingDaily")
imaging_data_list = os.listdir(imaging_data)

for file in imaging_data_list:
    print(file)
    ttl_path = os.path.join(imaging_data, file)
    convert_graph(ttl_path)

print('-'*200)
tsv_file = "pharmacy_output_data.tsv"
tsv_path = os.path.join(tsv_dir, tsv_file)

# Open file in text mode to avoid byte encoding issues
with open(tsv_path, "w", encoding="utf-8") as f:
    # Write the header
    f.write("File\tSubject\tPredicate\tObject\n")
    f.close()

pharmacy_data = os.path.join(ttl_dir, "PharmacyDaily")
pharmacy_data_list = os.listdir(pharmacy_data)

for file in pharmacy_data_list:
    print(file)
    ttl_path = os.path.join(pharmacy_data, file)
    convert_graph(ttl_path)


