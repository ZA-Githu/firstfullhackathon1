import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './about.module.css';

export default function About(): ReactNode {
  const {i18n} = useDocusaurusContext();
  const isUrdu = i18n.currentLocale === 'ur';

  return (
    <Layout title={isUrdu ? "تعارف" : "About"} description={isUrdu ? "Physical AI & Humanoid Robotics ٹیکسٹ بک کے بارے میں" : "About the Physical AI & Humanoid Robotics Textbook"}>
      <main className={styles.aboutPage}>
        <div className="container">
          <div className={styles.hero}>
            <div className={styles.badge}>{isUrdu ? "📖 اس ٹیکسٹ بک کے بارے میں" : "📖 About This Textbook"}</div>
            <Heading as="h1" className={styles.title}>
              {isUrdu ? "فزیکل اے آئی اور ہیومنائیڈ روبوٹکس" : "Physical AI & Humanoid Robotics"}
            </Heading>
            <p className={styles.subtitle}>
              {isUrdu 
                ? "ایک AI-Native انٹرایکٹو ٹیکسٹ بک جو Panaversity Hackathon 1 کے لیے بنائی گئی ہے — مکمل طور پر Docusaurus پر۔"
                : "An AI-Native interactive textbook built for Panaversity Hackathon 1 — entirely on Docusaurus."}
            </p>
          </div>

          <div className={styles.grid}>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🎯</div>
              <Heading as="h3">{isUrdu ? "مشن" : "Mission"}</Heading>
              <p>{isUrdu 
                ? "Physical AI اور humanoid robotics کو ہر انجینئر کے لیے قابل رسائی بنانا — ROS 2 بنیادی باتوں سے لے کر حقیقی humanoid ہارڈویئر پر VLA models deploy کرنے تک۔"
                : "Make Physical AI and humanoid robotics accessible to every engineer — from ROS 2 fundamentals to deploying VLA models on real humanoid hardware."}</p>
            </div>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🛠️</div>
              <Heading as="h3">{isUrdu ? "ٹیک اسٹیک" : "Tech Stack"}</Heading>
              <p>{isUrdu 
                ? (<><strong>Docusaurus</strong> فرنٹ اینڈ کے لیے، <strong>FastAPI</strong> بیک اینڈ کے لیے، <strong>Qdrant</strong> ویکٹر سرچ کے لیے، اور <strong>Cohere</strong> embeddings اور generation کے لیے۔</>)
                : (<>Built with <strong>Docusaurus</strong> for the frontend, <strong>FastAPI</strong> for the backend, <strong>Qdrant</strong> for vector search, and <strong>Cohere</strong> for embeddings and generation.</>)}</p>
            </div>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🤖</div>
              <Heading as="h3">{isUrdu ? "AI فیچرز" : "AI Features"}</Heading>
              <p>{isUrdu 
                ? "ہر صفحے پر RAG chatbot، منتخب-ٹیکسٹ موڈ، 5 reusable skills کے ساتھ TextbookMasterAgent، اردو ترجمہ، اور تجربے کی سطح کے مطابق ذاتی مواد۔"
                : "RAG chatbot for every page, selected-text mode, TextbookMasterAgent with 5 reusable skills, Urdu translation, and personalised content by experience level."}</p>
            </div>
            <div className={styles.card}>
              <div className={styles.cardIcon}>🌍</div>
              <Heading as="h3">{isUrdu ? "کثیر لسانی" : "Multilingual"}</Heading>
              <p>{isUrdu 
                ? "مکمل انگریزی اور اردو (اردو) سپورٹ۔ Navbar میں ڈراپ ڈاؤن کا استعمال کرتے ہوئے زبانیں تبدیل کریں۔ تکنیکی اصطلاحات کو اردو موڈ میں بھی انگریزی میں محفوظ رکھا گیا ہے۔"
                : "Full English and Urdu (اردو) support. Switch languages using the dropdown in the navbar. Technical terms are preserved in English even in Urdu mode."}</p>
            </div>
          </div>

          <div className={styles.hardware}>
            <Heading as="h2">{isUrdu ? "شامل ہارڈویئر" : "Hardware Covered"}</Heading>
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
