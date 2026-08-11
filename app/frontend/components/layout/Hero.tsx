"use client";

import { motion } from "framer-motion";
import { Scale } from "lucide-react";

import SearchBar from "@/components/search/SearchBar";

interface HeroProps {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  onSearch: (query: string) => void;
}

export default function Hero({
  query,
  setQuery,
  onSearch,
}: HeroProps) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.7,
        ease: "easeOut",
      }}
      className="flex flex-col items-center justify-center space-y-6 text-center"
    >
      <Scale className="h-16 w-16 text-orange-300" />

      <div className="flex flex-col items-center">
        <h1 className="text-5xl font-bold tracking-tight">
          CourtSight
        </h1>

        <p className="mt-4 max-w-2xl text-lg text-zinc-400">
          Ask, retrieve, and verify Indian Supreme Court judgments using AI.
        </p>

        <div className="mt-8 w-full">
          <SearchBar
            query={query}
            setQuery={setQuery}
            onSearch={onSearch}
          />
        </div>
      </div>
    </motion.section>
  );
}