type SourcesListProps = {
  sources: any[];
};

function getScoreColor(score: number) {
    if (score >= 0.85) {
        return "bg-green-900/40 text-green-300";
    }

    if (score >= 0.70) {
        return "bg-blue-900/40 text-blue-300";
    }

    if (score >= 0.55) {
        return "bg-yellow-900/40 text-yellow-300";
    }

    return "bg-red-900/40 text-red-300";
}

export default function SourcesList({ sources }: SourcesListProps) {
  return (
    <div className="mt-8">
      <h2 className="mb-4 text-2xl font-semibold text-zinc-100">
        Sources
      </h2>

      <div className="space-y-4">
        {sources.map((source, index) => (
          <div
            key={index}
            className="rounded-xl border border-zinc-800 bg-zinc-900 p-5 transition-all duration-200 hover:-translate-y-1 hover:border-zinc-700 hover:bg-zinc-800/70 hover:shadow-lg hover:shadow-black/30"
          >
            <h3 className="text-lg font-semibold text-zinc-100">
              {source.title}
            </h3>

            <div className="mt-3 flex flex-wrap gap-2 text-sm">
                <span className={`rounded-full ${getScoreColor(source.score)} px-3 py-1`}>
                    Score: {source.score}
                </span>

                <span className="rounded-full bg-zinc-800 px-3 py-1 text-zinc-300">
                    Chunk #{source.chunk_number}
                </span>
            </div>

            <p className="mt-4 leading-7 text-zinc-300">
                {source.preview}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}