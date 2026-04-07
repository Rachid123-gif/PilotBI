"use client";

import { useCallback, useState } from "react";
import { api } from "@/lib/api";
import type { UploadResponse } from "@/types/api";

interface UploadState {
  progress: number;
  isUploading: boolean;
  result: UploadResponse | null;
  error: string | null;
  fileName: string | null;
}

export function useUpload() {
  const [state, setState] = useState<UploadState>({
    progress: 0,
    isUploading: false,
    result: null,
    error: null,
    fileName: null,
  });

  const upload = useCallback(async (file: File) => {
    setState({
      progress: 0,
      isUploading: true,
      result: null,
      error: null,
      fileName: file.name,
    });

    try {
      const formData = new FormData();
      formData.append("file", file);

      const result = await api.upload<UploadResponse>(
        "/upload",
        formData,
        (percent) => {
          setState((prev) => ({ ...prev, progress: percent }));
        }
      );

      setState({
        progress: 100,
        isUploading: false,
        result,
        error: null,
        fileName: file.name,
      });

      return result;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Erreur lors de l'upload";
      setState((prev) => ({
        ...prev,
        isUploading: false,
        error: message,
      }));
      throw err;
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      progress: 0,
      isUploading: false,
      result: null,
      error: null,
      fileName: null,
    });
  }, []);

  return {
    ...state,
    upload,
    reset,
  };
}
