import React from "react";

function AILegalAssistant() {
  return (
    <section style={styles.container}>
      <h2>AI Legal Assistant</h2>
      <p>Draft and refine client messages with professional legal tone and accuracy.</p>
      <textarea
        style={styles.textarea}
        placeholder="Type your legal message draft here..."
      ></textarea>
      <button style={styles.button}>Generate Response</button>
    </section>
  );
}

const styles = {
  container: {
    padding: "40px 20px",
    textAlign: "center",
    fontFamily: "'Garamond', serif", 
  },
  textarea: {
    width: "80%",
    height: "150px",
    padding: "10px",
    fontSize: "1rem",
    fontFamily: "'Garamond', serif", 
  },
  button: {
    marginTop: "20px",
    padding: "10px 20px",
    fontSize: "1rem",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontFamily: "'Arial', sans-serif", // font-family: Arial, sans-serif;
  },
};

export default AILegalAssistant;