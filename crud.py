from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Wallet

async def get_wallet(db: AsyncSession, wallet_id: int):
    result = await db.execute(select(Wallet).filter(Wallet.id == wallet_id))
    return result.scalar_one_or_none()

async def create_wallet(db: AsyncSession, owner: str):
    wallet = Wallet(owner=owner, balance=0)
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

async def update_balance(db: AsyncSession, wallet_id: int, amount: float):
    result = await db.execute(select(Wallet).filter(Wallet.id == wallet_id).with_for_update())
    wallet = result.scalar_one_or_none()
    if wallet:
        wallet.balance += amount
        await db.commit()
        await db.refresh(wallet)
    return wallet