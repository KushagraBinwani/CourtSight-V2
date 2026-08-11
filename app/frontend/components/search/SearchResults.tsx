"use client";

import AnswerCard from "@/components/search/AnswerCard";
import LoadingState from "@/components/search/LoadingState";
import RetrievalStats from "@/components/search/RetrievalStats";
import SourcesList from "../sources/SourcesList";

type SearchResultsProps = {
  answer: string;
  sources: any[];
  loading: boolean;
  stats: {
    retrieved: number;
    latency: number;
    avg_score: number;
  } | null;
  onSuggestionClick: (topic: string) => void;
};

const popularSearches = [
  "Reservation Ceiling",
  "Basic Structure",
  "Article 21",
  "Judicial Review",
  "Article 14",
  "Federalism",
  "Freedom of Speech",
  "Right to Privacy",
];

export default function SearchResults({
  answer,
  sources,
  loading,
  stats,
  onSuggestionClick,
}: SearchResultsProps) {
  if (loading) {
    return <LoadingState />;
  }

  if (!answer) {
    return (
      <div className="mt-6 flex w-full max-w-4xl flex-col items-center">
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.25em] text-zinc-500">
          Explore Topics
        </p>

        <div className="flex max-w-3xl flex-wrap justify-center gap-3">
          {popularSearches.map((search) => (
            <button
              key={search}
              onClick={() => onSuggestionClick(search)}
              className="rounded-full border border-[#D4A44B]/30 bg-[#D4A44B]/10 px-5 py-2 text-sm font-medium text-[#D4A44B] transition-all duration-200 hover:-translate-y-0.5 hover:border-[#D4A44B] hover:bg-[#D4A44B]/20 hover:shadow-lg hover:shadow-[#D4A44B]/10"
            >
              {search}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mt-12 w-full max-w-4xl space-y-6">
      {stats && (
        <RetrievalStats
          retrieved={stats.retrieved}
          latency={stats.latency}
          avgScore={stats.avg_score}
        />
      )}

      <AnswerCard answer={answer} />

      <SourcesList sources={sources} />
    </div>
  );
}