import { Card, CardContent } from "@/components/ui/card";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface AnswerCardProps {
  answer: string;
}

export default function AnswerCard({ answer }: AnswerCardProps) {
  return (
    <Card className="w-full border-zinc-800 bg-zinc-900 text-zinc-100 shadow-lg">
      <CardContent className="p-8">
        <div
          className="
            prose
            prose-invert
            prose-zinc
            max-w-none
            prose-headings:font-semibold
            prose-headings:text-zinc-100
            prose-p:text-zinc-300
            prose-li:text-zinc-300
            prose-strong:text-zinc-100
            prose-code:text-blue-300
            prose-pre:bg-zinc-950
            prose-blockquote:border-zinc-700
          "
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {answer}
          </ReactMarkdown>
        </div>
      </CardContent>
    </Card>
  );
}