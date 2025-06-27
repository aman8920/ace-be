# from dataclasses import dataclass
# from typing import Optional

from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

from kenvas.models.db.user import User as UserTable
from kenvas.models.db import planogram as pog

PlanogramRun = pydantic_model_creator(pog.PlanogramRun)
Planogram = pydantic_model_creator(pog.Planogram, exclude=["id"])
KpiBaseScorecard = pydantic_model_creator(pog.KpiBaseScorecard, exclude=["id"])
KpiAttrScorecard = pydantic_model_creator(pog.KpiAttrScorecard, exclude=["id"])
# KpiScorecard.suffix = Field(allow_inf_nan=True)


class PlanogramOutput(BaseModel):
    planogram: list[Planogram]
    base_scorecard: Optional[list[KpiBaseScorecard]] = None
    attr_scorecard: Optional[list[KpiAttrScorecard]] = None


# Modular = pydantic_model_creator(pog.Modular)
# ModularPlan = pydantic_model_creator(pog.ModularPlan)
# ModularPlanAccess = pydantic_model_creator(pog.ModularPlanAccess)
# Item = pydantic_model_creator(pog.Item)
# ModularItemLocation = pydantic_model_creator(pog.ModularItemLocation)
# ItemBaseAttributes = pydantic_model_creator(pog.ItemBaseAttributes)
# ItemCdtAttributes = pydantic_model_creator(pog.ItemCdtAttributes)
# KpiBaseScorecard = pydantic_model_creator(pog.KpiBaseScorecard)



# @dataclass
# class Modular:
#     id: str
#     desc: str
#     width_qty: float
#     height_qty: float
#     section_cnt: int
#     shelf_cnt: int
#     category_desc: str


# @dataclass
# class ModularPlan:
#     id: str
#     desc: str
#     version: str
#     modular: Modular
#     created_dt: str
#     finger_space_qty: float


# @dataclass
# class Item:
#     id: str
#     upc_nbr: str
#     attributes: "ItemBaseAttributes"
#     cdt: "ItemCdtAttributes"
#     width_qty: float
#     height_qty: float
#     depth_qty: float
#     is_tray_item: bool
#     tray_width_qty: float
#     tray_height_qty: float
#     tray_depth_qty: float
#     hfacings_per_tray_qty: int
#     vfacings_per_tray_qty: int
#     dfacings_per_tray_qty: int
#     tray_spacers_cnt: int
#     tray_items_width_qty: float
#     tray_spacers_width_qty: float


# @dataclass
# class ItemBaseAttributes:
#     item_id: str
#     name: str
#     brand_nm: str
#     category_desc: str
#     subcategory_desc: str


# @dataclass
# class ItemCdtAttributes:
#     item_id: str
#     cdt_level_id: int
#     cdt_level_nm: str
#     cdt_level_val: str


# @dataclass
# class ModularItemLocation:
#     id: int
#     section_nbr: int
#     shelf_nbr: int
#     item: Item
#     tray_hfacings_qty: int
#     tray_vfacings_qty: int
#     tray_dfacings_qty: int
#     item_hfacings_qty: int
#     item_vfacings_qty: int
#     item_dfacings_qty: int
#     facing_height_qty: Optional[float] = None
#     shelf_height_qty: Optional[float] = None
#     air_space_qty: Optional[float] = None
#     section_height_qty: Optional[float] = None

#     def __post_init__(self):
#         if self.item_hfacings_qty and self.tray_hfacings_qty and self.item.hfacings_per_tray_qty:
#             if self.item_hfacings_qty != self.tray_hfacings_qty * self.item.hfacings_per_tray_qty:
#                 raise ValueError("Tray and Item facings out of sync!")


# @dataclass
# class Test:
#     id: int
#     text: Optional[str] = None


# if __name__ == "__main__":
#     test1 = Test(id=123, text="abc")
#     test2 = Test(id=123)
#     print(test1)
#     print(test2)
