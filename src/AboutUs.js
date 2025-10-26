import React from "react";
import teamPhoto from "./assets/IMG_7825.jpg";

function AboutUs() {
  return (
    <section style={styles.container}>
      <h1 style={styles.heading}>About Us</h1>
      <img src={teamPhoto} alt="Our team" style={styles.image} />
      <p style={styles.paragraph}>
        Welcome to Lawgic! We hope this website helps streamline your legal communications and 
        provides a glimpse into how AI can support professionals in their work. We are Rosie, Jenna, 
        and Katrina — computer science students at the University of Central Florida. This project is
         our very first hackathon creation, and it marks the beginning of our journey in computer science. 
         We built Lawgic to challenge ourselves, explore new technologies, and apply our learning in a 
         practical, real-world project. We are excited to continue developing our skills and sharing 
         innovative solutions with the world.
      </p>
    </section>
  );
}

const styles = {
  container: {
    padding: "80px 20px",
    fontFamily: "'Garamond', serif",
    lineHeight: 1.6,
    maxWidth: "1200px",
    margin: "0 auto",
    textAlign: "left",
    backgroundColor: "#1b3099ff",
    color: "white", 
  },
  heading: {
    fontSize: "36px",
    marginBottom: "20px",
  },
  image: {
    float: "right",
    width: "300px",
    height: "auto",
    margin: "0 0 20px 20px",
    borderRadius: "10px",
  },
  paragraph: {
    fontSize: "18px",
  },
};

export default AboutUs;