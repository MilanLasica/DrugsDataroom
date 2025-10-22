from typing import Dict, Any, List
import re
import json
import os
try:
    from friendli import Friendli
    FRIENDLI_AVAILABLE = True
except ImportError:
    FRIENDLI_AVAILABLE = False
    print("Warning: friendli package not available, using mock responses")


class ExtractionService:
    def __init__(self):
        if FRIENDLI_AVAILABLE and os.getenv("FRIENDLI_TOKEN"):
            self.client = Friendli(token=os.getenv("FRIENDLI_TOKEN"))
        else:
            self.client = None
    
    async def extract_perspectives(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Extract multi-perspective insights from document"""
        
        content = document["content"]
        entities = document.get("metadata", {}).get("entities", {})
        
        # Extract Finance perspective
        finance = await self._extract_finance(content, entities)
        
        # Extract Sustainability perspective
        sustainability = await self._extract_sustainability(content, entities)
        
        # Extract Chemistry/Process perspective
        chemistry = await self._extract_chemistry(content, entities)
        
        # Generate knowledge graph data
        graph_data = self._generate_graph_data(finance, sustainability, chemistry, entities)
        
        return {
            "finance": finance,
            "sustainability": sustainability,
            "chemistry": chemistry,
            "graph_data": graph_data
        }
    
    async def _extract_finance(self, content: str, entities: Dict) -> Dict[str, Any]:
        """Extract financial insights"""
        
        prompt = f"""Analyze the following pharmaceutical manufacturing document and extract all financial information.
        Focus on: costs, pricing, payment milestones, budget allocations, supplier dependencies.
        
        Document content:
        {content[:2000]}
        
        Provide a structured JSON response with keys: total_cost, cost_breakdown, milestones, roi_considerations."""
        
        if self.client:
            try:
                response = await self._call_friendli(prompt)
                return self._parse_json_response(response)
            except Exception as e:
                print(f"Error calling FriendliAI: {e}")
        
        # Fallback: Rule-based extraction
        return {
            "total_cost": self._extract_costs(content),
            "cost_breakdown": {
                "raw_materials": self._find_pattern(content, r'raw materials?:?\s*\$?([\d,]+)'),
                "manufacturing": self._find_pattern(content, r'manufacturing:?\s*\$?([\d,]+)'),
                "qc_testing": self._find_pattern(content, r'(?:QC|testing):?\s*\$?([\d,]+)'),
            },
            "milestones": entities.get("costs", []),
            "roi_considerations": self._extract_sentences_with_keywords(content, ["cost", "price", "budget", "payment"]),
            "summary": "Financial analysis shows multi-stage investment with defined cost centers and milestone-based payments."
        }
    
    async def _extract_sustainability(self, content: str, entities: Dict) -> Dict[str, Any]:
        """Extract sustainability insights"""
        
        prompt = f"""Analyze the following pharmaceutical manufacturing document for sustainability metrics.
        Focus on: waste recovery, solvent recycling, emissions, energy use, environmental impact.
        
        Document content:
        {content[:2000]}
        
        Provide a structured JSON response with keys: waste_recovery, emissions, energy_efficiency, compliance."""
        
        if self.client:
            try:
                response = await self._call_friendli(prompt)
                return self._parse_json_response(response)
            except Exception as e:
                print(f"Error calling FriendliAI: {e}")
        
        # Fallback: Rule-based extraction
        return {
            "waste_recovery": {
                "ethanol_recovery": self._find_pattern(content, r'ethanol recovery:?\s*([\d.]+\s*%)'),
                "water_treatment": self._find_pattern(content, r'water treatment:?\s*([\d.]+\s*%)'),
            },
            "emissions": {
                "co2_per_unit": self._find_pattern(content, r'CO[₂2] emissions?:?\s*([\d.]+\s*kg)'),
            },
            "energy_efficiency": self._extract_sentences_with_keywords(content, ["energy", "power", "efficiency"]),
            "compliance": self._extract_sentences_with_keywords(content, ["environmental", "EPA", "ISO 14001", "sustainability"]),
            "summary": "Process incorporates solvent recovery systems and emission controls to minimize environmental impact."
        }
    
    async def _extract_chemistry(self, content: str, entities: Dict) -> Dict[str, Any]:
        """Extract chemistry and process insights"""
        
        prompt = f"""Analyze the following pharmaceutical manufacturing document for chemistry and process information.
        Focus on: formulation details, process parameters, quality specs, yield targets, purity requirements.
        
        Document content:
        {content[:2000]}
        
        Provide a structured JSON response with keys: formulation, process_parameters, quality_specs, critical_steps."""
        
        if self.client:
            try:
                response = await self._call_friendli(prompt)
                return self._parse_json_response(response)
            except Exception as e:
                print(f"Error calling FriendliAI: {e}")
        
        # Fallback: Rule-based extraction
        return {
            "formulation": {
                "active_ingredients": entities.get("products", []),
                "excipients": self._extract_sentences_with_keywords(content, ["excipient", "buffer", "lipid"]),
            },
            "process_parameters": {
                "batch_size": self._find_pattern(content, r'batch size:?\s*([\d,]+\s*\w+)'),
                "temperature": self._find_pattern(content, r'temperature:?\s*([\d.-]+\s*[°]?C)'),
                "pressure": self._find_pattern(content, r'pressure:?\s*([\d.]+\s*\w+)'),
                "mixing_method": self._find_pattern(content, r'mixing:?\s*(\w+)'),
            },
            "quality_specs": {
                "purity": self._find_pattern(content, r'purity:?\s*[≥>]?\s*([\d.]+\s*%)'),
                "encapsulation_efficiency": self._find_pattern(content, r'encapsulation efficiency:?\s*[≥>]?\s*([\d.]+\s*%)'),
                "particle_size": self._find_pattern(content, r'(?:particle|LNP) size:?\s*([\d-]+\s*nm)'),
            },
            "critical_steps": self._extract_sentences_with_keywords(content, ["critical", "key", "essential", "required"]),
            "summary": "Process requires high encapsulation efficiency and strict particle size control using optimized mixing conditions."
        }
    
    def _generate_graph_data(self, finance: Dict, sustainability: Dict, chemistry: Dict, entities: Dict) -> Dict[str, Any]:
        """Generate knowledge graph data for D3.js visualization"""
        
        nodes = []
        links = []
        node_id = 0
        
        # Central document node
        nodes.append({
            "id": node_id,
            "label": "Manufacturing Document",
            "type": "document",
            "group": 0
        })
        doc_node_id = node_id
        node_id += 1
        
        # Finance nodes
        finance_node_id = node_id
        nodes.append({"id": node_id, "label": "Financial", "type": "category", "group": 1})
        links.append({"source": doc_node_id, "target": node_id, "value": 2})
        node_id += 1
        
        for key in ["total_cost", "cost_breakdown"]:
            if key in finance and finance[key]:
                nodes.append({"id": node_id, "label": key.replace("_", " ").title(), "type": "metric", "group": 1})
                links.append({"source": finance_node_id, "target": node_id, "value": 1})
                node_id += 1
        
        # Sustainability nodes
        sustainability_node_id = node_id
        nodes.append({"id": node_id, "label": "Sustainability", "type": "category", "group": 2})
        links.append({"source": doc_node_id, "target": node_id, "value": 2})
        node_id += 1
        
        for key in ["waste_recovery", "emissions"]:
            if key in sustainability and sustainability[key]:
                nodes.append({"id": node_id, "label": key.replace("_", " ").title(), "type": "metric", "group": 2})
                links.append({"source": sustainability_node_id, "target": node_id, "value": 1})
                node_id += 1
        
        # Chemistry nodes
        chemistry_node_id = node_id
        nodes.append({"id": node_id, "label": "Chemistry/Process", "type": "category", "group": 3})
        links.append({"source": doc_node_id, "target": node_id, "value": 2})
        node_id += 1
        
        for key in ["formulation", "process_parameters", "quality_specs"]:
            if key in chemistry and chemistry[key]:
                nodes.append({"id": node_id, "label": key.replace("_", " ").title(), "type": "metric", "group": 3})
                links.append({"source": chemistry_node_id, "target": node_id, "value": 1})
                node_id += 1
        
        return {
            "nodes": nodes,
            "links": links
        }
    
    async def _call_friendli(self, prompt: str) -> str:
        """Call FriendliAI API"""
        if not self.client:
            return ""
        
        response = self.client.chat.completions.create(
            model="meta-llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert pharmaceutical manufacturing analyst. Provide structured, accurate analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response"""
        try:
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return {}
    
    def _extract_costs(self, content: str) -> str:
        """Extract total cost information"""
        cost_patterns = [
            r'total cost:?\s*\$?([\d,]+)',
            r'target cost:?\s*\$?([\d,]+)',
            r'estimated cost:?\s*\$?([\d,]+)'
        ]
        for pattern in cost_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return f"${match.group(1)}"
        return "Not specified"
    
    def _find_pattern(self, content: str, pattern: str) -> str:
        """Find and extract pattern from content"""
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1) if match else "Not specified"
    
    def _extract_sentences_with_keywords(self, content: str, keywords: List[str]) -> List[str]:
        """Extract sentences containing specific keywords"""
        sentences = re.split(r'[.!?]+', content)
        relevant = []
        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                relevant.append(sentence.strip())
        return relevant[:5]  # Limit to 5 sentences

