import { useState } from "react";
import axios from "axios";
import "./upload.css";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Upload file
      const uploadRes = await axios.post(
        "https://car-contract-ai.onrender.com/upload"
,
        formData
      );

      const contractId = uploadRes.data.contract_id;

      // Redirect to result page
      

      const navigate = useNavigate();
       navigate(`/result/${contractId}`);


    } catch (err) {
      setResult("Error occurred while processing file.");
      console.error(err);
    }
  };

  return (
    <div className="page">
      <h1 className="title">Car Contract AI</h1>

      <div className="card">
        <h3>Upload Contract</h3>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={handleUpload}>
          Upload & Analyze
        </button>

        {result && <p className="result">{result}</p>}
      </div>
    </div>
  );
}
