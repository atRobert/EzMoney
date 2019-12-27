from .production import *
print(file_in_use)

try:
    from .local import *
    print('Local imported successfully.')
    print(file_in_use)
except:
    print('Error with local. Using Production.')
    print(file_in_use)
    pass
