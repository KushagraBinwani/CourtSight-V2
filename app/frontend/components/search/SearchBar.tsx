"use client";

import { ArrowUp } from "lucide-react";

interface SearchBarProps {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  onSearch: (query: string) => void;
}

export default function SearchBar({
  query,
  setQuery,
  onSearch,
}: SearchBarProps) {
  const handleSearch = () => {
    if (!query.trim()) return;
    onSearch(query);
  };

  return (
    <div className="mt-12 w-full max-w-3xl">
      <div className="flex items-center rounded-2xl border border-zinc-800 bg-zinc-900 p-2 shadow-lg backdrop-blur-sm">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearch();
            }
          }}
          placeholder="Ask a legal question..."
          className="flex-1 bg-transparent px-4 py-3 text-lg text-zinc-100 placeholder:text-zinc-500 focus:outline-none"
        />

        <button
          onClick={handleSearch}
          className="rounded-xl bg-orange-400 p-3 text-black transition hover:bg-orange-300"
        >
          <ArrowUp className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}