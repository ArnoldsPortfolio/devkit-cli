"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
type Finding = { path: string; line: number; rule: string; snippet: string };
type Scan = { id: string; root: string; finding_count: number; exit_code: number; findings: Finding[] };
export default function ScansPage() {
  const [rows, setRows] = useState<Scan[]>([]);
  const [root, setRoot] = useState(".");
  const [error, setError] = useState("");
  async function load() { setRows(await api<Scan[]>("/scans")); }
  useEffect(() => { load().catch((err: Error) => setError(err.message)); }, []);
  return (
    <main>
      <h1>Scans</h1>
      {error ? <p className="err">{error}</p> : null}
      <p>
        <input value={root} onChange={(e) => setRoot(e.target.value)} />
        <button type="button" onClick={() => api("/scans", { method: "POST", body: JSON.stringify({ root }) }).then(load).catch((err: Error) => setError(err.message))}>Run scan</button>
      </p>
      {rows.map((s) => (
        <article className="card" key={s.id}>
          <p>{s.root} · {s.finding_count} finding(s) · exit {s.exit_code}</p>
          {s.findings.map((f, i) => <p className="muted" key={i}>{f.path}:{f.line} {f.rule} — {f.snippet}</p>)}
        </article>
      ))}
    </main>
  );
}
