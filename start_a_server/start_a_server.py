from image_searcher.api import run

# Option 1: Through a config file
run(config_path="search_config_file.yml")

# Option 2: Through an instanciated Search object
# from image_searcher import Search

# run(searcher=Search(image_dir_path="/home/manu/perso/ImageSearcher/data/", 
#                     traverse=True, 
#                     include_faces=False))



