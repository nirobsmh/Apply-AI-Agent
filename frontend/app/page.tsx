"use client";
import { useState } from "react";
import { CoverLetterResponse } from "./types/analysis";

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [coverLetter, setCoverLetter] = useState<string>("");
  const [jobDescription, setJobDescription] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  const handleResumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleJobDescriptionChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>,
  ) => {
    setJobDescription(event.target.value);
  };

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setErrorMessage("Please upload a resume PDF.");
      return;
    }

    if (!jobDescription.trim()) {
      setErrorMessage("Please enter a job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    formData.append("job_description", jobDescription.trim());

    setErrorMessage("");
    setIsAnalyzing(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze_upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let detail = "Failed to analyze resume.";
        try {
          const errorPayload = (await response.json()) as { detail?: string };
          if (typeof errorPayload.detail === "string" && errorPayload.detail) {
            detail = errorPayload.detail;
          }
        } catch {
          // Keep default detail message.
        }
        setErrorMessage(detail);
        return;
      }

      const data = (await response.json()) as CoverLetterResponse;
      setCoverLetter(data.cover_letter ?? "");
    } catch {
      setErrorMessage("Unable to reach server. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-white">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-white sm:items-start">
        <div className="flex flex-col items-center gap-8 text-center sm:items-start sm:text-left">
          <section className="flex flex-col gap-2">
            <h1 className="text-2xl font-bold text-slate-900">
              Job Application Research Agent
            </h1>
            <p className="text-slate-500">
              Upload a resume PDF, paste a job description, and get a tailored
              analysis.
            </p>
          </section>
          <section className="flex flex-col gap-2">
            <div className="flex flex-col gap-2">
              <label htmlFor="resume" className="text-slate-500">
                Upload Resume
              </label>
              <input
                type="file"
                accept="application/pdf"
                id="resume"
                name="resume"
                className="border border-black rounded-md p-2 text-slate-500 cursor-pointer"
                onChange={handleResumeChange}
              />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="job-description" className="text-slate-500">
                Job Description
              </label>
              <textarea
                id="job-description"
                name="job-description"
                className="border border-black rounded-md p-2 text-slate-500"
                onChange={handleJobDescriptionChange}
              />
            </div>
            <div className="flex justify-center">
              <button
                className={`bg-blue-500 text-white rounded-md p-2 ${isAnalyzing ? "opacity-60 cursor-not-allowed" : "cursor-pointer"}`}
                onClick={handleAnalyze}
                disabled={isAnalyzing}
              >
                {isAnalyzing ? "Analyzing..." : "Analyze"}
              </button>
            </div>
            {errorMessage ? (
              <p className="text-sm text-red-600">{errorMessage}</p>
            ) : null}
          </section>
          <section className="flex flex-col gap-2 w-full">
            <div className="flex flex-col gap-2">
              <label htmlFor="cover-letter" className="text-slate-500">
                Cover Letter
              </label>
              <textarea
                id="cover-letter"
                name="cover-letter"
                className="border border-black rounded-md p-2 text-slate-500"
                readOnly
                value={coverLetter}
              />
            </div>
            {
              /* <button
              className="bg-blue-500 text-white rounded-md p-2 cursor-pointer"
              onClick={handleGenerateCoverLetter}
            >
              Generate Cover Letter
            </button> */
            }
          </section>
        </div>
      </main>
    </div>
  );
}
