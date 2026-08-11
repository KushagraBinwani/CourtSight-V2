import { Scale } from "lucide-react";

export default function Navbar() {
  return (
    <header className="w-full border-b border-zinc-800">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <Scale className="h-6 w-6 text-orange-300" />

          <span className="text-lg font-semibold tracking-tight">
            CourtSight
          </span>
        </div>

        <button className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 transition hover:border-zinc-600 hover:bg-zinc-900">
          Developer Mode
        </button>
      </div>
    </header>
  );
}