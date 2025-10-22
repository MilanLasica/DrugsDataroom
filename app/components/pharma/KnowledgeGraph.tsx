"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import * as d3 from "d3";

interface GraphData {
  nodes: Array<{ id: number; label: string; type: string; group: number }>;
  links: Array<{ source: number; target: number; value: number }>;
}

interface KnowledgeGraphProps {
  documentId: string;
}

export default function KnowledgeGraph({ documentId }: KnowledgeGraphProps) {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchGraphData();
  }, [documentId]);

  useEffect(() => {
    if (graphData && svgRef.current && containerRef.current) {
      renderGraph(graphData);
    }
  }, [graphData]);

  const fetchGraphData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/documents/${documentId}`);
      if (!response.ok) throw new Error("Failed to fetch graph data");
      const data = await response.json();
      setGraphData(data.graph_data);
    } catch (error) {
      console.error("Error fetching graph data:", error);
    } finally {
      setLoading(false);
    }
  };

  const renderGraph = (data: GraphData) => {
    if (!svgRef.current || !containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Clear existing
    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height]);

    // Color scale for groups
    const color = d3.scaleOrdinal<string>()
      .domain(["0", "1", "2", "3"])
      .range(["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"]);

    // Create force simulation
    const simulation = d3
      .forceSimulation(data.nodes as any)
      .force(
        "link",
        d3
          .forceLink(data.links)
          .id((d: any) => d.id)
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(50));

    // Add links
    const link = svg
      .append("g")
      .selectAll("line")
      .data(data.links)
      .join("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", (d) => Math.sqrt(d.value) * 2);

    // Add nodes
    const node = svg
      .append("g")
      .selectAll("g")
      .data(data.nodes)
      .join("g")
      .call(
        d3
          .drag<any, any>()
          .on("start", (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d: any) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    // Add circles to nodes
    node
      .append("circle")
      .attr("r", (d) => (d.type === "document" ? 20 : d.type === "category" ? 15 : 10))
      .attr("fill", (d) => color(String(d.group)))
      .attr("stroke", "#fff")
      .attr("stroke-width", 2);

    // Add labels to nodes
    node
      .append("text")
      .text((d) => d.label)
      .attr("x", 0)
      .attr("y", (d) => (d.type === "document" ? 30 : d.type === "category" ? 25 : 20))
      .attr("text-anchor", "middle")
      .attr("font-size", (d) => (d.type === "document" ? "14px" : d.type === "category" ? "12px" : "10px"))
      .attr("font-weight", (d) => (d.type === "category" ? "bold" : "normal"))
      .attr("fill", "currentColor");

    // Add tooltips
    node.append("title").text((d) => `${d.label}\nType: ${d.type}`);

    // Update positions on each tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });
  };

  if (loading) {
    return (
      <Card className="h-full">
        <CardContent className="flex items-center justify-center h-full">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>Knowledge Graph</CardTitle>
        <CardDescription>
          Interactive visualization showing relationships between manufacturing requirements
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 min-h-0 relative" ref={containerRef}>
        <svg ref={svgRef} className="w-full h-full" />
        <div className="absolute bottom-4 left-4 bg-card border rounded-lg p-3 text-xs space-y-1 shadow-lg text-foreground">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span className="text-foreground">Document</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-foreground">Finance</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500" />
            <span className="text-foreground">Sustainability</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-500" />
            <span className="text-foreground">Chemistry</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

