""" Contains all the data models used in inputs/outputs """

from .editable_manual import EditableManual
from .editable_manual_instructions import EditableManualInstructions
from .editable_part import EditablePart
from .editable_part_type import EditablePartType
from .editable_variant import EditableVariant
from .editable_variant_bill_of_materials import EditableVariantBillOfMaterials
from .error_message import ErrorMessage
from .game_round import GameRound
from .handle_file_upload_json_body import HandleFileUploadJsonBody
from .instruction import Instruction
from .io_link_device import IoLinkDevice
from .io_link_device_variant import IoLinkDeviceVariant
from .io_link_device_variant_device_type import IoLinkDeviceVariantDeviceType
from .io_link_master import IoLinkMaster
from .io_link_master_connected_iolink_devices import IoLinkMasterConnectedIolinkDevices
from .io_linkidentification import IoLinkidentification
from .key_performance_indicator import KeyPerformanceIndicator
from .manual import Manual
from .manual_instructions import ManualInstructions
from .order import Order
from .order_confirmation import OrderConfirmation
from .order_order_state import OrderOrderState
from .part import Part
from .part_to_pick import PartToPick
from .part_type import PartType
from .picking_mode import PickingMode
from .pole_housing import PoleHousing
from .pole_housing_pole_housing_type import PoleHousingPoleHousingType
from .priority_level import PriorityLevel
from .process_data import ProcessData
from .production_line import ProductionLine
from .shelf_balluff import ShelfBalluff
from .shelf_kardex import ShelfKardex
from .shelf_system_balluff import ShelfSystemBalluff
from .shelf_system_balluff_current_color import ShelfSystemBalluffCurrentColor
from .shelf_system_balluff_shelf_system_status import ShelfSystemBalluffShelfSystemStatus
from .shelf_system_kardex import ShelfSystemKardex
from .training import Training
from .training_analytics_data import TrainingAnalyticsData
from .training_analytics_data_event import TrainingAnalyticsDataEvent
from .training_analytics_data_order import TrainingAnalyticsDataOrder
from .value_stream_kpi_admin_settings import ValueStreamKpiAdminSettings
from .value_stream_kpi_config import ValueStreamKpiConfig
from .value_stream_kpi_config_layout_type import ValueStreamKpiConfigLayoutType
from .value_stream_kpi_definition import ValueStreamKpiDefinition
from .value_stream_kpi_definition_threshold_type import ValueStreamKpiDefinitionThresholdType
from .value_stream_kpi_definition_unit import ValueStreamKpiDefinitionUnit
from .variant import Variant
from .variant_bill_of_materials import VariantBillOfMaterials
from .variant_set import VariantSet
from .variant_set_parts import VariantSetParts
from .webhook import Webhook
from .webhook_events_item import WebhookEventsItem
from .work_process import WorkProcess
from .work_station import WorkStation
from .work_station_automation_degree import WorkStationAutomationDegree
from .work_station_work_station_status import WorkStationWorkStationStatus

__all__ = (
    "EditableManual",
    "EditableManualInstructions",
    "EditablePart",
    "EditablePartType",
    "EditableVariant",
    "EditableVariantBillOfMaterials",
    "ErrorMessage",
    "GameRound",
    "HandleFileUploadJsonBody",
    "Instruction",
    "IoLinkDevice",
    "IoLinkDeviceVariant",
    "IoLinkDeviceVariantDeviceType",
    "IoLinkidentification",
    "IoLinkMaster",
    "IoLinkMasterConnectedIolinkDevices",
    "KeyPerformanceIndicator",
    "Manual",
    "ManualInstructions",
    "Order",
    "OrderConfirmation",
    "OrderOrderState",
    "Part",
    "PartToPick",
    "PartType",
    "PickingMode",
    "PoleHousing",
    "PoleHousingPoleHousingType",
    "PriorityLevel",
    "ProcessData",
    "ProductionLine",
    "ShelfBalluff",
    "ShelfKardex",
    "ShelfSystemBalluff",
    "ShelfSystemBalluffCurrentColor",
    "ShelfSystemBalluffShelfSystemStatus",
    "ShelfSystemKardex",
    "Training",
    "TrainingAnalyticsData",
    "TrainingAnalyticsDataEvent",
    "TrainingAnalyticsDataOrder",
    "ValueStreamKpiAdminSettings",
    "ValueStreamKpiConfig",
    "ValueStreamKpiConfigLayoutType",
    "ValueStreamKpiDefinition",
    "ValueStreamKpiDefinitionThresholdType",
    "ValueStreamKpiDefinitionUnit",
    "Variant",
    "VariantBillOfMaterials",
    "VariantSet",
    "VariantSetParts",
    "Webhook",
    "WebhookEventsItem",
    "WorkProcess",
    "WorkStation",
    "WorkStationAutomationDegree",
    "WorkStationWorkStationStatus",
)
