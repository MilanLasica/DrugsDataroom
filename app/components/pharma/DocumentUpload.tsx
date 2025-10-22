"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, FileText, Loader2, CheckCircle, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/useToast";

interface DocumentUploadProps {
  onDocumentUploaded: () => void;
}

export default function DocumentUpload({ onDocumentUploaded }: DocumentUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const { toast } = useToast();

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith(".pdf")) {
      toast({
        title: "Invalid file type",
        description: "Please upload a PDF file",
        variant: "destructive",
      });
      return;
    }

    setUploading(true);
    setUploadStatus("idle");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      setUploadStatus("success");
      toast({
        title: "Document uploaded successfully",
        description: `${data.filename} has been processed (${data.pages} pages)`,
      });

      onDocumentUploaded();

      // Reset after 3 seconds
      setTimeout(() => {
        setUploadStatus("idle");
      }, 3000);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadStatus("error");
      toast({
        title: "Upload failed",
        description: "There was an error uploading your document. Please try again.",
        variant: "destructive",
      });
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  return (
    <Card className="border-2 border-dashed">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5" />
          Upload Pharmaceutical Document
        </CardTitle>
        <CardDescription>
          Upload a PDF containing drug manufacturing specifications, RFPs, or technical briefs
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center justify-center py-8">
          {uploadStatus === "idle" && (
            <>
              <Upload className="h-12 w-12 text-muted-foreground mb-4" />
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                disabled={uploading}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload">
                <Button asChild disabled={uploading}>
                  <span className="cursor-pointer">
                    {uploading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Upload className="mr-2 h-4 w-4" />
                        Select PDF File
                      </>
                    )}
                  </span>
                </Button>
              </label>
              <p className="text-xs text-muted-foreground mt-2">
                Supported format: PDF (max 50MB)
              </p>
            </>
          )}

          {uploadStatus === "success" && (
            <div className="flex flex-col items-center text-green-600">
              <CheckCircle className="h-12 w-12 mb-4" />
              <p className="font-medium">Upload successful!</p>
              <p className="text-sm text-muted-foreground mt-1">Document is being processed</p>
            </div>
          )}

          {uploadStatus === "error" && (
            <div className="flex flex-col items-center text-red-600">
              <AlertCircle className="h-12 w-12 mb-4" />
              <p className="font-medium">Upload failed</p>
              <Button
                variant="outline"
                size="sm"
                className="mt-4"
                onClick={() => setUploadStatus("idle")}
              >
                Try Again
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

