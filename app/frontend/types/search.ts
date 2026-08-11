export interface Source {
  id: string;
  title: string;
  citation: string;
  similarity: number;
}

export interface SearchResponse {
  answer: string;
  sources: Source[];
}