from typing import Optional, List

import fastapi
from database.crud import list_by_data, list_by_price, list_by_price2, list_by_date2, get_by_embeded_item
from pydantic import BaseModel
from fastapi import Depends


class OverviewUnit(BaseModel):
    hydro: Optional[bool] = None
    heat: Optional[bool] = None
    water: Optional[bool] = None

    wifi: Optional[bool] = None

    parking_min: Optional[str] = None
    parking_max: Optional[str] = None

    # ...
    agreement_min: Optional[str] = None
    agreement_max: Optional[str] = None

    move_in_date_min: Optional[str] = None
    move_in_date_max: Optional[str] = None
    # ...
    pet_friendly: Optional[bool] = None
    # ...
    size_min: Optional[int] = None
    size_max: Optional[int] = None
    # ...
    furnished: Optional[bool] = None
    laundry: Optional[bool] = None
    dishwasher: Optional[bool] = None
    fridge: Optional[bool] = None
    conditioning: Optional[bool] = None
    outdoor_space: Optional[bool] = None
    smoking: Optional[bool] = None




router = fastapi.APIRouter()


@router.get("/api/v1/")
async def read_one(price_min: int = None, price_max: int = None, date_min=None, date_max=None, overview_unit: OverviewUnit = Depends()):
    if price_min or price_max:
        data = await list_by_price2(price_min, price_max)
        return data.to_list(None)
    elif date_min or date_max:
        data = await list_by_date2(date_min, date_max)
        return data.to_list(None)
    query_dict = {}
    if overview_unit.hydro is not None:
        if overview_unit.hydro:
            query_dict["Overview.Utilities Included"] = {"$in": ["Hydro"]}
        else:
            query_dict["Overview.Utilities Included"] = {"$nin": ["Hydro"]}
    if overview_unit.heat is not None:
        if overview_unit.heat:
            elem = query_dict.get("Overview.Utilities Included", {"$in": []})
            elem['$in'] = elem.get("$in", []) + ["Heat"]
            query_dict["Overview.Utilities Included"] = elem
        else:
            elem = query_dict.get("Overview.Utilities Included", {"$nin": []})
            elem['$nin'] = elem.get("$nin", []) + ["Heat"]
            query_dict["Overview.Utilities Included"] = elem
    if overview_unit.water is not None:
        if overview_unit.water:
            elem = query_dict.get("Overview.Utilities Included", {"$in": []})
            elem['$in'] = elem.get("$in", []) + ["Water"]
            query_dict["Overview.Utilities Included"] = elem
        else:
            elem = query_dict.get("Overview.Utilities Included", {"$nin": []})
            elem['$nin'] = elem.get("$nin", []) + ["Water"]
            query_dict["Overview.Utilities Included"] = elem

    if overview_unit.wifi is not None:
        if overview_unit.wifi:
            query_dict["Overview.Wi-Fi and More"] = { "$ne" : "Not Included"}
        else:
            query_dict["Overview.Wi-Fi and More"] = { "$eq" : "Not Included"}
    

    if overview_unit.parking_min is not None:
        query_dict['Overview.Parking Included'] = { "$gte" : overview_unit.parking_min}
    
    if overview_unit.parking_max is not None:
        query_dict['Overview.Parking Included'] = query_dict.get('Overview.Parking Included', {})
        query_dict['Overview.Parking Included'].update({ "$lt" : overview_unit.parking_max})
    
    if overview_unit.agreement_min is not None:
        query_dict['Overview.Agreement Type'] = { "$gte" : overview_unit.agreement_min}
    
    if overview_unit.agreement_max is not None:
        query_dict['Overview.Agreement Type'] = query_dict.get('Overview.Parking Included', {})
        query_dict['Overview.Agreement Type'].update({ "$lt" : overview_unit.agreement_max})


    if overview_unit.size_min is not None:
        query_dict['Overview.Move-In Date'] = { "$gte" : overview_unit.move_in_date_min}
    
    if overview_unit.size_max is not None:
        query_dict['Overview.Move-In Date'] = query_dict.get('Overview.Move-In Date', {})
        query_dict['Overview.Move-In Date'].update({ "$lt" : overview_unit.move_in_date_max})


    if overview_unit.size_min is not None:
        query_dict['Overview.Size (sqft)'] = { "$gte" : overview_unit.agreement_min}
    
    if overview_unit.size_max is not None:
        query_dict['Overview.Size (sqft)'] = query_dict.get('Overview.Parking Included', {})
        query_dict['Overview.Size (sqft)'].update({ "$lt" : overview_unit.agreement_max})


    if overview_unit.pet_friendly is not None:
        if overview_unit.pet_friendly:
            query_dict["Overview.Pet Friendly"] = { "$eq" : "Yes"}
        else:
            query_dict["Overview.Pet Friendly"] = { "$ne" : "Yes"}

    if overview_unit.furnished is not None:
        if overview_unit.furnished:
            query_dict["Overview.Pet Friendly"] = { "$eq" : "Yes"}
        else:
            query_dict["Overview.Pet Friendly"] = { "$ne" : "Yes"}
    
    if overview_unit.laundry is not None:
        if overview_unit.laundry:
            elem = query_dict.get("The Unit.Appliances", {"$in": []})
            elem['$in'] = elem.get("$in", []) + ["Laundry (In Building)", "Laundry (In Unit)"]
            query_dict["The Unit.Appliances"] = elem
        else:
            elem = query_dict.get("The Unit.Appliances", {"$nin": []})
            elem['$nin'] = elem.get("$nin", []) + ["Laundry (In Building)", "Laundry (In Unit)"]
            query_dict["The Unit.Appliances"] = elem

    if overview_unit.dishwasher is not None:
        if overview_unit.dishwasher:
            elem = query_dict.get("The Unit.Appliances", {"$in": []})
            elem['$in'] = elem.get("$in", []) + ["Dishwasher"]
            query_dict["The Unit.Appliances"] = elem
        else:
            elem = query_dict.get("The Unit.Appliances", {"$nin": []})
            elem['$nin'] = elem.get("$nin", []) + ["Dishwasher"]
            query_dict["The Unit.Appliances"] = elem
    
    if overview_unit.fridge is not None:
        if overview_unit.fridge:
            elem = query_dict.get("The Unit.Appliances", {"$in": []})
            elem['$in'] = elem.get("$in", []) + ["Fridge / Freezer"]
            query_dict["The Unit.Appliances"] = elem
        else:
            elem = query_dict.get("The Unit.Appliances", {"$nin": []})
            elem['$nin'] = elem.get("$nin", []) + ["Fridge / Freezer"]
            query_dict["The Unit.Appliances"] = elem
    
    if overview_unit.conditioning is not None:
        if overview_unit.conditioning:
            query_dict["The Unit.Air Conditioning"] = { "$eq" : "Yes"}
        else:
            query_dict["The Unit.Air Conditioning"] = { "$ne" : "Yes"}
    
    if overview_unit.outdoor_space is not None:
        if overview_unit.outdoor_space:
            query_dict["The Unit.Personal Outdoor Space"] = { "$exist" : True}
        else:
            query_dict["The Unit.Personal Outdoor Space"] = { "$exist" : False}

    if overview_unit.smoking is not None:
        if overview_unit.smoking:
            query_dict["The Unit.Smoking Permitted"] = { "$eq" : "Yes"}
        else:
            query_dict["The Unit.Smoking Permitted"] = { "$ne" : "Yes"}

    return await get_by_embeded_item(query_dict)


@router.get("/api/v2/")
async def read_one(order_by_price: bool = False, order_by_date: bool = False):
    if order_by_price:
        data = await list_by_price()
        return data
    if order_by_date:
        data = await list_by_data()
        return data



