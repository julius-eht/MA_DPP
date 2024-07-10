from __future__ import annotations
from enum import Enum

from typing import Optional, List, Union, Literal
from click import Option

from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection

class PCFGoodsAddressHandover(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the handover address for product carbon footprint.

    Args:
        description (Optional[str]): The description of the address.
        id_short (Optional[str]): The short id of the address.
        semantic_id (Optional[str]): The semantic id of the address.
        street (str): The street of the address.
        house_number (str): The house number of the address.
        zip_code (str): The zip code of the address.
        city_town (str): The city or town of the address.
        country (str): The country of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """
    Street: str
    HouseNumber: str
    ZipCode: str
    CityTown: str
    Country: str
    Latitude: float
    Longitude: float

class TCFGoodsTransportAddressTakeover(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the takeover address for transport carbon footprint.

    Args:
        description (Optional[str]): The description of the address.
        id_short (Optional[str]): The short id of the address.
        semantic_id (Optional[str]): The semantic id of the address.
        street (str): The street of the address.
        house_number (str): The house number of the address.
        zip_code (str): The zip code of the address.
        city_town (str): The city or town of the address.
        country (str): The country of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """
    Street: str
    HouseNumber: str
    ZipCode: str
    CityTown: str
    Country: str
    Latitude: float
    Longitude: float

class TCFGoodsTransportAddressHandover(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the handover address for transport carbon footprint.

    Args:
        description (Optional[str]): The description of the address.
        id_short (Optional[str]): The short id of the address.
        semantic_id (Optional[str]): The semantic id of the address.
        street (str): The street of the address.
        house_number (str): The house number of the address.
        zip_code (str): The zip code of the address.
        city_town (str): The city or town of the address.
        country (str): The country of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """
    Street: str
    HouseNumber: str
    ZipCode: str
    CityTown: str
    Country: str
    Latitude: float
    Longitude: float

class ProductCarbonFootprint(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the carbon footprint of a product.

    Args:
        description (Optional[str]): The description of the product carbon footprint.
        id_short (Optional[str]): The short id of the product carbon footprint.
        semantic_id (Optional[str]): The semantic id of the product carbon footprint.
        PCFCalculationMethod (str): The calculation method used.
        PCFCO2eq (float): The CO2 equivalent value.
        PCFReferenceValueForCalculation (Optional[str]): The reference value for calculation.
        PCFQuantityOfMeasureForCalculation (Optional[float]): The quantity of measure for calculation.
        PCFLifeCyclePhase (Optional[str]): The life cycle phase.
        PCFGoodsAddressHandover (Optional[PCFGoodsAddressHandover]): The handover address.
    """
    PCFCalculationMethod: str
    PCFCO2eq: float
    PCFReferenceValueForCalculation: Optional[str]
    PCFQuantityOfMeasureForCalculation: Optional[float]
    PCFLifeCyclePhase: Optional[str]
    PCFGoodsAddressHandover: Optional[PCFGoodsAddressHandover]

class TransportCarbonFootprint(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the carbon footprint of transport.

    Args:
        description (Optional[str]): The description of the transport carbon footprint.
        id_short (Optional[str]): The short id of the transport carbon footprint.
        semantic_id (Optional[str]): The semantic id of the transport carbon footprint.
        TCFCalculationMethod (str): The calculation method used.
        TCFCO2eq (float): The CO2 equivalent value.
        TCFReferenceValueForCalculation (Optional[str]): The reference value for calculation.
        TCFQuantityOfMeasureForCalculation (Optional[float]): The quantity of measure for calculation.
        TCFProcessesForGreenhouseGasEmissionInATransportService (Optional[str]): The processes for greenhouse gas emission.
        TCFGoodsTransportAddressTakeover (Optional[TCFGoodsTransportAddressTakeover]): The takeover address.
        TCFGoodsTransportAddressHandover (Optional[TCFGoodsTransportAddressHandover]): The handover address.
    """
    TCFCalculationMethod: str
    TCFCO2eq: float
    TCFReferenceValueForCalculation: Optional[str]
    TCFQuantityOfMeasureForCalculation: Optional[float]
    TCFProcessesForGreenhouseGasEmissionInATransportService: Optional[str]
    TCFGoodsTransportAddressTakeover: Optional[TCFGoodsTransportAddressTakeover]
    TCFGoodsTransportAddressHandover: Optional[TCFGoodsTransportAddressHandover]

class CarbonFootprint(Submodel):
    """
    Submodel to describe the carbon footprint data of a product.

    Args:
        description (Optional[str]): The description of the carbon footprint submodel.
        id_short (Optional[str]): The short id of the carbon footprint submodel.
        semantic_id (Optional[str]): The semantic id of the carbon footprint submodel.
        product_footprint (Optional[List[ProductCarbonFootprint]]): The product carbon footprint data.
        transport_footprint (Optional[List[TransportCarbonFootprint]]): The transport carbon footprint data.
    """
    product_footprints: Optional[List[ProductCarbonFootprint]]
    transport_footprints: Optional[List[TransportCarbonFootprint]]

class ProductUseType(str, Enum):
    """
    Enum to describe how a subproduct is used in the product.
    """
    ASSEMBLED = "assembled"
    UNASSEMBLED = "unassembled"
    CONSUMED = "consumed"


class SubProduct(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe a subproduct of a product with reference to its AAS, status information and quantity.

    Args:
        description (Optional[str]): The description of the subproduct.
        id_short (Optional[str]): The short id of the subproduct.
        semantic_id (Optional[str]): The semantic id of the subproduct.
        product_type (str): The type of the subproduct.
        passport_id (str): The AAS reference of the subproduct passport.
        product_use_type (ProductUseType): Defines the Product use type
        quantity (int): The quantity of the subproduct(s).
    """
    product_type: str
    passport_id: str
    product_use_type: ProductUseType
    quantity: int

class BOM(Submodel):
    """
    Submodel to describe the bill of materials of a product.

    Args:
        id (str): The id of the bill of materials.
        description (Optional[str]): The description of the bill of materials.
        id_short (Optional[str]): The short id of the bill of materials.
        semantic_id (Optional[str]): The semantic id of the bill of materials.
        sub_product_count (Optional[int]): The total number of subproducts (depht 1)
        sub_products (Optional[List[SubmodelElementCollection]]): The list of subproducts contained in the product (depht 1)
    """
    sub_product_count: Optional[int]
    sub_products: Optional[List[SubProduct]]

class Passport(AAS):
    """
    AAS to describe a product through its product passport.

    Args:
        id (str): The id of the productpassport.
        description (Optional[str]): The description of the product.
        id_short (Optional[str]): The short id of the passport.
        semantic_id (Optional[str]): The semantic id of the passport.
        carbon_footprint (Optional[CarbonFootprint]): The carbon footprint data of the product.
    """
    carbon_footprint: Optional[CarbonFootprint]
    bom: Optional[BOM]
    # TBD Add other compartments
