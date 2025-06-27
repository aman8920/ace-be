from tortoise.models import Model
from tortoise import fields, run_async, Tortoise

from kenvas.utils.database import DB_URI


# class Modular(Model):
#     id = fields.UUIDField(pk=True)
#     desc = fields.CharField(max_length=100)
#     width_qty = fields.FloatField()
#     height_qty = fields.FloatField()
#     section_cnt = fields.IntField()
#     shelf_cnt = fields.IntField()
#     category_desc = fields.CharField(max_length=100)

#     class Meta:
#         table = "modular"


# class ModularPlan(Model):
#     id = fields.UUIDField(pk=True)
#     desc = fields.TextField(max_length=500)
#     version = fields.CharField(max_length=50)
#     modular = fields.ForeignKeyField(model_name="models.Modular", to_field="id")
#     created_dt = fields.DatetimeField(auto_now_add=True)
#     finger_space_qty = fields.FloatField(null=True)

#     class Meta:
#         table = "modular_plan"


# class Item(Model):
#     id = fields.UUIDField(pk=True)
#     upc_nbr = fields.CharField(max_length=13, unique=True)
#     # base_attrs = fields.ForeignKeyField(model_name="")
#     # cdt_attrs: "ItemCdtAttributes"
#     width_qty = fields.FloatField()
#     height_qty = fields.FloatField()
#     depth_qty = fields.FloatField()
#     is_tray_item = fields.BooleanField()
#     tray_width_qty = fields.FloatField()
#     tray_height_qty = fields.FloatField()
#     tray_depth_qty = fields.FloatField()
#     hfacings_per_tray_qty = fields.IntField()
#     vfacings_per_tray_qty = fields.IntField()
#     dfacings_per_tray_qty = fields.IntField()
#     tray_spacers_cnt = fields.IntField()
#     tray_items_width_qty = fields.FloatField()
#     tray_spacers_width_qty = fields.FloatField()

#     class Meta:
#         table = "item"


# class ItemBaseAttributes(Model):
#     item = fields.OneToOneField(
#         model_name="models.Item", to_field="id", related_name="base_attrs"
#     )
#     name = fields.CharField(max_length=100)
#     brand_nm = fields.CharField(max_length=50)
#     category_desc = fields.CharField(max_length=50)
#     subcategory_desc = fields.CharField(max_length=50)

#     class Meta:
#         table = "item_base_attributes"


# class ItemCdtAttributes(Model):
#     item = fields.OneToOneField(
#         model_name="models.Item", to_field="upc_nbr", related_name="cdt_attrs"
#     )
#     cdt_1 = fields.CharField(max_length=100)
#     cdt_2 = fields.CharField(max_length=100)
#     cdt_3 = fields.CharField(max_length=100)
#     cdt_4 = fields.CharField(max_length=100)
#     cdt_5 = fields.CharField(max_length=100)
#     cdt_6 = fields.CharField(max_length=100)
#     cdt_7 = fields.CharField(max_length=100)

#     class Meta:
#         table = "item_cdt_attributes"


# class ModularItemLocation(Model):
#     modular = fields.ForeignKeyField(model_name="models.Modular", to_field="id")
#     idx = fields.IntField()
#     section_nbr = fields.IntField()
#     shelf_nbr = fields.IntField()
#     item = fields.ForeignKeyField(model_name="models.Item", to_field="id")
#     tray_hfacings_qty = fields.IntField()
#     tray_vfacings_qty = fields.IntField()
#     tray_dfacings_qty = fields.IntField()
#     item_hfacings_qty = fields.IntField()
#     item_vfacings_qty = fields.IntField()
#     item_dfacings_qty = fields.IntField()
#     facing_height_qty = fields.FloatField()
#     shelf_height_qty = fields.FloatField()
#     air_space_qty = fields.FloatField()
#     section_height_qty = fields.FloatField()

#     class Meta:
#         table = "modular_item_location"


# class KpiBaseScorecard(Model):
#     modular_plan = fields.ForeignKeyField(
#         model_name="models.ModularPlan", to_field="id", related_name="base_kpis"
#     )
#     name = fields.CharField(max_length=100)
#     category = fields.CharField(max_length=50)
#     prefix = fields.CharField(max_length=10)
#     suffix = fields.CharField(max_length=10)
#     before = fields.FloatField()
#     after = fields.FloatField()
#     lift = fields.FloatField()
#     pct_lift = fields.FloatField()

#     class Meta:
#         table = "kpi_base_scorecard"


# class ModularPlanAccess(Model):
#     user = fields.ForeignKeyField(
#         model_name="models.User", to_field="id", related_name="modular_plans"
#     )
#     modular_plan = fields.ForeignKeyField(
#         model_name="models.ModularPlan", to_field="id", related_name="users"
#     )
#     is_owner = fields.BooleanField()
#     can_edit = fields.BooleanField()
#     created_dt = fields.DatetimeField(auto_now_add=True)
#     modified_dt = fields.DatetimeField(auto_now=True)

#     class Meta:
#         table = "modular_plan_access"


from enum import StrEnum


class ModularVersionEnum(StrEnum):
    BEFORE = "before"
    AFTER = "after"


class PlanogramRun(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    created_dt = fields.DatetimeField(auto_now_add=True)


class Planogram(Model):
    run = fields.ForeignKeyField(model_name="models.PlanogramRun", to_field="id", related_name="planogram_items")
    version = fields.CharEnumField(
        max_length=10, enum_type=ModularVersionEnum, null=True
    )
    upc_nbr = fields.BigIntField()
    modular_plan_id = fields.CharField(max_length=100)
    cdt_1 = fields.CharField(max_length=100)
    cdt_2 = fields.CharField(max_length=100)
    cdt_3 = fields.CharField(max_length=100)
    cdt_4 = fields.CharField(max_length=100)
    cdt_5 = fields.CharField(max_length=100)
    cdt_6 = fields.CharField(max_length=100)
    cdt_7 = fields.CharField(max_length=100)
    brand_nm = fields.CharField(max_length=100)
    subcategory_desc = fields.CharField(max_length=100)
    fineline_desc = fields.CharField(max_length=100)
    item_desc = fields.CharField(max_length=100)
    modular_section_cnt = fields.IntField()
    section_width_qty = fields.FloatField()
    modular_width_qty = fields.FloatField()
    modular_height_qty = fields.FloatField()
    section_nbr = fields.IntField()
    shelf_nbr = fields.IntField()
    modular_loc_id = fields.IntField()
    is_tray_item = fields.BooleanField()
    tot_item_hfacings_qty = fields.FloatField(null=True)
    tot_item_vfacings_qty = fields.FloatField(null=True)
    tot_tray_hfacings_qty = fields.FloatField(null=True)
    tot_tray_vfacings_qty = fields.FloatField(null=True)
    tray_item_hfacings_qty = fields.FloatField(null=True)
    tray_item_vfacings_qty = fields.FloatField(null=True)
    tray_width_qty = fields.FloatField(null=True)
    tray_height_qty = fields.FloatField(null=True)
    item_width_adj_qty = fields.FloatField()
    item_height_adj_qty = fields.FloatField()
    tray_items_width_qty = fields.FloatField(null=True)
    tray_spacers_width_qty = fields.FloatField(null=True)
    tray_spacers_cnt = fields.IntField(null=True)
    tray_spacer_width_qty = fields.FloatField(null=True)
    facing_height_qty = fields.FloatField()
    shelf_height_qty = fields.FloatField()
    section_height_qty = fields.FloatField()
    section_shelf_cnt = fields.IntField()
    air_space_qty = fields.FloatField()
    finger_space_qty = fields.FloatField()


class PlanogramAccess(Model):
    user = fields.ForeignKeyField(
        model_name="models.User", to_field="id", related_name="planograms"
    )
    run_id = fields.CharField(max_length=50)
    is_owner = fields.BooleanField()
    can_edit = fields.BooleanField()
    created_dt = fields.DatetimeField(auto_now_add=True)
    modified_dt = fields.DatetimeField(auto_now=True)

    # class Meta:
    #     table = "modular_plan_access"


class KpiBaseScorecard(Model):
    run = fields.ForeignKeyField(model_name="models.PlanogramRun", to_field="id", related_name="base_scorecard_kpis")
    kpi = fields.CharField(max_length=100)
    category = fields.CharField(max_length=50)
    prefix = fields.CharField(max_length=10, null=True)
    suffix = fields.CharField(max_length=10, null=True)
    before = fields.FloatField(null=True)
    after = fields.FloatField(null=True)
    lift = fields.FloatField(null=True)
    pct_lift = fields.FloatField(null=True)


class KpiAttrScorecard(Model):
    run = fields.ForeignKeyField(model_name="models.PlanogramRun", to_field="id", related_name="attr_scorecard_kpis")
    attr_nm = fields.CharField(max_length=10)
    attr_val = fields.CharField(max_length=50)
    kpi = fields.CharField(max_length=100)
    # category = fields.CharField(max_length=50)
    prefix = fields.CharField(max_length=10, null=True)
    suffix = fields.CharField(max_length=10, null=True)
    before = fields.FloatField(null=True)
    after = fields.FloatField(null=True)
    lift = fields.FloatField(null=True)
    pct_lift = fields.FloatField(null=True)
