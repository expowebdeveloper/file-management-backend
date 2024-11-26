from sqlalchemy.orm import Session
from app.dal.dal import get_all_documents, get_document_by_id, create_document, delete_document
from app.schema.schema import DocumentCreate
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_documents_service(db: Session, search: str = None, sort_by: str = "created_at", desc: bool = False):
    try:
        logger.info(
            f"Fetching documents with search={search}, sort_by={sort_by}, desc={desc}")
        documents = get_all_documents(db, search, sort_by, desc)
        logger.info(f"Successfully retrieved {documents.total} documents")
        return documents
    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


def get_document_service(db: Session, id: int):
    try:
        logger.info(f"Fetching document with id={id}")
        document = get_document_by_id(db, id)
        if not document:
            logger.warning(f"Document not found with id={id}")
            raise HTTPException(status_code=404, detail="Document not found")
        logger.info(f"Successfully retrieved document with id={id}")
        return document
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching document {id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


def create_document_service(db: Session, doc: DocumentCreate):
    try:
        logger.info(f"Creating new document with name={doc.name}")
        document = create_document(db, doc)
        logger.info(f"Successfully created document with id={document.id}")
        return document
    except ValueError as ve:
        logger.warning(f"Validation error while creating document: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


def delete_document_service(db: Session, id: int):
    try:
        logger.info(f"Deleting document with id={id}")
        document = delete_document(db, id)
        if not document:
            logger.warning(f"Document not found for deletion: id={id}")
            raise HTTPException(status_code=404, detail="Document not found")
        logger.info(f"Successfully deleted document with id={id}")
        return {"message": "Document deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting document {id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
