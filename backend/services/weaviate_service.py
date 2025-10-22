import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery
import os
from typing import Dict, Any, List, Optional
import json


class WeaviateService:
    def __init__(self):
        self.client = None
        self._connect()
    
    def _connect(self):
        """Connect to Weaviate instance"""
        weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
        
        try:
            if weaviate_api_key:
                self.client = weaviate.connect_to_custom(
                    http_host=weaviate_url.replace("http://", "").replace("https://", ""),
                    http_port=8080,
                    http_secure=False,
                    auth_credentials=Auth.api_key(weaviate_api_key)
                )
            else:
                self.client = weaviate.connect_to_local(
                    host=weaviate_url.replace("http://", "").replace("https://", "").split(":")[0],
                    port=8080
                )
            
            # Create schema if it doesn't exist
            self._create_schema()
        except Exception as e:
            print(f"Warning: Could not connect to Weaviate: {e}")
            self.client = None
    
    def _create_schema(self):
        """Create Weaviate schema for pharmaceutical documents"""
        if not self.client:
            return
        
        try:
            # Check if collection exists
            collections = self.client.collections.list_all()
            
            if "PharmaDocument" not in collections:
                self.client.collections.create(
                    name="PharmaDocument",
                    description="Pharmaceutical manufacturing documents",
                    properties=[
                        {
                            "name": "document_id",
                            "dataType": ["text"],
                            "description": "Unique document identifier"
                        },
                        {
                            "name": "filename",
                            "dataType": ["text"],
                            "description": "Original filename"
                        },
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "Document content chunk"
                        },
                        {
                            "name": "chunk_index",
                            "dataType": ["int"],
                            "description": "Index of this chunk in the document"
                        },
                        {
                            "name": "metadata",
                            "dataType": ["text"],
                            "description": "Additional metadata as JSON"
                        }
                    ]
                )
        except Exception as e:
            print(f"Warning: Could not create schema: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to Weaviate"""
        return self.client is not None and self.client.is_ready()
    
    async def store_document(self, document_data: Dict[str, Any]) -> bool:
        """Store processed document in Weaviate"""
        if not self.client:
            print("Warning: Weaviate not connected, skipping storage")
            return False
        
        try:
            collection = self.client.collections.get("PharmaDocument")
            
            # Store each node/chunk
            for idx, node in enumerate(document_data["nodes"]):
                collection.data.insert(
                    properties={
                        "document_id": document_data["document_id"],
                        "filename": document_data["filename"],
                        "content": node["text"],
                        "chunk_index": idx,
                        "metadata": json.dumps({
                            "entities": document_data["entities"],
                            "node_metadata": node["metadata"]
                        })
                    }
                )
            
            return True
        except Exception as e:
            print(f"Error storing document: {e}")
            return False
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by ID"""
        if not self.client:
            return self._get_mock_document(document_id)
        
        try:
            collection = self.client.collections.get("PharmaDocument")
            
            # Query for all chunks of this document
            response = collection.query.fetch_objects(
                filters={
                    "path": ["document_id"],
                    "operator": "Equal",
                    "valueText": document_id
                },
                limit=100
            )
            
            if not response.objects:
                return None
            
            # Reconstruct document
            chunks = sorted(response.objects, key=lambda x: x.properties.get("chunk_index", 0))
            full_content = "\n\n".join([chunk.properties["content"] for chunk in chunks])
            
            return {
                "document_id": document_id,
                "filename": chunks[0].properties["filename"],
                "content": full_content,
                "metadata": json.loads(chunks[0].properties.get("metadata", "{}"))
            }
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return self._get_mock_document(document_id)
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents"""
        if not self.client:
            # Fallback: Read from local uploads directory
            import os
            import hashlib
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                return []
            
            documents = []
            for filename in os.listdir(upload_dir):
                if filename.endswith('.pdf'):
                    # Generate consistent document_id
                    doc_id = hashlib.md5(filename.encode()).hexdigest()
                    documents.append({
                        "document_id": doc_id,
                        "filename": filename
                    })
            return documents
        
        try:
            collection = self.client.collections.get("PharmaDocument")
            response = collection.query.fetch_objects(limit=100)
            
            # Group by document_id and get unique documents
            documents = {}
            for obj in response.objects:
                doc_id = obj.properties["document_id"]
                if doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "filename": obj.properties["filename"]
                    }
            
            return list(documents.values())
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
    
    async def search_literature(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant literature/documents"""
        if not self.client:
            return self._get_mock_literature(query)
        
        try:
            collection = self.client.collections.get("PharmaDocument")
            
            # Perform hybrid search
            response = collection.query.hybrid(
                query=query,
                limit=limit
            )
            
            results = []
            for obj in response.objects:
                results.append({
                    "content": obj.properties["content"],
                    "document_id": obj.properties["document_id"],
                    "filename": obj.properties["filename"],
                    "score": getattr(obj.metadata, 'score', 0.0)
                })
            
            return results
        except Exception as e:
            print(f"Error searching literature: {e}")
            return self._get_mock_literature(query)
    
    def _get_mock_document(self, document_id: str) -> Dict[str, Any]:
        """Return mock document for demo purposes"""
        return {
            "document_id": document_id,
            "filename": "RMX-207-PTS.pdf",
            "content": """
            RMX-207 Manufacturing Process Technical Specification
            
            Product Overview:
            RMX-207 is an mRNA-based therapeutic vaccine utilizing lipid nanoparticle (LNP) encapsulation.
            
            Manufacturing Parameters:
            - Batch size: 10,000 vials per lot
            - Encapsulation efficiency: ≥90%
            - Purity: ≥95% by HPLC
            - LNP size: 80-120 nm
            - Polydispersity index: <0.2
            
            Quality Control:
            - Sterility testing per USP <71>
            - Endotoxin levels: <5 EU/mL
            - Identity confirmation via sequencing
            
            Sustainability Targets:
            - Ethanol recovery: ≥85%
            - CO₂ emissions: <0.5 kg per vial
            - Waste water treatment: 99% contaminant removal
            
            Cost Structure:
            - Raw materials: $45,000 per batch
            - Manufacturing: $120,000 per batch
            - QC testing: $25,000 per batch
            - Target cost: $19 per vial
            
            Timeline:
            - Tech transfer: 3 months
            - Process validation: 2 months
            - First commercial batch: Month 6
            """,
            "metadata": {
                "entities": {
                    "products": ["RMX-207"],
                    "compounds": ["mRNA", "LNP"],
                    "parameters": ["90% efficiency", "95% purity"],
                    "timelines": ["3 months", "2 months", "6 months"],
                    "costs": ["$45,000", "$120,000", "$25,000", "$19"]
                }
            }
        }
    
    def _get_mock_literature(self, query: str) -> List[Dict[str, Any]]:
        """Return mock literature for demo purposes"""
        return [
            {
                "content": "FDA Guidance for Industry: Quality Considerations for Continuous Manufacturing - This guidance describes quality considerations for pharmaceutical manufacturers using continuous manufacturing (CM).",
                "document_id": "fda-guidance-001",
                "filename": "FDA_Continuous_Manufacturing_Guidance.pdf",
                "score": 0.92
            },
            {
                "content": "Good Manufacturing Practices (GMP) for mRNA vaccines require stringent environmental controls, validated processes, and comprehensive quality testing at each stage.",
                "document_id": "gmp-mRNA-002",
                "filename": "GMP_mRNA_Vaccines.pdf",
                "score": 0.87
            },
            {
                "content": "Lipid nanoparticle formulation best practices: Microfluidic mixing has been shown to improve encapsulation efficiency by 15-20% compared to traditional bulk mixing methods.",
                "document_id": "lnp-best-practices-003",
                "filename": "LNP_Formulation_2024.pdf",
                "score": 0.83
            }
        ]
    
    def __del__(self):
        """Close Weaviate connection"""
        if self.client:
            try:
                self.client.close()
            except:
                pass

