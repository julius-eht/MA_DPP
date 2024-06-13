import sys
import os
import importlib

# Print the current Python path
print("Python path:", sys.path)

# Import the module and print its path
import models.product
print("Attributes in models.product:", dir(models.product))
print("Product module path:", os.path.abspath(models.product.__file__))

# Reload the module to ensure the latest version is used
importlib.reload(models.product)

# Print the attributes after reloading
print("Attributes in models.product after reload:", dir(models.product))

# Try importing the classes again
try:
    from models.product import (
        ProcessReference,
        Product,
        ProductInformation,
        ProductUseType,
        SubProduct,
        BOM,
        TrackingData,
        ConstructionData
    )
    print("Imported ProductInformation successfully.")
except ImportError as e:
    print("ImportError:", e)
