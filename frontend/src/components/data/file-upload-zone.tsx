"use client";

import { useState, useCallback } from "react";
import { cn } from "@/lib/utils";
import { Upload, FileCheck, X, FileSpreadsheet, Loader2 } from "lucide-react";

interface FileUploadZoneProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  maxSizeMb?: number;
  isUploading?: boolean;
  progress?: number;
  className?: string;
}

export function FileUploadZone({
  onFileSelect,
  accept = ".xlsx,.csv",
  maxSizeMb = 10,
  isUploading = false,
  progress = 0,
  className,
}: FileUploadZoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const validateFile = useCallback(
    (file: File): boolean => {
      setError(null);
      const validExtensions = accept.split(",").map((e) => e.trim());
      const fileExt = "." + file.name.split(".").pop()?.toLowerCase();

      if (!validExtensions.includes(fileExt)) {
        setError(`Format non supporte. Utilisez : ${accept}`);
        return false;
      }

      if (file.size > maxSizeMb * 1024 * 1024) {
        setError(`Fichier trop volumineux. Maximum : ${maxSizeMb} MB`);
        return false;
      }

      return true;
    },
    [accept, maxSizeMb]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file && validateFile(file)) {
        setSelectedFile(file);
        onFileSelect(file);
      }
    },
    [onFileSelect, validateFile]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file && validateFile(file)) {
        setSelectedFile(file);
        onFileSelect(file);
      }
    },
    [onFileSelect, validateFile]
  );

  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function clearFile() {
    setSelectedFile(null);
    setError(null);
  }

  if (isUploading) {
    return (
      <div
        className={cn(
          "flex flex-col items-center gap-4 rounded-2xl border-2 border-blue-200 bg-blue-50 p-10",
          className
        )}
      >
        <Loader2 className="h-10 w-10 text-blue-600 animate-spin" />
        <div className="w-full max-w-xs">
          <div className="flex items-center justify-between text-sm mb-2">
            <span className="text-blue-700 font-medium">
              Import en cours...
            </span>
            <span className="text-blue-600 font-semibold">{progress}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-blue-200">
            <div
              className="h-2 rounded-full bg-blue-600 transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
        {selectedFile && (
          <p className="text-xs text-blue-600">{selectedFile.name}</p>
        )}
      </div>
    );
  }

  if (selectedFile && !isUploading) {
    return (
      <div
        className={cn(
          "rounded-2xl border-2 border-green-200 bg-green-50 p-6",
          className
        )}
      >
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
            <FileCheck className="h-6 w-6 text-green-600" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium text-green-800 truncate">
              {selectedFile.name}
            </p>
            <p className="text-sm text-green-600">
              {formatFileSize(selectedFile.size)}
            </p>
          </div>
          <button
            type="button"
            onClick={clearFile}
            className="rounded-lg p-1.5 text-green-600 hover:bg-green-100 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragOver(true);
      }}
      onDragLeave={() => setIsDragOver(false)}
      onDrop={handleDrop}
      className={cn(
        "flex flex-col items-center gap-4 rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-200 cursor-pointer",
        isDragOver
          ? "border-blue-500 bg-blue-50 scale-[1.01]"
          : "border-gray-200 bg-gray-50/50 hover:border-blue-300 hover:bg-blue-50/30",
        error && "border-red-300 bg-red-50/30",
        className
      )}
    >
      <div
        className={cn(
          "flex h-16 w-16 items-center justify-center rounded-2xl transition-colors",
          isDragOver ? "bg-blue-200" : "bg-blue-100"
        )}
      >
        {isDragOver ? (
          <FileSpreadsheet className="h-8 w-8 text-blue-600" />
        ) : (
          <Upload className="h-8 w-8 text-blue-600" />
        )}
      </div>
      <div>
        <p className="text-sm font-medium text-ink">
          {isDragOver
            ? "Deposez votre fichier ici"
            : "Glissez votre fichier ici"}
        </p>
        <p className="mt-1 text-xs text-ink-3">ou cliquez pour selectionner</p>
      </div>
      <label className="cursor-pointer">
        <span className="inline-flex items-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors">
          Parcourir
        </span>
        <input
          type="file"
          accept={accept}
          onChange={handleFileInput}
          className="hidden"
        />
      </label>
      <p className="text-xs text-ink-3">
        Formats : .xlsx, .csv &middot; Max. {maxSizeMb} MB
      </p>

      {error && (
        <p className="text-xs text-red-600 font-medium">{error}</p>
      )}
    </div>
  );
}
