from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.schemas.proposal_schema import ProposalRequest, ProposalResponse
from app.models.product import Product
from app.models.proposal import Proposal
from app.services.ai_service import generate_proposal

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate-proposal", response_model=ProposalResponse)
def generate_proposal_endpoint(data: ProposalRequest, db: Session = Depends(get_db)):
    """
    AI endpoint to generate intelligent B2B proposals.
    
    Takes client type, budget, and sustainability priority to generate
    optimized product recommendations using AI.
    """
    try:
        # Get all available products
        products = db.query(Product).all()
        
        if not products:
            return {
                "recommended_products": [],
                "total_cost": 0,
                "budget_remaining": data.budget,
                "impact_positioning_summary": "No products available in catalog."
            }
        
        # Generate AI-powered proposal
        proposal_result = generate_proposal(
            client_type=data.client_type,
            budget=data.budget,
            sustainability_priority=data.sustainability_priority,
            products=products,
            db=db
        )
        
        # Store proposal in database
        new_proposal = Proposal(
            client_type=data.client_type,
            budget=data.budget,
            proposal_json=proposal_result
        )
        
        db.add(new_proposal)
        db.commit()
        
        logger.info(f"Proposal generated for {data.client_type}: {len(proposal_result['recommended_products'])} products")
        
        return proposal_result
        
    except ValueError as e:
        logger.error(f"Validation error in proposal generation: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Proposal generation failed: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating proposal: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to generate proposal")
