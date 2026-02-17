import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/home.jsx";

import Upload from "./pages/Upload";
import Result from "./pages/Result";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/result/:id" element={<Result />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
