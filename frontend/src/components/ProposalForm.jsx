// import React, { useState } from "react";
// import axios from "axios";

// function ProposalForm() {

//   const [form, setForm] = useState({
//     client_type: "",
//     budget: "",
//     sustainability_priority: ""
//   });

//   const [result, setResult] = useState(null);

//   const handleChange = (e) => {
//     setForm({
//       ...form,
//       [e.target.name]: e.target.value
//     });
//   };

//   const handleSubmit = async () => {

//     const response = await axios.post(
//       "http://127.0.0.1:8000/ai/generate-proposal",
//       form
//     );

//     setResult(response.data);
//   };

//   return (
//     <div className="card">
//       <h2>B2B Proposal Generator</h2>

//       <input
//         name="client_type"
//         placeholder="Client Type (Hotel, Office, Retail)"
//         onChange={handleChange}
//       />

//       <input
//         name="budget"
//         type="number"
//         placeholder="Budget"
//         onChange={handleChange}
//       />

//       <select name="sustainability_priority" onChange={handleChange}>
//         <option value="">Select Sustainability Priority</option>
//         <option value="High">High</option>
//         <option value="Medium">Medium</option>
//         <option value="Low">Low</option>
//       </select>

//       <button onClick={handleSubmit}>Generate Proposal</button>

//       {result && (
//         <div className="result">
//           <p><b>Total Cost:</b> {result.total_cost}</p>
//           <p><b>Budget Remaining:</b> {result.budget_remaining}</p>

//           <p><b>Impact Summary:</b></p>
//           <p>{result.impact_positioning_summary}</p>
//         </div>
//       )}

//     </div>
//   );
// }

// export default ProposalForm;

import React, { useState } from "react";
import axios from "axios";

function ProposalForm() {

  const [form, setForm] = useState({
    client_type: "",
    budget: "",
    sustainability_priority: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await axios.post(
        "http://127.0.0.1:8000/ai/generate-proposal",
        {
          ...form,
          budget: Number(form.budget)
        }
      );

      setResult(response.data);

    } catch (err) {

      console.error(err);

      if (err.response) {
        setError(err.response.data.detail || "Server error");
      } else {
        setError("Unable to connect to server");
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">

      <h2>B2B Proposal Generator</h2>

      <input
        name="client_type"
        placeholder="Client Type (Hotel, Office, Retail)"
        onChange={handleChange}
      />

      <input
        name="budget"
        type="number"
        placeholder="Budget"
        onChange={handleChange}
      />

      <select
        name="sustainability_priority"
        onChange={handleChange}
      >
        <option value="">Select Sustainability Priority</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Generating..." : "Generate Proposal"}
      </button>

      {error && (
        <p style={{ color: "red" }}>{error}</p>
      )}

      {result && (
        <div className="result">

          <h3>Proposal Result</h3>

          {result.suggested_products && (
            <>
              <p><b>Suggested Products:</b></p>
              <ul>
                {result.suggested_products.map((item, index) => (
                  <li key={index}>
                    {item.product_name} - Qty: {item.quantity} - Cost: {item.cost}
                  </li>
                ))}
              </ul>
            </>
          )}

          <p><b>Total Cost:</b> {result.total_cost}</p>

          <p><b>Budget Remaining:</b> {result.budget_remaining}</p>

          <p><b>Impact Summary:</b></p>
          <p>{result.impact_positioning_summary}</p>

        </div>
      )}

    </div>
  );
}

export default ProposalForm;