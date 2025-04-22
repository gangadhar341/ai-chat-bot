import React from "react";

export default function ErrorPage() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Something Went Wrong</h1>
      <p>We encountered an unexpected error. Please try again later.</p>
      <button
        onClick={() => window.location.reload()}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#007BFF",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
        }}
      >
        Reload Page
      </button>
    </div>
  );
}
