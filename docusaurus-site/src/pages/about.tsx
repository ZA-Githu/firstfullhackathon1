import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './about.module.css';

export default function About(): ReactNode {
  return (
    <Layout title="About" description="About the Physical AI & Humanoid Robotics Textbook">
      <main className={styles.aboutPage}>
        <div className="container">
          <div className={styles.hero}>
            <div className={styles.badge}>📖 About This Textbook</div>
            <Heading as="h1" className={styles.title}>
              Physical AI & Humanoid Robotics
            </Heading>
            <p className={styles.subtitle}>
              An AI-Native interactive textbook built for Panaversity Hackathon 1 — entirely on Docusaurus.
            </p>
          </div>

          <div className={styles.grid}>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🎯</div>
              <Heading as="h3">Mission</Heading>
              <p>Make Physical AI and humanoid robotics accessible to every engineer — from ROS 2 fundamentals to deploying VLA models on real humanoid hardware.</p>
            </div>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🛠️</div>
              <Heading as="h3">Tech Stack</Heading>
              <p>Built with <strong>Docusaurus</strong> for the frontend, <strong>FastAPI</strong> for the backend, <strong>Qdrant</strong> for vector search, and <strong>Cohere</strong> for embeddings and generation.</p>
            </div>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🤖</div>
              <Heading as="h3">AI Features</Heading>
              <p>RAG chatbot for every page, selected-text mode, TextbookMasterAgent with 5 reusable skills, Urdu translation, and personalised content by experience level.</p>
            </div>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🌍</div>
              <Heading as="h3">Multilingual</Heading>
              <p>Full English and Urdu (اردو) support. Switch languages using the dropdown in the navbar. Technical terms are preserved in English even in Urdu mode.</p>
            </div>
          </div>

          <div className={styles.hardware}>
            <Heading as="h2">Hardware Covered</Heading>
            <div className={styles.hwGrid}>
              <div className={styles.hwItem}><span>🔧</span><strong>Jetson Orin Nano</strong><p>40 TOPS · 8 GB RAM · Edge AI inference</p></div>
              <div className={styles.hwItem}><span>💻</span><strong>RTX 4090 / 5090</strong><p>24 GB VRAM · Isaac Sim · Local training</p></div>
              <div className={styles.hwItem}><span>🦾</span><strong>Unitree G1 / H1</strong><p>Full-body humanoid · Python SDK · Locomotion</p></div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
