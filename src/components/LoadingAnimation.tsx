// components/LoadingScreen.tsx
"use client";

import React, { useEffect, useState } from "react";

interface StatusResponse {
  status: "queue" | "completed" | "none";
  message?: string;
}

interface LoadingScreenProps {
  uid: string;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ uid }) => {
  const [status, setStatus] = useState<"queue" | "completed" | "none">("queue");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!uid) {
      setError("No UID provided.");
      setStatus("none");
      return;
    }

    const checkStatus = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/status?uid=${uid}`);
        if (!response.ok) {
          throw new Error("Failed to fetch status.");
        }

        const data: StatusResponse = await response.json();
        setStatus(data.status);
      } catch (err: any) {
        setError(err.message || "An unexpected error occurred.");
        setStatus("none");
      }
    };

    checkStatus();

    const interval = setInterval(() => {
      checkStatus();
    }, 5000);

    return () => clearInterval(interval);
  }, [uid]);

  const renderContent = () => {
    switch (status) {
      case "queue":
        return (
          <>
            <div className="loader mb-4"></div>
            <p className="text-lg">Your request is being processed. An email will be sent once completed.</p>
          </>
        );
      case "completed":
        return (
          <p className="text-lg text-green-600">Processing completed! Please check your email.</p>
        );
      case "none":
        return (
          <p className="text-lg text-red-600">No processing found for the provided UID.</p>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black p-4">
      <div className="bg-black p-8 rounded shadow-md w-full max-w-md text-center">
        <h2 className="text-2xl font-bold mb-6">Processing Your Request</h2>
        {error ? (
          <div className="text-red-600">{error}</div>
        ) : (
          renderContent()
        )}
      </div>
      <style jsx>{`
        .loader {
          border: 4px solid #f3f3f3;
          border-top: 4px solid #3490dc;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
};

export default LoadingScreen;
