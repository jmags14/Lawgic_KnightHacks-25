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
    alignItems: "center", // centers vertically
    padding: "0 30px",
    backgroundColor: "#1a1a1a",
    color: "white",
    height: "60px", // 👈 fixed height for the bar
    position: "sticky",
    top: 0,
    zIndex: 10,
  },
  logo: {
    fontSize: "35px", // 👈 make logo text bigger
    fontWeight: "bold",
    lineHeight: "1", // 👈 prevents extra spacing
    fontFamily: "'Garamond', serif",
  },
  links: {
    display: "flex",
    gap: "20px",
    listStyle: "none",
    cursor: "pointer",
  },
};

export default NavBar;