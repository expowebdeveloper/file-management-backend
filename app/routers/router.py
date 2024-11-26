from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.services import list_documents_service, get_document_service, create_document_service, delete_document_service
from app.schema.schema import DocumentCreate, DocumentResponse, DocumentList, DocumentDeleteResponse, DocumentError
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/api/documents", response_model=DocumentList)
async def list_documents(search: Optional[str] = None, sort_by: str = "created_at", desc: bool = False, db: Session = Depends(get_db)):
    try:
        logger.info(
            f"Listing documents with search={search}, sort_by={sort_by}, desc={desc}")
        return list_documents_service(db, search, sort_by, desc)
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/documents/{id}", response_model=DocumentResponse)
async def get_document(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Getting document with id={id}")
        document = get_document_service(db, id)
        return document
    except HTTPException as he:
        logger.warning(f"Document not found: id={id}")
        raise he
    except Exception as e:
        logger.error(f"Error retrieving document {id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/documents", response_model=DocumentResponse)
async def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating new document with name={doc.name}")
        created_document = create_document_service(db, doc)
        logger.info(
            f"Successfully created document with id={created_document.id}")
        return created_document
    except ValueError as ve:
        logger.warning(f"Validation error while creating document: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/documents/{id}", response_model=DocumentDeleteResponse)
async def delete_document(id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting document with id={id}")
        deleted = delete_document_service(db, id)
        if not deleted:
            logger.warning(f"Document not found for deletion: id={id}")
            raise HTTPException(status_code=404, detail="Document not found")
        logger.info(f"Successfully deleted document with id={id}")
        return DocumentDeleteResponse(message="Document deleted successfully")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting document {id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
