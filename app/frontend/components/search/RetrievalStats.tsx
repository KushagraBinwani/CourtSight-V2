"use client";

import { Database, Gauge, Clock3 } from "lucide-react";

interface RetrievalStatsProps {
  retrieved: number;
  latency: number;
  avgScore: number;
}

export default function RetrievalStats({
  retrieved,
  latency,
  avgScore,
}: RetrievalStatsProps) {
  return (
    <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
      <StatCard
        icon={<Database className="h-5 w-5 text-[#D4A44B]" />}
        label="Retrieved"
        value={`${retrieved} Chunks`}
      />

      <StatCard
        icon={<Gauge className="h-5 w-5 text-[#D4A44B]" />}
        label="Avg. Similarity"
        value={avgScore.toFixed(4)}
      />

      <StatCard
        icon={<Clock3 className="h-5 w-5 text-[#D4A44B]" />}
        label="Latency"
        value={`${latency.toFixed(2)} s`}
      />
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5">
      <div className="mb-3 flex items-center gap-2">
        {icon}
        <span className="text-sm text-zinc-400">{label}</span>
      </div>

      <p className="text-2xl font-semibold text-zinc-100">
        {value}
      </p>
    </div>
  );
}