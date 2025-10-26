import React from "react";

function AboutUs() {
  return (
    <section style={styles.container}>
      <h3>About Us</h3>
      <p>
        Lawgic was built to help legal professionals and teams craft clear,
        empathetic, and compliant communications. Our AI assistant ensures
        messages maintain professionalism while saving time and effort.
      </p>
    </section>
  );
}

const styles = {
  container: {
    padding: "40px 20px",
    backgroundColor: "#eee",
    textAlign: "center",
    fontFamily: "'Garamond', serif", 
  },
};

export default AboutUs;