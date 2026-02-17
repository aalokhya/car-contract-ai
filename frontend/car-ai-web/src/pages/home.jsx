import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="page">
      <div className="card">
        <h1>Car Contract AI</h1>
        <p>
          Analyze car lease contracts, detect risks, and get negotiation tips.
        </p>

        <button onClick={() => navigate("/upload")}>
          Start Analysis
        </button>
      </div>
    </div>
  );
}
