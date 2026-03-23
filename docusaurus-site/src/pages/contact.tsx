import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './contact.module.css';

export default function Contact(): ReactNode {
  return (
    <Layout title="Contact" description="Contact us about the Physical AI & Humanoid Robotics Textbook">
      <main className={styles.contactPage}>
        <div className="container">
          <div className={styles.hero}>
            <div className={styles.badge}>✉️ Get In Touch</div>
            <Heading as="h1" className={styles.title}>Contact Us</Heading>
            <p className={styles.subtitle}>Questions about the textbook, the AI chatbot, or Physical AI in general? We'd love to hear from you.</p>
          </div>

          <div className={styles.grid}>
            <div className={styles.formCard}>
              <Heading as="h2">Send a Message</Heading>
              <form className={styles.form} onSubmit={e => e.preventDefault()}>
                <div className={styles.field}>
                  <label>Name</label>
                  <input type="text" placeholder="Your name" />
                </div>
                <div className={styles.field}>
                  <label>Email</label>
                  <input type="email" placeholder="your@email.com" />
                </div>
                <div className={styles.field}>
                  <label>Subject</label>
                  <input type="text" placeholder="What is this about?" />
                </div>
                <div className={styles.field}>
                  <label>Message</label>
                  <textarea rows={5} placeholder="Your message..." />
                </div>
                <button type="submit" className={styles.submitBtn}>Send Message →</button>
              </form>
            </div>

            <div className={styles.infoCol}>
              <div className={styles.infoCard}>
                <div className={styles.infoIcon}>🎓</div>
                <Heading as="h3">Panaversity</Heading>
                <p>This textbook is built for Panaversity Hackathon 1 — AI-Native Interactive Textbook on Physical AI & Humanoid Robotics.</p>
              </div>
              <div className={styles.infoCard}>
                <div className={styles.infoIcon}>💬</div>
                <Heading as="h3">Use the AI Chatbot</Heading>
                <p>For questions about textbook content, use the RAG chatbot on any chapter page — it's faster and smarter than email.</p>
              </div>
              <div className={styles.infoCard}>
                <div className={styles.infoIcon}>🐛</div>
                <Heading as="h3">Found a Bug?</Heading>
                <p>Open an issue on GitHub. Include the page URL, what you expected, and what you saw.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
