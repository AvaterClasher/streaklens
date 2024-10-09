// pages/loading.tsx
"use client";

import React from "react";
import LoadingScreen from "@/components/LoadingAnimation";
import { useSearchParams } from "next/navigation";

const LoadingPage: React.FC = () => {
  const searchParams = useSearchParams();
  const uid = searchParams.get("uid") || "";

  return <LoadingScreen uid={uid} />;
};

export default LoadingPage;
