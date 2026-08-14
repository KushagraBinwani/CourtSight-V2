"use client";

import { useState } from "react";
import axios from "axios";

import Hero from "@/components/layout/Hero";
import Navbar from "@/components/layout/navbar";
import SearchResults from "@/components/search/SearchResults";
import Footer from "@/components/layout/Footer";

export default function Home() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<any>(null);

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;

    setLoading(true);

    try {
      const { data } = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/query`,
        {
          query: searchQuery,
        }
      );

      setAnswer(data.answer);
      setSources(data.sources);
      setStats(data.stats);
    } catch (error) {
      console.error(error);
      setAnswer("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (topic: string) => {
    setQuery(topic);
    handleSearch(topic);
  };

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-50">
      <Navbar />

      <div className="mx-auto flex max-w-7xl flex-col items-center px-6 py-20">
        <Hero
          query={query}
          setQuery={setQuery}
          onSearch={handleSearch}
        />

        <SearchResults
          answer={answer}
          sources={sources}
          loading={loading}
          stats={stats}
          onSuggestionClick={handleSuggestionClick}
        />
      </div>

      <Footer />
    </main>
  );
}