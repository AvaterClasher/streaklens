"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useClerk } from "@clerk/nextjs";

interface SubmissionFormData {
  product_name: string;
  file_url: string;
  uid: string;
}

const SubmitForm: React.FC = () => {
  const clerk = useClerk();
  const userId = clerk.user?.id;
  const router = useRouter();
  const [formData, setFormData] = useState<SubmissionFormData>({
    product_name: "",
    file_url: "",
    uid: userId || "",
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

  const handleSubmit = async () => {
    setError("");
    if (!formData.product_name || !formData.file_url || !formData.uid) {
      setError("All fields are required.");
      return;
    }

    try {
      console.log(formData);
      const response = await fetch("http://localhost:8000/process_file", {
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

      router.push(`/loading?uid=${formData.uid}`);

    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    }
  };

  return (
    <div className="space-y-4">
      {error && <div className="mb-4 text-red-600 text-center">{error}</div>}
      
      <div>
        <label className="block text-sm font-medium text-gray-400">
          Product Name
        </label>
        <input
          type="text"
          name="product_name"
          value={formData.product_name}
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
          name="file_url"
          value={formData.file_url}
          onChange={handleChange}
          required
          className="mt-1 block w-full border border-gray-300 text-black rounded-md p-2"
          placeholder="https://example.com/file.csv"
        />
      </div>
      <button
        onClick={handleSubmit}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
      >
        Submit
      </button>
    </div>
  );
};

export default SubmitForm;
