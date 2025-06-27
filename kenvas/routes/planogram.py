from fastapi import APIRouter, Depends, Query, Form, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
import uuid
import os
import pandas as pd
import numpy as np
import uuid
from kenvas.models.py.user import User, UserId, UserToken, UserPublic
from kenvas.models.db.user import User as UserTable
from kenvas.models.db.planogram import (
    PlanogramRun as PlanogramRunDb,
    Planogram as PlanogramDb,
    KpiBaseScorecard as KpiBaseScorecardDb,
    KpiAttrScorecard as KpiAttrScorecardDb,
    PlanogramAccess as PlanogramAccessDb,
)
from kenvas.models.py.planogram import (
    PlanogramRun as PlanogramRunPy,
    Planogram as PlanogramPy,
    KpiBaseScorecard as KpiBaseScorecardPy,
    KpiAttrScorecard as KpiAttrScorecardPy,
    PlanogramOutput as PlanogramOutputPy,
)
from kenvas.utils import auth as U
from kenvas.exceptions import auth as E, planogram as PE
from tortoise.exceptions import IntegrityError
from loguru import logger


router = APIRouter(prefix="/planogram", tags=["planogram"])


@router.post("/upload")
async def upload_planogram(
    file: UploadFile,
    user: UserTable = Depends(U.get_current_user),
    response_model=PlanogramRunPy,
):
    if isinstance(user, E.InvalidToken):
        raise E.InvalidToken()

    file_ext = os.path.splitext(file.filename)[1]

    run_id = uuid.uuid4()
    run_name = os.path.splitext(file.filename)[0]

    try:
        run_db = await PlanogramRunDb.create(
            id=str(run_id),
            name=run_name,
        )
        await PlanogramAccessDb.create(
            user_id=user.id,
            run_id=run_id,
            is_owner=True,
            can_edit=True,
        )
    except IntegrityError:
        raise PE.RunAlreadyExists()

    modular_plan_dict = {}
    xl = pd.ExcelFile(file.file)
    print(xl.sheet_names)
    
    valid_sheets = ["before", "after", "base_scorecard", "attr_scorecard"]
    available_sheets = xl.sheet_names
    
    sheets = set(available_sheets) & set(valid_sheets)

    for sheet in sheets:
        if file_ext == ".csv":
            # df = pd.read_csv(file.file)
            raise HTTPException(500)
        elif file_ext == ".xlsx":
            # df = pd.read_excel(file.file, engine="openpyxl")
            df = pd.read_excel(file.file, sheet_name=sheet, engine="openpyxl")
        else:
            raise HTTPException(500)

        modular_plan_dict[sheet] = df

        # pog_dict = {}
        if sheet in ["before", "after"]:
            # pog = []
            # df = df.fillna("")
            for idx, row in df.iterrows():
                row["run_id"] = str(run_id)
                row["version"] = sheet
                # pos = PlanogramPy(**row.to_dict())
                # pog.append(pos)
                await PlanogramDb.create(**row.to_dict())
            # pog_dict[sheet] = pog
        elif sheet in ["base_scorecard", "attr_scorecard"]:
            # scorecard = []
            df = df.replace("-", None)
            # df = df.fillna("")
            df["prefix"] = df["prefix"].fillna("")
            df["suffix"] = df["suffix"].fillna("")
            # df = df.fillna("")
            for idx, row in df.iterrows():
                row["run_id"] = run_id
                # kpi = KpiScorecardPy(**row.to_dict())
                # scorecard.append(kpi)
                if sheet == "base_scorecard":
                    await KpiBaseScorecardDb.create(**row.to_dict())
                elif sheet == "attr_scorecard":
                    await KpiAttrScorecardDb.create(**row.to_dict())
            # pog_dict[sheet] = scorecard


    return PlanogramRunPy(id=run_db.id, name=run_db.name, created_dt=run_db.created_dt)


@router.get("/all")
async def get_planograms(
    user: UserTable = Depends(U.get_current_user), response_model=list[PlanogramRunPy]
):
    if isinstance(user, E.InvalidToken):
        raise E.InvalidToken()

    try:
        run_ids = await PlanogramAccessDb.filter(user_id=user.id).values_list("run_id")
        runs = await PlanogramRunDb.filter(id__in=[id[0] for id in run_ids])
    except Exception as e:
        logger.info(e)
        raise PE.PlanogramNotFound()

    logger.info(runs)

    return runs


@router.get("/{run_id}")
async def get_planogram(
    run_id: str,
    user: UserTable = Depends(U.get_current_user),
    response_model=list[PlanogramOutputPy],
):
    if isinstance(user, E.InvalidToken):
        raise E.InvalidToken()

    try:
        run_ids = await PlanogramAccessDb.filter(user_id=user.id).values_list("run_id")
        run_ids = [id[0] for id in run_ids]
        # if run_id in run_ids:
        # run = await PlanogramRunDb.filter(id=run_id)
        planogram = await PlanogramDb.filter(run_id=run_id)

    except Exception as e:
        logger.info(e)
        raise PE.PlanogramNotFound()

    try:
        base_scorecard = await KpiBaseScorecardDb.filter(run_id=run_id)
        attr_scorecard = await KpiAttrScorecardDb.filter(run_id=run_id)
    except Exception as e:
        logger.info(e)
        raise PE.ScorecardNotFound()
    if len(planogram):
        if len(base_scorecard) and len(attr_scorecard):
            return PlanogramOutputPy(planogram=planogram, base_scorecard=base_scorecard, attr_scorecard=attr_scorecard)
        return PlanogramOutputPy(planogram=planogram)




@router.delete("/{run_id}")
async def delete_planogram(
    run_id: str,
    user: UserTable = Depends(U.get_current_user),
    response_model=list[PlanogramRunPy],
):
    if isinstance(user, E.InvalidToken):
        raise E.InvalidToken()

    try:
        result = await PlanogramAccessDb.get(user_id=user.id, run_id=run_id).values_list("is_owner")
        is_owner = result[0]
        if not is_owner:
            raise PE.RunDeleteNotAuthorized()
        
        await PlanogramAccessDb.filter(run_id=run_id).delete()
        await PlanogramDb.filter(run_id=run_id).delete()
        await KpiBaseScorecardDb.filter(run_id=run_id).delete()
        await KpiAttrScorecardDb.filter(run_id=run_id).delete()
        await PlanogramRunDb.filter(id=run_id).delete()

    except Exception as e:
        logger.info(e)
        raise PE.PlanogramNotFound()