"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Loader2, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface Document {
  document_id: string;
  filename: string;
}

interface DocumentListProps {
  refreshTrigger: number;
  onDocumentSelected: (documentId: string) => void;
  selectedDocumentId: string | null;
}

export default function DocumentList({
  refreshTrigger,
  onDocumentSelected,
  selectedDocumentId,
}: DocumentListProps) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDocuments = async () => {
      setLoading(true);
      try {
        const response = await fetch("http://localhost:8000/api/documents");
        const data = await response.json();
        setDocuments(data.documents || []);
      } catch (error) {
        console.error("Error fetching documents:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDocuments();
  }, [refreshTrigger]);

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </CardContent>
      </Card>
    );
  }

  if (documents.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Documents</CardTitle>
          <CardDescription>Upload a document to get started</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground text-center py-4">
            No documents uploaded yet
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Documents</CardTitle>
        <CardDescription>Select a document to analyze</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {documents.map((doc) => (
            <button
              key={doc.document_id}
              onClick={() => onDocumentSelected(doc.document_id)}
              className={cn(
                "w-full flex items-center justify-between p-4 rounded-lg border transition-colors",
                "hover:bg-accent hover:border-primary",
                selectedDocumentId === doc.document_id
                  ? "bg-accent border-primary"
                  : "bg-card border-border"
              )}
            >
              <div className="flex items-center gap-3">
                <FileText className="h-5 w-5 text-primary" />
                <span className="text-sm font-medium">{doc.filename}</span>
              </div>
              <ChevronRight className="h-4 w-4 text-muted-foreground" />
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

