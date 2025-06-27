import os
from typing import Union

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile

from old.models import (
    UPC,
    Modular,
    ModularPlan,
    ModularPlanList,
    ModularUPCLocation,
    Section,
    Shelf,
)
from old.utils import expand_facings

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload-mod")
async def upload_modular_plan(file: UploadFile, response_model=ModularPlan):
    df = pd.read_excel(file.file, engine="openpyxl")
    modular_plan = []
    df = df.replace({np.nan: None})
    for idx, row in df.iterrows():
        modular = Modular(
            id=row["modlr_plan_id"],
            category=row["modlr_catg_desc"],
            width=row["modlr_wdth_qty"],
        )
        shelf = Shelf(
            id=row["shelf_id"], height=row["shelf_height"], depth=row["shelf_depth"]
        )
        section = Section(id=row["modlr_sect_nbr_derived"])
        upc = UPC(
            id=row["upc_nbr"],
            name=row["item_name"],
            category=row["modlr_catg_desc"],
            subcategory=row["omni_subcatg_desc"],
            fineline=row["fineline_desc"],
            color=row["color_desc"],
            brand=row["brand_nm"],
            subbrand=row["subbrand_final"],
            brand_owner="SOMETHING",
            length=row["mdse_styl_depth_qty"],
            width=row["mdse_styl_wdth_qty"],
            height=row["mdse_styl_ht_qty"],
            status="ACTIVE",
        )
        modular_upc_location = ModularUPCLocation(
            modular=modular,
            shelf=shelf,
            section=section,
            modular_loc_id=row["modlr_loc_id"],
            shelf_loc_id=0,
            section_loc_id=0,
            upc=upc,
            n_width_facings=row["tot_hrznl_facing_qty"],
            n_depth_facings=row["tot_depth_facing_qty"],
            n_height_facings=row["tot_vertical_facing_qty"],
        )
        modular_plan.append(modular_upc_location)

    return ModularPlan(modular_plan=expand_facings(modular_plan))


@app.post("/upload-upc")
async def upload_upc_list(file: UploadFile):
    df = pd.read_excel(file.file, engine="openpyxl")
    for idx, row in df.iterrows():
        upc = UPC(**row.to_dict())
        print(upc)

    print(df[:3])
    return {"data": df.to_json(orient="records")}


@app.post("/upload")
async def upload_mod(file: UploadFile):
    print("incoming")
    file_ext = os.path.splitext(file.filename)[1]

    modular_plan_dict = {}
    sheets = ["before", "after"]
    for sheet in sheets:
        if file_ext == ".csv":
            # df = pd.read_csv(file.file)
            raise HTTPException(500)
        elif file_ext == ".xlsx":
            # df = pd.read_excel(file.file, engine="openpyxl")
            df = pd.read_excel(file.file, sheet_name=sheet, engine="openpyxl")
        else:
            raise HTTPException(500)
        df = df[df["shelf_id"] != 0].reset_index(drop=True)
        df = df[df["modlr_sect_nbr_derived"] != 0].reset_index(drop=True)
        # print(df[:3])
        modular_plan_dict[sheet] = df

    # return ModularPlanList(
    #     before=modular_plan_dict["before"].to_json(orient="records"),
    #     after=modular_plan_dict["after"].to_json(orient="records")
    # )
    return {
        "before": modular_plan_dict["before"].to_json(orient="records"),
        "after": modular_plan_dict["after"].to_json(orient="records"),
        }
