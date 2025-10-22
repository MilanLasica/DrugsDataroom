from typing import Dict, Any, List, Optional
import os
try:
    from friendli import Friendli
    FRIENDLI_AVAILABLE = True
except ImportError:
    FRIENDLI_AVAILABLE = False
    print("Warning: friendli package not available, using mock responses")


class ChatService:
    def __init__(self, weaviate_service):
        self.weaviate_service = weaviate_service
        
        if FRIENDLI_AVAILABLE and os.getenv("FRIENDLI_TOKEN"):
            self.client = Friendli(token=os.getenv("FRIENDLI_TOKEN"))
        else:
            self.client = None
    
    async def process_query(
        self,
        document_id: str,
        message: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Process a user query about a document"""
        
        # Retrieve document context
        document = await self.weaviate_service.get_document(document_id)
        if not document:
            return {
                "answer": "Document not found.",
                "citations": [],
                "sources": []
            }
        
        # Search for relevant context using Weaviate
        relevant_chunks = await self.weaviate_service.search_literature(message, limit=3)
        
        # Build context
        context = self._build_context(document, relevant_chunks)
        
        # Generate response
        if self.client:
            answer = await self._generate_response_with_ai(message, context, conversation_history)
        else:
            answer = self._generate_mock_response(message, context)
        
        # Extract citations
        citations = self._extract_citations(answer, relevant_chunks, document)
        
        return {
            "answer": answer,
            "citations": citations,
            "sources": [chunk.get("filename", "Unknown") for chunk in relevant_chunks]
        }
    
    def _build_context(self, document: Dict[str, Any], relevant_chunks: List[Dict[str, Any]]) -> str:
        """Build context from document and relevant chunks"""
        context = f"Document: {document['filename']}\n\n"
        context += f"Main Content:\n{document['content'][:1500]}\n\n"
        
        if relevant_chunks:
            context += "Related Information:\n"
            for i, chunk in enumerate(relevant_chunks, 1):
                context += f"{i}. {chunk['content'][:300]}...\n\n"
        
        return context
    
    async def _generate_response_with_ai(
        self,
        message: str,
        context: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Generate response using FriendliAI"""
        
        system_prompt = """You are a pharmaceutical manufacturing expert assistant. 
        Answer questions about drug manufacturing specifications, processes, and requirements.
        Always cite specific sections when providing information.
        Be precise and technical when appropriate."""
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages
            messages.append(msg)
        
        # Add current query with context
        user_message = f"""Context:\n{context}\n\nQuestion: {message}"""
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="meta-llama-3.1-70b-instruct",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return self._generate_mock_response(message, context)
    
    def _generate_mock_response(self, message: str, context: str) -> str:
        """Generate a mock response for demo purposes"""
        
        message_lower = message.lower()
        
        # Pattern matching for common queries
        if "specification" in message_lower or "spec" in message_lower:
            if "lnp" in message_lower or "formulation" in message_lower:
                return """The LNP formulation specifications for RMX-207 require:

- **Encapsulation efficiency**: ≥90%
- **Particle size**: 80-120 nm
- **Polydispersity index**: <0.2
- **Purity**: ≥95% by HPLC

These specifications ensure optimal stability and efficacy of the mRNA therapeutic. The encapsulation efficiency target is critical for protecting the mRNA payload and achieving the desired pharmacokinetic profile.

*[Source: RMX-207 PTS, Section 3.2]*"""
        
        elif "co2" in message_lower or "co₂" in message_lower or "emission" in message_lower:
            return """The CO₂ emission limit for RMX-207 manufacturing is **<0.5 kg per vial**.

This target aligns with sustainability goals and requires:
- Optimized energy usage during processing
- Solvent recovery systems (ethanol recovery ≥85%)
- Efficient HVAC systems in manufacturing suites

Meeting this target may require investment in emission monitoring equipment and process optimization.

*[Source: RMX-207 PTS, Sustainability Section]*"""
        
        elif "payment" in message_lower or "milestone" in message_lower:
            return """Payment milestones for RMX-207 manufacturing are typically structured as:

1. **Tech Transfer Completion**: 20% upon successful knowledge transfer (Month 3)
2. **Process Validation**: 30% after validation batch approval (Month 5)
3. **First Commercial Batch**: 25% upon batch release (Month 6)
4. **Ongoing Production**: 25% distributed across subsequent batches

Total estimated cost per batch:
- Raw materials: $45,000
- Manufacturing: $120,000
- QC testing: $25,000
- **Total**: $190,000 per batch (10,000 vials)

*[Source: RMX-207 PTS, Financial Terms]*"""
        
        elif "ethanol" in message_lower or "recovery" in message_lower:
            return """The ethanol recovery target is **≥85%** for RMX-207 manufacturing.

This is achieved through:
- Distillation systems post-purification
- Condensation and recirculation loops
- Monitoring of solvent purity for reuse

Benefits:
- Reduces raw material costs by ~40%
- Minimizes environmental impact
- Complies with green chemistry principles

The recovery system should be validated to ensure recovered ethanol meets quality standards for reuse in the process.

*[Source: RMX-207 PTS, Sustainability & Process Sections]*"""
        
        elif "batch" in message_lower or "size" in message_lower:
            return """The standard batch size for RMX-207 is **10,000 vials per lot**.

Manufacturing parameters:
- Fill volume: 0.5 mL per vial
- Total volume per batch: ~5 liters (accounting for overfill and losses)
- Manufacturing time: 48-72 hours per batch
- QC release time: Additional 5-7 days

Batch size was selected to:
- Optimize equipment utilization
- Meet market demand projections
- Balance cost efficiency with flexibility

*[Source: RMX-207 PTS, Manufacturing Section]*"""
        
        else:
            return f"""Based on the RMX-207 manufacturing documentation:

{context[:400]}...

To provide more specific information, please ask about:
- Formulation specifications (LNP, mRNA, excipients)
- Process parameters (batch size, temperature, mixing)
- Quality control requirements
- Sustainability targets
- Cost and payment milestones
- Timeline and deliverables

I can help you understand any aspect of the manufacturing requirements.

*[Source: RMX-207 Technical Specification]*"""
    
    def _extract_citations(
        self,
        answer: str,
        relevant_chunks: List[Dict[str, Any]],
        document: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract citations from answer and relevant chunks"""
        
        citations = []
        
        # Add main document as primary citation
        citations.append({
            "source": document["filename"],
            "content": document["content"][:200] + "...",
            "relevance": "primary"
        })
        
        # Add relevant chunks as supporting citations
        for chunk in relevant_chunks[:3]:
            citations.append({
                "source": chunk.get("filename", "Related Document"),
                "content": chunk["content"][:200] + "...",
                "relevance": "supporting",
                "score": chunk.get("score", 0.0)
            })
        
        return citations

