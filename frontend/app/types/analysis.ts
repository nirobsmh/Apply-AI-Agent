
export type AnalyzeResponse = {
    resume_skills: string[];
    job_skills: string[];
    missing_skills: string[];
    match_score: number;
    resume_suggestions: string[];
    cover_letter: string;
  };

export type CoverLetterResponse = {
    cover_letter: string;
};