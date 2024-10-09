// pages/submit.tsx
"use client";

import React from "react";
import SubmitForm from "@/components/SubmissionForm";

const SubmitPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Submit Your Product</h2>
        <SubmitForm />
      </div>
    </div>
  );
};

export default SubmitPage;
