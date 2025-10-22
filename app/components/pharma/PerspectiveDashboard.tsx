"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Loader2, DollarSign, Leaf, Beaker, TrendingUp } from "lucide-react";

interface PerspectiveData {
  finance: any;
  sustainability: any;
  chemistry: any;
  graph_data: any;
}

interface PerspectiveDashboardProps {
  documentId: string;
}

export default function PerspectiveDashboard({ documentId }: PerspectiveDashboardProps) {
  const [data, setData] = useState<PerspectiveData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalysis();
  }, [documentId]);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/api/documents/${documentId}`);
      if (!response.ok) throw new Error("Failed to fetch analysis");
      const analysisData = await response.json();
      setData(analysisData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <p className="text-sm text-muted-foreground">Failed to load analysis</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold">Multi-Perspective Analysis</h2>
        <p className="text-sm text-muted-foreground mt-1">
          AI-extracted insights categorized by domain
        </p>
      </div>

      <Tabs defaultValue="finance" className="w-full">
        <TabsList className="grid w-full max-w-2xl grid-cols-3">
          <TabsTrigger value="finance" className="flex items-center gap-2">
            <DollarSign className="h-4 w-4" />
            Finance
          </TabsTrigger>
          <TabsTrigger value="sustainability" className="flex items-center gap-2">
            <Leaf className="h-4 w-4" />
            Sustainability
          </TabsTrigger>
          <TabsTrigger value="chemistry" className="flex items-center gap-2">
            <Beaker className="h-4 w-4" />
            Chemistry/Process
          </TabsTrigger>
        </TabsList>

        <TabsContent value="finance" className="space-y-4 mt-6">
          <FinancePerspective data={data.finance} />
        </TabsContent>

        <TabsContent value="sustainability" className="space-y-4 mt-6">
          <SustainabilityPerspective data={data.sustainability} />
        </TabsContent>

        <TabsContent value="chemistry" className="space-y-4 mt-6">
          <ChemistryPerspective data={data.chemistry} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function FinancePerspective({ data }: { data: any }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Cost Structure</CardTitle>
          <CardDescription>Breakdown of manufacturing costs</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {data.total_cost && (
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-medium">Total Cost</span>
                <Badge variant="default" className="text-lg">{data.total_cost}</Badge>
              </div>
            )}
            {data.cost_breakdown && Object.entries(data.cost_breakdown).map(([key, value]: [string, any]) => (
              value !== "Not specified" && (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground capitalize">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="text-sm font-medium">${value}</span>
                </div>
              )
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Payment Milestones</CardTitle>
          <CardDescription>Key financial checkpoints</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {data.milestones && data.milestones.length > 0 ? (
              data.milestones.slice(0, 5).map((milestone: string, idx: number) => (
                <div key={idx} className="flex items-start gap-2">
                  <TrendingUp className="h-4 w-4 text-primary mt-0.5" />
                  <span className="text-sm">{milestone}</span>
                </div>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No milestones specified</p>
            )}
          </div>
        </CardContent>
      </Card>

      {data.summary && (
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">Financial Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed">{data.summary}</p>
          </CardContent>
        </Card>
      )}

      {data.roi_considerations && data.roi_considerations.length > 0 && (
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">ROI Considerations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {data.roi_considerations.slice(0, 3).map((item: string, idx: number) => (
                <li key={idx} className="text-sm leading-relaxed">• {item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function SustainabilityPerspective({ data }: { data: any }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Waste Recovery</CardTitle>
          <CardDescription>Resource recovery and recycling</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {data.waste_recovery && Object.entries(data.waste_recovery).map(([key, value]: [string, any]) => (
              value !== "Not specified" && (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{key.replace(/_/g, " ")}</span>
                  <Badge variant="default">{value}</Badge>
                </div>
              )
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Emissions</CardTitle>
          <CardDescription>Environmental impact metrics</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {data.emissions && Object.entries(data.emissions).map(([key, value]: [string, any]) => (
              value !== "Not specified" && (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{key.replace(/_/g, " ")}</span>
                  <Badge variant="default">{value}</Badge>
                </div>
              )
            ))}
          </div>
        </CardContent>
      </Card>

      {data.summary && (
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">Sustainability Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed">{data.summary}</p>
          </CardContent>
        </Card>
      )}

      {data.compliance && data.compliance.length > 0 && (
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">Compliance & Standards</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {data.compliance.slice(0, 3).map((item: string, idx: number) => (
                <li key={idx} className="text-sm leading-relaxed">• {item}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function ChemistryPerspective({ data }: { data: any }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Formulation</CardTitle>
          <CardDescription>Product composition details</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {data.formulation?.active_ingredients && (
              <div>
                <span className="text-sm font-medium">Active Ingredients</span>
                <div className="mt-2 flex flex-wrap gap-2">
                  {data.formulation.active_ingredients.map((ing: string, idx: number) => (
                    <Badge key={idx} variant="default">{ing}</Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Process Parameters</CardTitle>
          <CardDescription>Manufacturing conditions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {data.process_parameters && Object.entries(data.process_parameters).map(([key, value]: [string, any]) => (
              value !== "Not specified" && (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{key.replace(/_/g, " ")}</span>
                  <span className="text-sm font-medium">{value}</span>
                </div>
              )
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Quality Specifications</CardTitle>
          <CardDescription>Target quality metrics</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {data.quality_specs && Object.entries(data.quality_specs).map(([key, value]: [string, any]) => (
              value !== "Not specified" && (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{key.replace(/_/g, " ")}</span>
                  <Badge>{value}</Badge>
                </div>
              )
            ))}
          </div>
        </CardContent>
      </Card>

      {data.summary && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Process Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed">{data.summary}</p>
          </CardContent>
        </Card>
      )}

      {data.critical_steps && data.critical_steps.length > 0 && (
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg">Critical Process Steps</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {data.critical_steps.slice(0, 4).map((step: string, idx: number) => (
                <li key={idx} className="text-sm leading-relaxed">• {step}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

