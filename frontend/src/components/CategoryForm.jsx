import React, { useState } from "react";
import axios from "axios";

function CategoryForm() {

  const [form, setForm] = useState({
    name: "",
    description: "",
    material: "",
    base_price: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {

    const response = await axios.post(
      "http://127.0.0.1:8000/ai/generate-category",
      form
    );

    setResult(response.data);
  };

  return (
    <div className="card">
      <h2>AI Product Category Generator</h2>

      <input name="name" placeholder="Product Name" onChange={handleChange} />

      <textarea
        name="description"
        placeholder="Product Description"
        onChange={handleChange}
      />

      <input name="material" placeholder="Material" onChange={handleChange} />

      <input
        name="base_price"
        placeholder="Base Price"
        type="number"
        onChange={handleChange}
      />

      <button onClick={handleSubmit}>Generate Category</button>

      {result && (
        <div className="result">
          <p><b>Primary Category:</b> {result.primary_category}</p>
          <p><b>Sub Category:</b> {result.sub_category}</p>
          <p><b>SEO Tags:</b> {result.seo_tags.join(", ")}</p>
          <p><b>Sustainability Filters:</b> {result.sustainability_filters.join(", ")}</p>
        </div>
      )}

    </div>
  );
}

export default CategoryForm;