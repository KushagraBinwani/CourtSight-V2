export default function Footer() {
  return (
    <footer className="mt-24 border-t border-zinc-800">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-8 text-sm text-zinc-500 md:flex-row">
        <div>
          © {new Date().getFullYear()} CourtSight. Built for intelligent legal research.
        </div>

        <div className="flex items-center gap-6">
          <span>Powered by Gemini</span>
          <span>•</span>
          <span>FAISS Retrieval</span>
          <span>•</span>
          <span>Indian Supreme Court Judgments</span>
        </div>
      </div>
    </footer>
  );
}