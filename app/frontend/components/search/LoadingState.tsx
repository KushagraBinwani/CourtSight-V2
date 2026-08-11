"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, Loader2, Circle } from "lucide-react";

const steps = [
  "Understanding your question",
  "Searching 33,016 judgments",
  "Ranking relevant precedents",
  "Generating legal analysis",
];

export default function LoadingState() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= steps.length - 1) {
          clearInterval(interval);
          return prev;
        }
        return prev + 1;
      });
    }, 900);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="mt-12 w-full max-w-3xl rounded-2xl border border-zinc-800 bg-zinc-900/60 p-8">
      <h2 className="mb-6 text-xl font-semibold text-zinc-100">
        ⚖️ Searching the CourtSight Index
      </h2>

      <div className="space-y-4">
        {steps.map((step, index) => {
          if (index < currentStep) {
            return (
              <div key={step} className="flex items-center gap-3 text-green-400">
                <CheckCircle2 className="h-5 w-5" />
                <span>{step}</span>
              </div>
            );
          }

          if (index === currentStep) {
            return (
              <div key={step} className="flex items-center gap-3 text-orange-300">
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>{step}</span>
              </div>
            );
          }

          return (
            <div key={step} className="flex items-center gap-3 text-zinc-500">
              <Circle className="h-5 w-5" />
              <span>{step}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}