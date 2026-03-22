from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import crud
from database import Base, get_db

app = FastAPI()

class OperationRequest(BaseModel):
    operation_type: str
    amount: float

@app.post("/wallets/{wallet_id}/operation")
async def post_wallet(wallet_id: int, request: OperationRequest,db: AsyncSession = Depends(get_db)):
    if request.operation_type not in ["DEPOSIT","WITHDRAW"]:
        raise HTTPException(status_code=400)
    
    amount = request.amount if request.operation_type == "DEPOSIT" else -request.amount

    wallet = await crud.update_balance(db, wallet_id, amount)
    if wallet is None:
        raise HTTPException(status_code=404,detail= 'Wallet not found')
    return {'wallet_id': wallet.id, 'balance': wallet.balance}

@app.get("/wallets/{wallet_id}")
async def get_wallet(wallet_id: int,db: AsyncSession = Depends(get_db)):
    wallet = await crud.get_wallet(db,wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail='Wallet not found')
    return {"wallet_id": wallet_id, 'owner': wallet.owner,"balance":wallet.balance }

@app.post('/wallets')
async def create_wallet(owner:str, db:AsyncSession=Depends(get_db)):
    wallet = await crud.create_wallet(db, owner)
    return {"wallet_id": wallet.id, "owner": wallet.owner, "balance": wallet.balance}