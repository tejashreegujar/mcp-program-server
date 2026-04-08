import httpx
import os

# ✅ Load from environment (SAFE)
API_KEY ="kz0PVV5xAR3VO4RofsljMqADFTxGGRttaWQ6m2QJj1h8hfOuEH5KFi8msIFq8C2p"

BASE_URL = "http://iapi.dev.flexoffers.com/agents/v1/programs"


async def get_program_details(programId: str):
    """
    Fetch program details from FlexOffers API
    """

    # 🔐 Validate API key
    if not API_KEY:
        return {
            "error": "API_KEY missing. Check your .env file.",
            "programId": programId
        }

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(
                f"{BASE_URL}/{programId}",
                headers=headers
            )

            response.raise_for_status()
            data = response.json()

            # ✅ Clean structured response
            return {
                "success": True,
                "programId": programId,
                "data": data
            }

        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}",
                "details": e.response.text,
                "programId": programId
            }

        except httpx.RequestError as e:
            return {
                "success": False,
                "error": "Connection failed",
                "details": str(e),
                "programId": programId
            }

        except Exception as e:
            return {
                "success": False,
                "error": "Unexpected error",
                "details": str(e),
                "programId": programId
            }