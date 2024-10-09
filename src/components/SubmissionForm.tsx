// components/SubmitForm.tsx
"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useClerk } from "@clerk/nextjs";

interface SubmissionFormData {
  productName: string;
  csvLink: string;
  clerkUid: string;
}

const SubmitForm: React.FC = () => {
  const clerk = useClerk()
  const userId = clerk.user?.id;
  const router = useRouter();
  const [formData, setFormData] = useState<SubmissionFormData>({
    productName: "",
    csvLink: "",
    clerkUid: userId,
  });
  const [error, setError] = useState<string>("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!formData.productName || !formData.csvLink || !formData.clerkUid) {
      setError("All fields are required.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to submit data.");
      }

      router.push(`/loading?uid=${formData.clerkUid}`);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="mb-4 text-red-600 text-center">{error}</div>
      )}
      <div>
        <label className="block text-sm font-medium text-gray-400">
          Product Name
        </label>
        <input
          type="text"
          name="productName"
          value={formData.productName}
          onChange={handleChange}
          required
          className="mt-1 block w-full border border-gray-300 text-black rounded-md p-2"
          placeholder="Enter product name"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-400">
          CSV File Link
        </label>
        <input
          type="url"
          name="csvLink"
          value={formData.csvLink}
          onChange={handleChange}
          required
          className="mt-1 block w-full border border-gray-300 text-black rounded-md p-2"
          placeholder="https://example.com/file.csv"
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
      >
        Submit
      </button>
    </form>
  );
};

export default SubmitForm;
