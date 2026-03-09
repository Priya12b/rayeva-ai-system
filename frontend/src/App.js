import React from "react";
import CategoryForm from "./components/CategoryForm";
import ProposalForm from "./components/ProposalForm";
import "./App.css";

function App() {
  return (
    <div className="container">
      <h1>Rayeva AI Sustainable Commerce System</h1>

      <CategoryForm />

      <hr />

      <ProposalForm />
    </div>
  );
}

export default App;