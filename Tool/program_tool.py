import httpx
import os
from prefect import flow, task

API_KEY = "kz0PVV5xAR3VO4RofsljMqADFTxGGRttaWQ6m2QJj1h8hfOuEH5KFi8msIFq8C2p"
BASE_URL = "http://iapi.dev.flexoffers.com/agents/v1"

@task
async def get_program(programId: str):

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:

        urls = [
            f"{BASE_URL}/programs/{programId}",
            f"{BASE_URL}/program/{programId}",
            f"{BASE_URL}/program?programId={programId}"
        ]

        for url in urls:
            try:
                r = await client.get(url, headers=headers)
                if r.status_code == 200:
                    return {"working_url": url, "data": r.json()}
            except:
                continue

        return {"error": "All endpoints failed", "programId": programId}
@task
async def get_payout(programId: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/programs/{programId}/payout",
            headers={"x-api-key": API_KEY}
        )
        return r.json()

@task
async def get_status():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/program/status",
            headers={"x-api-key": API_KEY}
        )
        return r.json()

@flow
async def program_flow(programId: str, action: str):
    if action == "payout":
        return await get_payout(programId)
    elif action == "status":
        return await get_status()
    else:
        return await get_program(programId)

async def program_tool(programId: str = "", action: str = "details"):
    return await program_flow(programId, action)