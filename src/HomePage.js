import React from "react";

function HomePage() {
  return (
    <section style={styles.container}>
      <h1>Welcome to Lawgic ⚖️</h1>
      <p>
        Streamline your legal communications with clarity, empathy, and precision.
      </p>
    </section>
  );
}

const styles = {
  container: {
    textAlign: "center",
    padding: "60px 20px",
    backgroundColor: "#f4f4f4",
  },
};

export default HomePage;