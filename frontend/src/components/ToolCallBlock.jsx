import React from "react";

export default function ToolCallBlock({ message }) {
  if (!message) return null;

  const { tool, status, input, result, error } = message;
  const title = tool ? tool.replace(/_/g, " ") : "Tool";

  return (
    <section className="tool-call-block" data-testid="tool-call-block">
      <div className="tool-call-header">
        <div className="tool-call-title" data-testid="tool-name">{title}</div>
        <div className={`tool-call-status tool-call-status-${status?.toLowerCase() || "running"}`}>
          {status || "Running"}
        </div>
      </div>

      <div className="tool-call-body">
        <div className="tool-call-section" data-testid="tool-input">
          <div className="tool-call-label">Input</div>
          <pre className="tool-call-json">{JSON.stringify(input || {}, null, 2)}</pre>
        </div>

        <div className="tool-call-section" data-testid="tool-result">
          <div className="tool-call-label">Output</div>
          {error ? (
            <pre className="tool-call-error">{typeof error === "string" ? error : JSON.stringify(error, null, 2)}</pre>
          ) : result ? (
            <pre className="tool-call-json">{JSON.stringify(result, null, 2)}</pre>
          ) : (
            <div className="tool-call-pending">Awaiting result…</div>
          )}
        </div>
      </div>
    </section>
  );
}
