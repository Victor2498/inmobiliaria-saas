from datetime import date
from dateutil.relativedelta import relativedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Contract, MonthlyCharge

class ContractService:
    @staticmethod
    async def create_contract(session: AsyncSession, contract_data: Contract) -> Contract:
        # 1. Save Contract
        session.add(contract_data)
        await session.flush() # Get ID
        
        # 2. Generate Monthly Charges
        # Logic: Iterate from start_date to end_date
        current_date = contract_data.start_date
        end_date = contract_data.end_date
        
        charges = []
        
        while current_date <= end_date:
            # Calculate due date (e.g., 5th or 10th of the month)
            # If billing_day is 10, then due date is 10th of current_date's month
            # Note: Need to handle invalid days (e.g. 31st in Feb)
            try:
                due_date = current_date.replace(day=contract_data.billing_day)
            except ValueError:
                # Fallback to last day of month if day is invalid
                last_day = (current_date + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)
                due_date = last_day

            charge = MonthlyCharge(
                contract_id=contract_data.id,
                month=current_date.month,
                year=current_date.year,
                due_date=due_date,
                rent_amount=contract_data.initial_amount, # Can be adjusted by index rules later
                total_amount=contract_data.initial_amount,
                balance_due=contract_data.initial_amount
            )
            session.add(charge)
            
            # Move to next month
            current_date += relativedelta(months=1)
            
        return contract_data
