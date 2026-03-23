import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

const features = [
  {
    title: 'ROS 2 & Navigation',
    icon: '🤖',
    description:
      'Master ROS 2 nodes, topics, services, actions, DDS middleware, and the Nav2 navigation stack for autonomous humanoid robots.',
  },
  {
    title: 'RAG AI Chatbot',
    icon: '💬',
    description:
      'Every page has a built-in AI assistant powered by Retrieval-Augmented Generation. Select any text and ask questions in context.',
  },
  {
    title: 'NVIDIA Isaac Platform',
    icon: '🌐',
    description:
      'Isaac Sim for physics-accurate simulation, Isaac ROS for hardware-accelerated perception, Isaac Lab for RL-based locomotion training.',
  },
  {
    title: 'VLA Models',
    icon: '⚡',
    description:
      'Vision-Language-Action models: RT-2, OpenVLA, π0. Train and deploy on Jetson Orin Nano for real-world humanoid control.',
  },
  {
    title: 'Simulation: Gazebo & Unity',
    icon: '📋',
    description:
      'Build sim environments in Gazebo Harmonic and Unity Robotics Hub. Master sim-to-real transfer for Unitree G1/H1 robots.',
  },
  {
    title: 'Physical AI Hardware',
    icon: '🚀',
    description:
      'Hands-on with Jetson Orin Nano (40 TOPS), RTX 4090/5090 GPUs, and Unitree G1/H1 humanoid robots via Python SDK.',
  },
];

const chapters = [
  { num: '01', title: 'Introduction to AI-Native Dev', desc: 'The paradigm shift powering the next generation of robotics engineers.', color: '#6366f1' },
  { num: '02', title: 'Spec-Driven Dev & Prompting', desc: 'Structured specs, prompt engineering, and the AI-Native workflow.', color: '#8b5cf6' },
  { num: '03', title: 'Architecture & Data Pipelines', desc: 'RAG, agent loops, vector stores, and model integration patterns.', color: '#06b6d4' },
  { num: '04', title: 'Testing & Monitoring', desc: 'Evaluation frameworks, observability, and the feedback flywheel.', color: '#10b981' },
  { num: '05', title: 'Emerging Patterns & Teams', desc: 'VLA models, multimodal AI, agents as OS, and AI-Native culture.', color: '#f59e0b' },
];

const stats = [
  { value: '5', label: 'Chapters' },
  { value: 'ROS 2', label: 'Framework' },
  { value: 'RAG', label: 'AI Chatbot' },
  { value: 'VLA', label: 'Models' },
];

function HomepageHeader(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroBackground}>
        <div className={styles.heroOrb1} />
        <div className={styles.heroOrb2} />
        <div className={styles.heroGrid} />
      </div>
      <div className={clsx('container', styles.heroContent)}>
        <div className={styles.heroBadge}>
          <span>✨ Panaversity Hackathon 1 — Built with Docusaurus</span>
        </div>
        <Heading as="h1" className={styles.heroTitle}>
          {siteConfig.title}
        </Heading>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <p className={styles.heroDescription}>
          Master Physical AI and Humanoid Robotics — from ROS 2 and NVIDIA Isaac to VLA models deployed
          on Jetson Orin Nano and Unitree G1/H1 robots. Built with Docusaurus as an AI-Native interactive textbook.
        </p>
        <div className={styles.heroButtons}>
          <Link className={styles.btnPrimary} to="/docs/intro">
            📖 Start Reading
          </Link>
          <Link className={styles.btnSecondary} to="/docs/chapter-01/topic-01">
            Chapter 1 →
          </Link>
        </div>
        <div className={styles.heroStats}>
          {stats.map(s => (
            <div key={s.label} className={styles.statItem}>
              <span className={styles.statValue}>{s.value}</span>
              <span className={styles.statLabel}>{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}

function FeatureCard({title, icon, description}: {title: string; icon: string; description: string}): JSX.Element {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIconWrap}>
        <span className={styles.featureIcon}>{icon}</span>
      </div>
      <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
      <p className={styles.featureDesc}>{description}</p>
    </div>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <HomepageHeader />

      <main>
        {/* Features */}
        <section className={styles.featuresSection}>
          <div className="container">
            <div className={styles.sectionHeader}>
              <Heading as="h2" className={styles.sectionTitle}>Everything You Need</Heading>
              <p className={styles.sectionSubtitle}>A comprehensive guide covering Physical AI, Humanoid Robotics, ROS 2, NVIDIA Isaac, and VLA Models</p>
            </div>
            <div className={styles.featuresGrid}>
              {features.map(feat => (
                <FeatureCard key={feat.title} {...feat} />
              ))}
            </div>
          </div>
        </section>

        {/* Chapters */}
        <section className={styles.chaptersSection}>
          <div className="container">
            <div className={styles.sectionHeader}>
              <Heading as="h2" className={styles.sectionTitle}>What You Will Learn</Heading>
              <p className={styles.sectionSubtitle}>Five chapters taking you from AI-Native fundamentals to deploying VLA models on humanoid robots</p>
            </div>
            <div className={styles.chaptersGrid}>
              {chapters.map((ch, i) => (
                <Link key={ch.num} to={`/docs/chapter-${ch.num}/topic-01`} className={styles.chapterCard}>
                  <div className={styles.chapterNumber} style={{color: ch.color}}>
                    {String(i + 1).padStart(2, '0')}
                  </div>
                  <div className={styles.chapterBar} style={{background: ch.color}} />
                  <strong className={styles.chapterTitle}>{ch.title}</strong>
                  <p className={styles.chapterDesc}>{ch.desc}</p>
                  <span className={styles.chapterArrow} style={{color: ch.color}}>Read →</span>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className={styles.ctaSection}>
          <div className="container">
            <div className={styles.ctaCard}>
              <div className={styles.ctaOrb} />
              <Heading as="h2" className={styles.ctaTitle}>Ready to Build Physical AI?</Heading>
              <p className={styles.ctaSubtitle}>
                Start with the introduction and work through all five chapters — from AI-Native fundamentals
                to deploying VLA models on Unitree humanoid robots. The RAG chatbot is ready to help on every page.
              </p>
              <div className={styles.ctaButtons}>
                <Link className={styles.btnPrimary} to="/docs/intro">
                  Get Started Free
                </Link>
                <Link className={styles.btnGhost} to="/docs/chapter-01/topic-01">
                  Jump to Chapter 1
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
