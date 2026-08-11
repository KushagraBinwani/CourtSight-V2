import { SearchResponse } from "@/types/search";

export const mockResponse: SearchResponse = {
  answer:
    "Res judicata prevents parties from re-litigating issues that have already been finally decided by a competent court.",

  sources: [
    {
      id: "1",
      title: "Satyadhyan Ghosal v. Deorajin Debi",
      citation: "AIR 1960 SC 941",
      similarity: 0.97,
    },
    {
      id: "2",
      title: "Daryao v. State of Uttar Pradesh",
      citation: "AIR 1961 SC 1457",
      similarity: 0.94,
    },
  ],
};