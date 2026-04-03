import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './contact.module.css';

export default function Contact(): ReactNode {
  const {i18n} = useDocusaurusContext();
  const isUrdu = i18n.currentLocale === 'ur';

  return (
    <Layout title={isUrdu ? "رابطہ کریں" : "Contact"} description={isUrdu ? "Physical AI & Humanoid Robotics ٹیکسٹ بک کے بارے میں ہم سے رابطہ کریں" : "Contact us about the Physical AI & Humanoid Robotics Textbook"}>
      <main className={styles.contactPage}>
        <div className="container">
          <div className={styles.hero}>
            <div className={styles.badge}>{isUrdu ? "✉️ رابطہ کریں" : "✉️ Get In Touch"}</div>
            <Heading as="h1" className={styles.title}>{isUrdu ? "ہم سے رابطہ کریں" : "Contact Us"}</Heading>
            <p className={styles.subtitle}>
              {isUrdu 
                ? "ٹیکسٹ بک، AI chatbot، یا عمومی Physical AI کے بارے میں سوالات؟ ہم آپ سے سننا پسند کریں گے۔"
                : "Questions about the textbook, the AI chatbot, or Physical AI in general? We'd love to hear from you."}
            </p>
          </div>

          <div className={styles.grid}>
            <div className={styles.formCard}>
              <Heading as="h2">{isUrdu ? "پیغام بھیجیں" : "Send a Message"}</Heading>
              <form className={styles.form} onSubmit={e => e.preventDefault()}>
                <div className={styles.field}>
                  <label>{isUrdu ? "نام" : "Name"}</label>
                  <input type="text" placeholder={isUrdu ? "آپ کا نام" : "Your name"} />
                </div>
                <div className={styles.field}>
                  <label>{isUrdu ? "ای میل" : "Email"}</label>
                  <input type="email" placeholder={isUrdu ? "آپ کا ای میل" : "your@email.com"} />
                </div>
                <div className={styles.field}>
                  <label>{isUrdu ? "موضوع" : "Subject"}</label>
                  <input type="text" placeholder={isUrdu ? "یہ کس بارے میں ہے؟" : "What is this about?"} />
                </div>
                <div className={styles.field}>
                  <label>{isUrdu ? "پیغام" : "Message"}</label>
                  <textarea rows={5} placeholder={isUrdu ? "آپ کا پیغام..." : "Your message..."} />
                </div>
                <button type="submit" className={styles.submitBtn}>{isUrdu ? "پیغام بھیجیں →" : "Send Message →"}</button>
              </form>
            </div>

            <div className={styles.infoCol}>
              <div className={styles.infoCard}>
                <div className={styles.infoIcon}>🎓</div>
                <Heading as="h3">Panaversity</Heading>
                <p>{isUrdu 
                  ? "یہ ٹیکسٹ بک Panaversity Hackathon 1 کے لیے بنائی گئی ہے — Physical AI & Humanoid Robotics پر AI-Native انٹرایکٹو ٹیکسٹ بک۔"
                  : "This textbook is built for Panaversity Hackathon 1 — AI-Native Interactive Textbook on Physical AI & Humanoid Robotics."}</p>
              </div>
              <div className={styles.infoCard}>
                <div className={styles.infoIcon}>💬</div>
                <Heading as="h3">{isUrdu ? "AI Chatbot کا استعمال کریں" : "Use the AI Chatbot"}</Heading>
                <p>{isUrdu 
                  ? "ٹیکسٹ بک کے مواد کے بارے میں سوالات کے لیے، کسی بھی chapter کے صفحے پر RAG chatbot کا استعمال کریں — یہ ای میل سے تیز اور زیادہ ہوشیار ہے۔"
                  : "For questions about textbook content, use the RAG chatbot on any chapter page — it's faster and smarter than email."}</p>
              </div>
              <div className={styles.infoCard}>
                <div className={styles.infoIcon}>🐛</div>
                <Heading as="h3">{isUrdu ? "کوئی Bug ملا؟" : "Found a Bug?"}</Heading>
                <p>{isUrdu 
                  ? "GitHub پر issue کھولیں۔ صفحے کا URL شامل کریں، آپ نے کیا توقع کی تھی، اور آپ نے کیا دیکھا۔"
                  : "Open an issue on GitHub. Include the page URL, what you expected, and what you saw."}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
