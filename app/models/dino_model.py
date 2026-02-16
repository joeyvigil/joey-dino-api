# model class helps us model data that we can use in our API. In this case, we are modeling a dinosaur with a name and a type.
# FastAPI models are based on Pydantic's BaseModel class. We can use this to create a model for our dinosaur data.
# Pydantic comes with many features, such as data validation and serialization. We can use these features to ensure that our data is in the correct format and to convert it to and from JSON when we send it over the API.
from typing import Annotated
from pydantic import BaseModel, Field

class DinoModel(BaseModel):
    id: Annotated[int, Field(gt=0)] = None # gt=0 means value must be greater than 0.  = None means that this field is optional and will be set to None if not provided.
    species: str
    period: str
    
    