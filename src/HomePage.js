import React from "react";

function HomePage() {
  return (
    <section style={styles.container}>
      <div style={styles.overlay}>
        <h1 style={styles.heading}>Welcome to Lawgic ⚖️</h1>
        <p style={styles.paragraph}>
          Streamline your legal communications with clarity, empathy, and precision.
        </p>
      </div>
    </section>
  );
}

const styles = {
  container: {
    position: "relative",
    textAlign: "center",
    padding: "100px 20px",
    backgroundImage: "url('https://www.acslaw.org/wp-content/uploads/2019/09/iStock-939262058.jpg')", // 👈 replace with your image https://www.acslaw.org/wp-content/uploads/2019/09/iStock-939262058.jpg
    backgroundSize: "cover",
    backgroundPosition: "center",
    color: "white", // text color
    fontFamily: "'Garamond', serif",
    height: "100vh", // makes the section full screen height
  },
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.5)", // 👈 black overlay
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: "0 20px",
  },
  heading: {
    fontSize: "48px",
    margin: "0 0 20px 0",
  },
  paragraph: {
    fontSize: "20px",
    maxWidth: "600px",
  },
};

export default HomePage;