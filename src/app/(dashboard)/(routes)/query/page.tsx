"use client";

import React from "react";

export default function QueryPage({uid}) {
    const id = uid;
    
    return (
        <div className="min-h-screen flex items-center justify-center p-4">
        <div className="p-8 rounded shadow-md w-full max-w-md">
            <h2 className="text-2xl font-bold mb-6 text-center">Query Your Product</h2>
            <form className="flex flex-col space-y-4">
            <label className="flex flex-col space-y-1">
                <span className="text-sm font-semibold">Product ID</span>
                <input
                type="text"
                className="p-2 border border-gray-300 rounded"
                placeholder="Enter your product ID"
                />
            </label>
            <button
                type="submit"
                className="p-2 bg-blue-500 text-white font-semibold rounded hover:bg-blue-600"
            >
                Query
            </button>
            </form>
        </div>
        </div>
    );
}