"""Forward webhook to RetailCRM
https://cdek.retailcrm.tech/api/webhook/v1/order
"""
import httpx

async def forward(request):
    async with httpx.AsyncClient() as client:
        body = await request.body()
        response = await client.post("http://127.0.0.1/api/cdek/update", content=body)
        return response
