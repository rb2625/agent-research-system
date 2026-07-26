"use client";

import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const PRESETS = [
  "Compare two job offers",
  "Explain a new UAE policy",
  "Should I buy a used or new laptop",
];

type JobStatus = "idle" | "running" | "done" | "error";

interface Finding {
  subtask: string;
  findings: string;
  provider?: string;
}

interface JobResult {
  topic: string;
  subtasks: string[];
  findings: Finding[];
  report: string;
}

interface JobState {
  status: JobStatus;
  steps: string[];
  result: JobResult | null;
  error: string | null;
}

export default function Home() {
  const [topic, setTopic] = useState("");
  const [job, setJob] = useState<JobState>({
    status: "idle",
    steps: [],
    result: null,
    error: null,
  });
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  const startResearch = async (query: string) => {
    if (!query.trim()) return;

    setJob({ status: "running", steps: [], result: null, error: null });

    const response = await fetch(`${API_URL}/research`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: query }),
    });

    const { job_id } = await response.json();

    pollRef.current = setInterval(async () => {
      const statusResponse = await fetch(`${API_URL}/research/${job_id}`);
      const data = await statusResponse.json();

      setJob({
        status: data.status,
        steps: data.steps,
        result: data.result,
        error: data.error,
      });

      if (data.status === "done" || data.status === "error") {
        if (pollRef.current) clearInterval(pollRef.current);
      }
    }, 1500);
  };

  const handleSubmit = () => {
    startResearch(topic);
  };

  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: "3rem 1.5rem" }}>
      <div
        style={{
          display: "flex",
          gap: 8,
          marginBottom: "1.75rem",
          flexWrap: "wrap",
        }}
      >
        {PRESETS.map((preset) => (
          <button
            key={preset}
            onClick={() => {
              setTopic(preset);
              startResearch(preset);
            }}
            style={presetButtonStyle}
          >
            {preset}
          </button>
        ))}
      </div>

      <div style={inputRowStyle}>
        <input
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          placeholder="Ask anything"
          style={inputStyle}
        />
        <button onClick={handleSubmit} style={runButtonStyle}>
          RUN &rarr;
        </button>
      </div>

      {job.status !== "idle" && (
        <div style={{ marginBottom: "2rem" }}>
          <p style={sectionLabelStyle}>Progress</p>
          {job.steps.map((step, index) => (
            <div key={index} style={stepRowStyle}>
              <span style={stepNumberStyle}>
                {String(index + 1).padStart(2, "0")}
              </span>
              <span
                style={{
                  fontSize: 14,
                  color:
                    index === job.steps.length - 1 && job.status === "running"
                      ? "var(--text-primary)"
                      : "var(--text-secondary)",
                }}
              >
                {step}
              </span>
            </div>
          ))}
          {job.status === "running" && (
            <div style={stepRowStyle}>
              <span style={{ ...stepNumberStyle, color: "var(--accent)" }}>
                {String(job.steps.length + 1).padStart(2, "0")}
              </span>
              <span style={{ fontSize: 14, color: "var(--text-primary)" }}>
                Working&hellip;
              </span>
            </div>
          )}
        </div>
      )}

      {job.status === "error" && (
        <p style={{ color: "var(--accent)", fontSize: 14 }}>{job.error}</p>
      )}

      {job.status === "done" && job.result && (
        <div
          style={{ borderTop: "1px solid var(--border)", paddingTop: "1.5rem" }}
        >
          <h3 style={reportTitleStyle}>{job.result.topic}</h3>
          <div style={reportBodyStyle}>
            <ReactMarkdown
              components={{
                h2: (props) => <h4 style={reportHeadingStyle} {...props} />,
                h3: (props) => <h4 style={reportHeadingStyle} {...props} />,
                p: (props) => <p style={reportParagraphStyle} {...props} />,
                strong: (props) => (
                  <strong style={reportStrongStyle} {...props} />
                ),
                ul: (props) => <ul style={reportListStyle} {...props} />,
                li: (props) => <li style={reportParagraphStyle} {...props} />,
                a: (props) => <a style={reportLinkStyle} {...props} />,
              }}
            >
              {job.result.report}
            </ReactMarkdown>
          </div>
        </div>
      )}
    </main>
  );
}

const presetButtonStyle: React.CSSProperties = {
  fontSize: 12,
  padding: "5px 12px",
  background: "transparent",
  border: "0.5px solid var(--border)",
  color: "var(--text-secondary)",
  borderRadius: 4,
};

const inputRowStyle: React.CSSProperties = {
  display: "flex",
  gap: 0,
  marginBottom: "2rem",
  borderBottom: "1px solid var(--border)",
  paddingBottom: 8,
};

const inputStyle: React.CSSProperties = {
  flex: 1,
  background: "transparent",
  border: "none",
  color: "var(--text-primary)",
  fontSize: 15,
  outline: "none",
};

const runButtonStyle: React.CSSProperties = {
  fontSize: 12,
  color: "var(--accent)",
  fontFamily: "var(--font-mono)",
  background: "transparent",
  border: "none",
  alignSelf: "center",
};

const sectionLabelStyle: React.CSSProperties = {
  fontSize: 11,
  letterSpacing: "0.08em",
  color: "var(--text-muted)",
  textTransform: "uppercase",
  marginBottom: 10,
  fontFamily: "var(--font-mono)",
};

const stepRowStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "baseline",
  gap: 10,
  padding: "5px 0",
  borderBottom: "1px solid var(--border-soft)",
};

const stepNumberStyle: React.CSSProperties = {
  fontSize: 12,
  color: "var(--text-muted)",
  fontFamily: "var(--font-mono)",
};

const reportTitleStyle: React.CSSProperties = {
  fontFamily: "var(--font-serif)",
  fontSize: 20,
  fontWeight: 400,
  color: "var(--text-primary)",
  marginBottom: 10,
};
const reportBodyStyle: React.CSSProperties = {
  fontFamily: "var(--font-serif)",
  fontSize: 15,
  color: "var(--text-secondary)",
};

const reportHeadingStyle: React.CSSProperties = {
  fontFamily: "var(--font-serif)",
  fontSize: 16,
  fontWeight: 500,
  color: "var(--text-primary)",
  marginTop: "1.5rem",
  marginBottom: "0.5rem",
};

const reportParagraphStyle: React.CSSProperties = {
  lineHeight: 1.7,
  marginBottom: "0.75rem",
};

const reportStrongStyle: React.CSSProperties = {
  fontWeight: 500,
  color: "var(--text-primary)",
};

const reportListStyle: React.CSSProperties = {
  paddingLeft: "1.25rem",
  marginBottom: "0.75rem",
};

const reportLinkStyle: React.CSSProperties = {
  color: "var(--accent)",
  textDecoration: "none",
};
