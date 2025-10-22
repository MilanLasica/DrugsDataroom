from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pypdf import PdfReader
import uuid
from typing import Dict, Any, List
import re


class DocumentProcessor:
    def __init__(self):
        # Initialize embedding model
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    
    async def process_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Process a PDF document and extract structured information"""
        
        # Extract text from PDF
        text_content = self._extract_text_from_pdf(file_path)
        
        # Create document
        document = Document(text=text_content)
        
        # Parse into nodes (chunks)
        nodes = self.node_parser.get_nodes_from_documents([document])
        
        # Extract entities and metadata
        entities = self._extract_entities(text_content)
        
        # Generate document ID
        document_id = str(uuid.uuid4())
        
        return {
            "document_id": document_id,
            "filename": filename,
            "pages": len(text_content.split('\n\n')),
            "text_content": text_content,
            "nodes": [{"id": node.node_id, "text": node.text, "metadata": node.metadata} for node in nodes],
            "entities": entities,
            "metadata": {
                "filename": filename,
                "document_id": document_id
            }
        }
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        return text
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract key entities from document text"""
        entities = {
            "products": [],
            "compounds": [],
            "parameters": [],
            "timelines": [],
            "costs": []
        }
        
        # Simple pattern matching for common pharmaceutical terms
        # Product names (capitalized words, acronyms)
        product_pattern = r'\b[A-Z]{2,}[-]?\d+\b'
        entities["products"] = list(set(re.findall(product_pattern, text)))
        
        # Compounds (look for chemical formulas, percentages)
        compound_pattern = r'(\d+\s*%|\d+\s*mg/mL|\w+\s+\d+\s*µg)'
        entities["compounds"] = list(set(re.findall(compound_pattern, text)))
        
        # Parameters (efficiency, purity, yield mentions)
        parameter_keywords = ["efficiency", "purity", "yield", "recovery", "encapsulation"]
        entities["parameters"] = [
            line.strip() for line in text.split('\n') 
            if any(keyword in line.lower() for keyword in parameter_keywords)
        ][:10]  # Limit to 10
        
        # Timelines (date patterns, duration patterns)
        timeline_pattern = r'(\d+\s+(?:days?|weeks?|months?|years?)|\d{1,2}/\d{1,2}/\d{2,4})'
        entities["timelines"] = list(set(re.findall(timeline_pattern, text)))[:10]
        
        # Costs (dollar amounts)
        cost_pattern = r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?(?:\s?(?:million|billion|M|B))?'
        entities["costs"] = list(set(re.findall(cost_pattern, text)))
        
        return entities

