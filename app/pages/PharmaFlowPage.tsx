"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DocumentUpload from "../components/pharma/DocumentUpload";
import DocumentList from "../components/pharma/DocumentList";
import PerspectiveDashboard from "../components/pharma/PerspectiveDashboard";
import ChatInterface from "../components/pharma/ChatInterface";
import KnowledgeGraph from "../components/pharma/KnowledgeGraph";
import { FileText, MessageSquare, Network, Upload } from "lucide-react";

export default function PharmaFlowPage() {
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleDocumentUploaded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleDocumentSelected = (documentId: string) => {
    setSelectedDocumentId(documentId);
  };

  return (
    <div className="flex flex-col w-full bg-background h-full">
      {/* Header */}
      <div className="border-b px-6 py-4 flex-shrink-0">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
          PharmaFlow
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          AI-Driven Drug Manufacturing Assistant
        </p>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Tabs defaultValue="upload" className="flex-1 flex flex-col overflow-hidden">
          <TabsList className="mx-6 mt-4 grid w-full max-w-md grid-cols-4 flex-shrink-0">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <Upload className="h-4 w-4" />
              Upload
            </TabsTrigger>
            <TabsTrigger value="analysis" className="flex items-center gap-2" disabled={!selectedDocumentId}>
              <FileText className="h-4 w-4" />
              Analysis
            </TabsTrigger>
            <TabsTrigger value="graph" className="flex items-center gap-2" disabled={!selectedDocumentId}>
              <Network className="h-4 w-4" />
              Graph
            </TabsTrigger>
            <TabsTrigger value="chat" className="flex items-center gap-2" disabled={!selectedDocumentId}>
              <MessageSquare className="h-4 w-4" />
              Chat
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="flex-1 overflow-y-auto overflow-x-hidden px-6 py-4">
            <div className="max-w-4xl mx-auto space-y-6">
              <DocumentUpload onDocumentUploaded={handleDocumentUploaded} />
              <DocumentList
                refreshTrigger={refreshTrigger}
                onDocumentSelected={handleDocumentSelected}
                selectedDocumentId={selectedDocumentId}
              />
            </div>
          </TabsContent>

          <TabsContent value="analysis" className="flex-1 overflow-y-auto overflow-x-hidden px-6 py-4">
            {selectedDocumentId && (
              <PerspectiveDashboard documentId={selectedDocumentId} />
            )}
          </TabsContent>

          <TabsContent value="graph" className="flex-1 overflow-hidden px-6 py-4">
            {selectedDocumentId && (
              <KnowledgeGraph documentId={selectedDocumentId} />
            )}
          </TabsContent>

          <TabsContent value="chat" className="flex-1 overflow-y-auto overflow-x-hidden px-6 py-4">
            {selectedDocumentId && (
              <ChatInterface documentId={selectedDocumentId} />
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

