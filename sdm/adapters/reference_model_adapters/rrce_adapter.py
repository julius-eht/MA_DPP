from sdm.models.sdm_reference_model import ReferenceModel, resources
from sdm.models.rrce.rrce import RrceModel, Resource
from typing import List


def transform_reference_model_to_rrce(reference_model: ReferenceModel) -> RrceModel:
    """
    Transform the reference model into the RRCE model.

    Args:
        reference_model (ReferenceModel): reference model to transform.

    Returns:
        RrceModel: transformed RRCE model.
    """

    resources = transform_resources(reference_model)
    return RrceModel(resources, [])

def transform_resources(reference_model: ReferenceModel) -> List[Resource]:
    """
    Transforms the resources of the reference model to RRCE resources.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[Resource]: transformed RRCE resources.
    """

    production_resources = []
    reference_model_production_resources = [resource for resource in reference_model.resources if resource.resource_information.production_level == "Station" and resource.resource_information.resource_type == "Manufacturing"]
    for reference_model_resource in reference_model_production_resources:
        rrce_res = create_rrce_resource(reference_model_resource, reference_model)
        if rrce_res:
            production_resources.append(rrce_res)
    return production_resources

def create_rrce_resource(reference_model_resource: resources.Resource, reference_model: ReferenceModel) -> Resource:
    """Create a RRCE resource from a reference model resource.

    Args:
        reference_model_resource (resources.Resource): reference model resource to transform.
        reference_model (ReferenceModel): reference model of production system.

    Returns:
        Resource: RRCE resource.
    """

    for resource in reference_model.resources:
        if resource.resource_configuration:
            for sub_resource in resource.resource_configuration.sub_resources:
                if sub_resource.resource_id == reference_model_resource.id_short:
                    return Resource(
                        id_short=reference_model_resource.id_short,
                        description=reference_model_resource.description,
                        production_level=reference_model_resource.resource_information.production_level,
                        resource_type=reference_model_resource.resource_information.resource_type,
                        cad_file=reference_model_resource.construction_data.cad_file,
                        position=sub_resource.position,
                        orientation=sub_resource.orientation
                    )
    return None

def update_reference_model_with_rrce_data(rrce_model: RrceModel, reference_model: ReferenceModel) -> ReferenceModel:
    """
    Update reference model with the RRCE data.

    Args:
        rrce_model (RrceModel): RRCE model.
        reference_model (ReferenceModel): reference model to update.

    Returns:
        ReferenceModel: updated reference model.
    """

    new_reference_model = update_resources(rrce_model, reference_model)
    return new_reference_model

def update_resources(rrce_model: RrceModel, reference_model: ReferenceModel) -> ReferenceModel:
    """
    Update a sdm reference model with data of the RRCE model.

    Args:
        rrce_model (RrceModel): RRCE data model to transform.
        reference_model (ReferenceModel): reference model to update.

    Returns:
        ReferenceModel: updated reference model.
    """

    rrce_resources = rrce_model.resources
    for rrce_res in rrce_resources:
        for resource in reference_model.resources:
            if resource.resource_configuration:
                for sub_resource in resource.resource_configuration.sub_resources:
                    if sub_resource.resource_id == rrce_res.id_short:
                        sub_resource.position = rrce_res.position
                        sub_resource.orientation = rrce_res.orientation
                        break
    return reference_model
