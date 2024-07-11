from __future__ import annotations
from typing import Optional, List
from aas2openapi.models.base import AAS, Submodel, SubmodelElementCollection

class PCFGoodsAddressHandover(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the handover address for product carbon footprint.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        Street (str): The street of the address.
        HouseNumber (str): The house number of the address.
        ZipCode (str): The zip code of the address.
        CityTown (str): The city or town of the address.
        Country (str): The country of the address.
        Latitude (float): The latitude of the address.
        Longitude (float): The longitude of the address.
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

class GeneralInformation(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe general information of SMT.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        ManufacturerName (str): Name of the manufacturer.
        ManufacturerLogo (str): Path or URL of the manufacturer's logo.
        ManufacturerProductDesignation (str): Product designation by the manufacturer.
        ManufacturerPartNumber (str): Part number assigned by the manufacturer.
        ManufacturerOrderCode (str): Order code provided by the manufacturer.
        ProductImage (str): Path or URL of the product image.
    """
    ManufacturerName: str
    ManufacturerLogo: str
    ManufacturerProductDesignation: str
    ManufacturerPartNumber: str
    ManufacturerOrderCode: str
    ProductImage: str

class ProductClassificationItem(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe a product classification item.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        ProductClassificationSystem (str): System used for classification.
        ClassificationSystemVersion (str): Version of the classification system.
        ProductClassId (str): Identifier of the product class.
    """
    ProductClassificationSystem: str
    ClassificationSystemVersion: str
    ProductClassId: str

class ProductClassifications(SubmodelElementCollection):
    """
    SubmodelElementCollection to group product classification items.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        ProductClassificationItem (List[ProductClassificationItem]): List of product classification items.
    """
    ProductClassificationItem: List[ProductClassificationItem]

class TechnicalProperties(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe technical properties.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        arbitrary_mlp str: Multi-language properties.
        arbitrary_string str: Arbitrary string properties.
        MainSection (MainSection): Main section of technical properties.
    """
    arbitrary_mlp: str
    arbitrary_string: Optional[str]


class FurtherInformation(SubmodelElementCollection):
    """
    SubmodelElementCollection to provide further information.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        TextStatement (str)): Multi-language property for text statements.
        ValidDate (str): Validity date in ISO format.
    """
    TextStatement: str
    ValidDate: str

class SMTTechnicalData(Submodel):
    """
    Submodel to describe the technical data for SMT.
    Implicit id, id_short, semantic_id, and description are used.

    Attributes:
        GeneralInformation (GeneralInformation): General information about SMT.
        ProductClassifications (ProductClassifications): Product classifications.
        TechnicalProperties (TechnicalProperties): Technical properties.
        FurtherInformation (FurtherInformation): Further information about SMT.
    """
    id: str
    GeneralInformation: GeneralInformation
    ProductClassifications: ProductClassifications
    TechnicalProperties: TechnicalProperties
    FurtherInformation: FurtherInformation

class DocumentId(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe a document identifier.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        DocumentDomainId (str): Domain identifier of the document.
        Valued (str): Valued property of the document.
        IsPrimary (Optional[str]): Indicates if this is the primary document.
    """
    DocumentDomainId: str
    Valued: str
    IsPrimary: Optional[str]

class DocumentClassification(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe document classification.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        ClassId (str): Identifier for the class.
        ClassName (str): Multi-language property for class names.
        ClassificationSystem (str): System used for classification.
    """
    ClassId: str
    ClassName: str
    ClassificationSystem: str

class DocumentVersion(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe a document version.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        Language (Optional[str]): Multi-language property for languages.
        DocumentVersionId (str): Identifier for the document version.
        Title (Optional[str]): Multi-language property for the title.
        SubTitle (Optional[str]): Multi-language property for the subtitle.
        Summary (Optional[str])): Multi-language property for the summary.
        KeyWords (Optional List[str]): Multi-language property for keywords.
        SetDate (Optional[str]): Date when the document was set.
        StatusValue (Optional[str]): Status of the document.
        OrganizationName (Optional[str]): Name of the organization.
        OrganizationOfficialName (Optional[str]): Official name of the organization.
        DigitalFile (Optional[str]): Path or URL of the digital file.
        PreviewFile (Optional[str]): Path or URL of the preview file.
        RefersTo (Optional[str]): Reference element.
        BasedOn (Optional[str]): Reference element.
        TranslationOf (Optional[str]): Reference element.
    """
    Language: List[str]
    DocumentVersionId: str
    Title: str
    SubTitle: Optional[str]
    Summary: Optional[str]
    KeyWords: Optional[List[str]]
    SetDate: Optional[str]
    StatusValue: Optional[str]
    OrganizationName: Optional[str]
    OrganizationOfficialName: Optional[str]
    DigitalFile: Optional[str]
    PreviewFile: Optional[str]
    RefersTo: Optional[str]
    BasedOn: Optional[str]
    TranslationOf: Optional[str]

class Document(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe a document.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        DocumentEntity (List[str]): List of reference elements.
        DocumentId (List[DocumentId]): List of document identifiers.
        DocumentClassification (List[DocumentClassification]): List of document classifications.
        DocumentVersion (List[DocumentVersion]): List of document versions.
    """
    DocumentEntity: List[str]
    DocumentId: List[DocumentId]
    DocumentClassification: List[DocumentClassification]
    DocumentVersion: List[DocumentVersion]

class HandoverDocumentation(Submodel):
    """
    Submodel to describe the handover documentation.
    Implicit id, id_short, semantic_id, and description are used.

    Attributes:
        Entity (List[str]): List of reference elements.
        Document (List[Document]): List of documents.
    """
    id: str
    Entity: List[str]
    Document: List[Document]

class OperatingConditionsOfReliabilityCharacteristics(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe the operating conditions of reliability characteristics.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        TypeOfVoltage (Optional[str]): Type of voltage.
        RatedVoltage (Optional[float]): Rated voltage.
        MinimumRatedVoltage (Optional[float]): Minimum rated voltage.
        MaximumRatedVoltage (Optional[float]): Maximum rated voltage.
        RatedOperationalCurrent (Optional[float]): Rated operational current.
        OtherOperatingConditions (Optional[str]): Other operating conditions.
        UsefulLifeInNumberOfOperations (Optional[int]): Useful life in number of operations.
        UsefulLifeInTimeInterval (Optional[float]): Useful life in time interval.
    """
    TypeOfVoltage: Optional[str]
    RatedVoltage: Optional[float]
    MinimumRatedVoltage: Optional[float]
    MaximumRatedVoltage: Optional[float]
    RatedOperationalCurrent: Optional[float]
    OtherOperatingConditions: Optional[str]
    UsefulLifeInNumberOfOperations: Optional[int]
    UsefulLifeInTimeInterval: Optional[float]

class ReliabilityCharacteristics(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe reliability characteristics.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        MTTF (Optional[int]): Mean Time To Failure.
        MTBF (Optional[int]): Mean Time Between Failures.
        B10 (Optional[int]): B10 life parameter.
    """
    MTTF: Optional[int]
    MTBF: Optional[int]
    B10: Optional[int]

class Reliability(Submodel):
    """
    Submodel to describe the reliability of a product.
    Implicit id, id_short, semantic_id, and description are used.

    Attributes:
        NumberOfReliabilitySets (int): Number of reliability sets.
        OperatingConditionsOfReliabilityCharacteristics (Optional[List[OperatingConditionsOfReliabilityCharacteristics]]): Operating conditions of reliability characteristics.
        ReliabilityCharacteristics (Optional[List[ReliabilityCharacteristics]]): Reliability characteristics.
    """
    id: str
    NumberOfReliabilitySets: int
    OperatingConditionsOfReliabilityCharacteristics: Optional[List[OperatingConditionsOfReliabilityCharacteristics]]
    ReliabilityCharacteristics: Optional[List[ReliabilityCharacteristics]]

class SubProduct(SubmodelElementCollection):
    """
    SubmodelElementCollection to describe a subproduct of a product.
    Implicit id_short, semantic_id, and description are used.

    Attributes:
        product_type (str): The type of the subproduct.
        passport_id (str): The AAS reference of the subproduct passport.
        product_use_type (str): Defines the Product use type.
        quantity (int): The quantity of the subproduct(s).
    """
    product_type: str
    passport_id: str
    product_use_type: str
    quantity: int

class BOM(Submodel):
    """
    Submodel to describe the bill of materials of a product.
    Implicit id, id_short, semantic_id, and description are used.

    Attributes:
        sub_product_count (Optional[int]): The total number of subproducts (depth 1).
        sub_products (Optional[List[SubProduct]]): The list of subproducts contained in the product (depth 1).
    """
    id: str
    sub_product_count: Optional[int]
    sub_products: Optional[List[SubProduct]]

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
    Submodel to describe the carbon footprint of a product.
    Implicit id, id_short, semantic_id, and description are used.

    Attributes:
        description (Optional[str]): The description of the carbon footprint.
        PCFGoodsAddressHandover (Optional[PCFGoodsAddressHandover]): The handover address for product carbon footprint.
        TCFGoodsTransportAddressTakeover (Optional[TCFGoodsTransportAddressTakeover]): The takeover address for transport carbon footprint.
    """
    product_footprints: Optional[List[ProductCarbonFootprint]]
    transport_footprints: Optional[List[TransportCarbonFootprint]]

class Passport(AAS):
    """
    AAS to describe a product through its product passport.
    Implicit id, id_short, semantic_id, and description are used.

    Attributes:
        carbon_footprint (Optional[CarbonFootprint]): The carbon footprint data of the product.
        bom (Optional[BOM]): The bill of materials.
        smt_technical_data (Optional[SMTTechnicalData]): The technical data for SMT.
        handover_documentation (Optional[HandoverDocumentation]): The handover documentation.
        reliability (Optional[Reliability]): The reliability of the product.
    """
    carbon_footprint: Optional[CarbonFootprint]
    bom: Optional[BOM]
    smt_technical_data: Optional[SMTTechnicalData]
    handover_documentation: Optional[HandoverDocumentation]
    reliability: Optional[Reliability]
