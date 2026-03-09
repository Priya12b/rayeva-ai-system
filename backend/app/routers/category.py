from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.schemas.category_schema import CategoryRequest, CategoryResponse
from app.models.product import Product
from app.services.ai_service import generate_category_tags

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate-category", response_model=CategoryResponse)
def generate_category(data: CategoryRequest, db: Session = Depends(get_db)):
    """
    AI endpoint to auto-generate product categories and SEO tags.
    
    Takes product details and uses OpenAI to intelligently categorize
    and suggest SEO tags, then stores in database.
    """
    try:
        # Generate AI categorization
        ai_result = generate_category_tags(data.dict(), db)
        
        # Create new product in database
        new_product = Product(
            name=data.name,
            description=data.description,
            material=data.material,
            base_price=data.base_price,
            ai_primary_category=ai_result["primary_category"],
            ai_sub_category=ai_result["sub_category"],
            seo_tags=ai_result["seo_tags"],
            sustainability_filters=ai_result["sustainability_filters"]
        )
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        logger.info(f"Product created: {data.name} (ID: {new_product.id})")
        
        return ai_result
        
    except ValueError as e:
        logger.error(f"Validation error in category generation: {str(e)}")
        raise HTTPException(status_code=400, detail=f"AI response validation failed: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating category: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to generate category")