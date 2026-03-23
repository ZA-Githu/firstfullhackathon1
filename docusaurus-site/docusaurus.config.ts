import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  customFields: {
    // Publishable key is safe to expose in frontend (it's designed to be public)
    clerkPublishableKey: process.env.REACT_APP_CLERK_PUBLISHABLE_KEY || 'pk_test_anVzdC1pYmV4LTE3LmNsZXJrLmFjY291bnRzLmRldiQ',
  },
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'The AI-Native Interactive Textbook on Physical AI, Humanoid Robotics, ROS 2, NVIDIA Isaac, and VLA Models',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // GitHub Pages deployment URL
  url: 'https://your-github-username.github.io',
  baseUrl: '/ai-native-book/',

  // GitHub Pages deployment config
  organizationName: 'your-github-username',
  projectName: 'ai-native-book',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: { label: 'English', direction: 'ltr' },
      ur: { label: 'اردو', direction: 'rtl' },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/your-github-username/ai-native-book/tree/main/docusaurus-site/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Textbook Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: '/',
          label: 'Home',
          position: 'left',
          activeBaseRegex: '^/$',
        },
        {
          type: 'docSidebar',
          sidebarId: 'bookSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          to: '/about',
          label: 'About',
          position: 'left',
        },
        {
          to: '/contact',
          label: 'Contact',
          position: 'left',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/your-github-username/ai-native-book',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'custom-clerk-auth',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Textbook',
          items: [
            { label: 'Introduction', to: '/docs/intro' },
            { label: 'Chapter 1 — AI-Native Dev', to: '/docs/chapter-01/topic-01' },
            { label: 'Chapter 2 — Spec-Driven Dev', to: '/docs/chapter-02/topic-01' },
          ],
        },
        {
          title: 'More Chapters',
          items: [
            { label: 'Chapter 3 — Architecture', to: '/docs/chapter-03/topic-01' },
            { label: 'Chapter 4 — Testing & Monitoring', to: '/docs/chapter-04/topic-01' },
            { label: 'Chapter 5 — Emerging Patterns', to: '/docs/chapter-05/topic-01' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'GitHub', href: 'https://github.com/your-github-username/ai-native-book' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
