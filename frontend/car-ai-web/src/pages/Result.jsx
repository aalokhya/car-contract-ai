import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import "./result.css";

export default function Result() {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    axios.post(`https://car-contract-ai.onrender.com/analyze/${id}`)
      .then(res => setAnalysis(res.data))
      .catch(err => console.error(err));
  }, [id]);

  // Loading state
  if (!analysis) {
    return (
      <div className="page">
        <div className="result-container">
          <h2 className="title">Analyzing contract...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="result-container">

        <h1 className="title">Contract Analysis</h1>

        <div className="result-card">

          {/* Summary */}
          <h3>Contract Summary</h3>
          <hr />
          {analysis.summary && Object.entries(analysis.summary).map(([key, value]) => (
            <p key={key}>
              <strong>{key.replace(/_/g, " ")}:</strong> {value || "Not found"}
            </p>
          ))}

          {/* Risks */}
          <h3>Risks Detected</h3>
          <hr />
          {analysis.risks && analysis.risks.length > 0 ? (
            analysis.risks.map((risk, i) => (
              <p key={i}>⚠ {risk}</p>
            ))
          ) : (
            <p>No major risks detected</p>
          )}

          {/* Fairness Score */}
          {analysis.fairness_score && (
            <>
              <h3>Fairness Score</h3>
              <hr />
              <p className="score">{analysis.fairness_score}/100</p>
            </>
          )}

          {/* Negotiation Tips */}
          {analysis.tips && (
            <>
              <h3>Negotiation Tips</h3>
              <hr />

              <strong>Unfair Clauses:</strong>
              <ul>
                {analysis.tips?.unfair_clauses?.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>

              <strong>Negotiation Points:</strong>
              <ul>
                {analysis.tips?.negotiation_points?.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>

              <strong>Suggested Message:</strong>
              <p>{analysis.tips.message_to_dealer}</p>
            </>
          )}

          {/* Download Button */}
          <button
            onClick={() =>
              window.open(`https://car-contract-ai.onrender.com/download/${id}`)
            }
          >
            Download Report
          </button>

        </div>
      </div>
    </div>
  );
}
