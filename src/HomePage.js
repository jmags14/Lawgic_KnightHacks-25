import React from "react";
import logo from "./assets/lawgic logo.png"; // ✅ make sure this path matches your file’s location

function HomePage() {
  return (
    <section style={styles.container}>
      <div style={styles.overlay}>
        <img src={logo} alt="Lawgic Logo" style={styles.logo} /> {/* swapped title for logo */}
        <h2 style={styles.subheading}>Streamline case work. Strengthen Strategy.</h2>
        <p style={styles.paragraph}>
          A specialized AI assistant built for legal professionals: automating
          routine tasks to save time, reduce administrative burden, and enhance
          overall case efficiency.
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
    backgroundImage:
      "url('https://www.acslaw.org/wp-content/uploads/2019/09/iStock-939262058.jpg')",
    backgroundSize: "cover",
    backgroundPosition: "center",
    color: "white",
    fontFamily: "'Garamond', serif",
    height: "100vh",
  },
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: "0 20px",
  },
  logo: {
    width: "500px", // adjust logo size here
    marginBottom: "-60px",
  },
  subheading: {
    fontSize: "36px",
    margin: "0 0 20px 0",
    fontWeight: "400",
  },
  paragraph: {
    fontSize: "24px",
    maxWidth: "700px",
  },
};

export default HomePage;