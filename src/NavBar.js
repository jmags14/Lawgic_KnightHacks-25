import React from "react";

function NavBar() {
  return (
    <nav style={styles.nav}>
      <h2 style={styles.logo}>Lawgic</h2>
      <ul style={styles.links}>
        <li>Home</li>
        <li>AI Legal Assistant</li>
        <li>About Us</li>
      </ul>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 30px",
    backgroundColor: "#1a1a1a",
    color: "white",
  },
  logo: { fontSize: "1.5rem", fontWeight: "bold" },
  links: { display: "flex", gap: "20px", listStyle: "none", cursor: "pointer" },
};

export default NavBar;