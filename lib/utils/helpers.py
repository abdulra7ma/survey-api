from ..exceptions.core import ObjectQueryIdNotFound, NotIntegerType, ObjectNotFound


def get_query_id(query_params, model_name: str = "Object"):
    """Get the an Object id from the query params"""

    object_id: None

    if "id" not in query_params:
        raise ObjectQueryIdNotFound(
            detail=f"{model_name} id not specified in the query params",
            code=f"{model_name.lower()}_query_id_not_found",
        )

    if query_params["id"] == "":
        raise ObjectQueryIdNotFound(
            detail=f"{model_name} id not specified in the query params",
            code=f"{model_name.lower()}_query_id_not_found",
        )

    try:
        object_id = int(query_params["id"])
    except ValueError:
        raise NotIntegerType(
            detail=f"{model_name} id must be in an integer form"
        )

    return object_id

def get_model_object(model, id):
    """Get the model Object with given id else raise ObjectNotFound exception"""

    try:
        return model.objects.get(id=id)
    except model.DoesNotExist:
        model_name = model.__name__
        raise ObjectNotFound(
            detail=f"{model_name} Not Found",
            code=f"{model_name.lower()}_not_found",
        )
