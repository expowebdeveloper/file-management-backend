from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Base, engine, SessionLocal
from app.dal.dal import create_document
from app.schema.schema import DocumentCreate

# Setup test database
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def setup_module(module):
    """Add sample data to test database."""
    db = SessionLocal()
    try:
        doc1 = DocumentCreate(name="example.txt", content="This is a test file.")
        doc2 = DocumentCreate(name="sample.txt", content="Another test file.")
        create_document(db, doc1)
        create_document(db, doc2)
        db.commit()
    finally:
        db.close()

def teardown_module(module):
    """Cleanup test database."""
    db = SessionLocal()
    try:
        db.execute("DELETE FROM documents")
        db.commit()
    finally:
        db.close()

def test_list_documents():
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert "example.txt" in [doc["name"] for doc in data["documents"]]

def test_search_documents():
    response = client.get("/api/documents?search=example")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["documents"][0]["name"] == "example.txt"

def test_sort_documents():
    response = client.get("/api/documents?sort_by=name&desc=true")
    assert response.status_code == 200
    data = response.json()
    documents = data["documents"]
    assert len(documents) > 1
    assert documents[0]["name"] > documents[1]["name"]

def test_get_document():
    # First get document id from list
    list_response = client.get("/api/documents")
    documents = list_response.json()["documents"]
    doc_id = documents[0]["id"]
    
    response = client.get(f"/api/documents/{doc_id}")
    assert response.status_code == 200
    document = response.json()
    assert document["id"] == doc_id
    assert document["name"] in ["example.txt", "sample.txt"]

def test_get_nonexistent_document():
    response = client.get("/api/documents/999")
    assert response.status_code == 404

def test_create_document():
    response = client.post(
        "/api/documents", 
        json={"name": "newdoc.txt", "content": "New document content"}
    )
    assert response.status_code == 200
    document = response.json()
    assert document["name"] == "newdoc.txt"
    assert document["size"] == len("New document content")

def test_create_duplicate_document():
    response = client.post(
        "/api/documents", 
        json={"name": "example.txt", "content": "Duplicate name"}
    )
    assert response.status_code == 400

def test_delete_document():
    # First create a document to delete
    create_response = client.post(
        "/api/documents", 
        json={"name": "to_delete.txt", "content": "Will be deleted"}
    )
    doc_id = create_response.json()["id"]
    
    # Delete the document
    response = client.delete(f"/api/documents/{doc_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Document deleted successfully"
    
    # Verify the document is removed
    get_response = client.get(f"/api/documents/{doc_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_document():
    response = client.delete("/api/documents/999")
    assert response.status_code == 404
