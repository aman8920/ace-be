from typing import Optional

from pydantic import BaseModel


class UPC(BaseModel):
    id: int
    name: str
    category: str
    subcategory: str
    fineline: str
    color: Optional[str | None] = None
    brand: str
    subbrand: Optional[str | None] = None
    brand_owner: str
    length: float
    width: float
    height: float
    status: str


class ModularLocation(BaseModel):
    modular_id: int
    loc_id: int


class SectionLocation(BaseModel):
    section_id: int
    loc_id: int


class ShelfLocation(BaseModel):
    shelf_id: int
    loc_id: int


class Modular(BaseModel):
    id: int
    category: str
    width: int


class Shelf(BaseModel):
    id: int
    height: float
    depth: float


class Section(BaseModel):
    id: int


class ModularUPCLocation(BaseModel):
    modular: Modular
    shelf: Shelf
    section: Section
    modular_loc_id: int
    shelf_loc_id: int
    section_loc_id: int
    upc: UPC
    n_width_facings: int
    n_depth_facings: int
    n_height_facings: int

    # image_file: Optional[str]
    # category: str
    # modular_loc_id: int
    # section_id: int
    # section_loc_id: int
    # shelf_id: int
    # upc_id: int


class ModularPlan(BaseModel):
    modular_plan: list[ModularUPCLocation]


class ModularPlanList(BaseModel):
    before: ModularPlan
    after: ModularPlan