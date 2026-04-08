import { createClient } from "@/lib/supabase/client";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(message: string, status: number, data?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

interface FetchOptions extends Omit<RequestInit, "body"> {
  body?: unknown;
  params?: Record<string, string | number | boolean | undefined>;
}

async function getAuthToken(): Promise<string | null> {
  try {
    const supabase = createClient();
    const {
      data: { session },
    } = await supabase.auth.getSession();
    return session?.access_token ?? null;
  } catch {
    return null;
  }
}

function buildUrl(
  path: string,
  params?: Record<string, string | number | boolean | undefined>
): string {
  // Concatenate base + path manually instead of using `new URL(path, base)`,
  // because URL(absolute-path, base) strips the base's own path segment
  // (e.g. the "/v1" in "https://pilotbi.onrender.com/v1").
  const base = BASE_URL.replace(/\/+$/, "");
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const full = `${base}${normalizedPath}`;

  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.set(key, String(value));
      }
    });
    const qs = searchParams.toString();
    return qs ? `${full}?${qs}` : full;
  }
  return full;
}

async function fetchApi<T>(
  path: string,
  options: FetchOptions = {}
): Promise<T> {
  const { body, params, headers: customHeaders, ...rest } = options;

  const token = await getAuthToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "application/json",
    ...((customHeaders as Record<string, string>) || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = buildUrl(path, params);

  const response = await fetch(url, {
    ...rest,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let errorData: unknown;
    try {
      errorData = await response.json();
    } catch {
      errorData = await response.text();
    }
    throw new ApiError(
      `API error: ${response.status} ${response.statusText}`,
      response.status,
      errorData
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export const api = {
  get<T>(path: string, options?: FetchOptions): Promise<T> {
    return fetchApi<T>(path, { ...options, method: "GET" });
  },

  post<T>(path: string, body?: unknown, options?: FetchOptions): Promise<T> {
    return fetchApi<T>(path, { ...options, method: "POST", body });
  },

  put<T>(path: string, body?: unknown, options?: FetchOptions): Promise<T> {
    return fetchApi<T>(path, { ...options, method: "PUT", body });
  },

  patch<T>(path: string, body?: unknown, options?: FetchOptions): Promise<T> {
    return fetchApi<T>(path, { ...options, method: "PATCH", body });
  },

  delete<T>(path: string, options?: FetchOptions): Promise<T> {
    return fetchApi<T>(path, { ...options, method: "DELETE" });
  },

  async upload<T>(
    path: string,
    formData: FormData,
    onProgress?: (percent: number) => void
  ): Promise<T> {
    const token = await getAuthToken();
    const url = buildUrl(path);

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", url);

      if (token) {
        xhr.setRequestHeader("Authorization", `Bearer ${token}`);
      }
      xhr.setRequestHeader("Accept", "application/json");

      xhr.upload.addEventListener("progress", (event) => {
        if (event.lengthComputable && onProgress) {
          const percent = Math.round((event.loaded / event.total) * 100);
          onProgress(percent);
        }
      });

      xhr.addEventListener("load", () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            resolve(JSON.parse(xhr.responseText));
          } catch {
            resolve(undefined as T);
          }
        } else {
          reject(
            new ApiError(
              `Upload error: ${xhr.status}`,
              xhr.status,
              xhr.responseText
            )
          );
        }
      });

      xhr.addEventListener("error", () => {
        reject(new ApiError("Network error during upload", 0));
      });

      xhr.send(formData);
    });
  },
};
