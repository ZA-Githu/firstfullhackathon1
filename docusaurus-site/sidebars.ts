import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Sidebar configuration for AI-Native Development Book.
 * Each chapter is a category with two topic pages.
 */
const sidebars: SidebarsConfig = {
  bookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: Introduction to AI-Native',
      link: { type: 'doc', id: 'chapter-01/chapter-01' },
      items: [
        'chapter-01/topic-01',
        'chapter-01/topic-02',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: The AI-Native Workflow',
      link: { type: 'doc', id: 'chapter-02/chapter-02' },
      items: [
        'chapter-02/topic-01',
        'chapter-02/topic-02',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: Architecture and Data',
      link: { type: 'doc', id: 'chapter-03/chapter-03' },
      items: [
        'chapter-03/topic-01',
        'chapter-03/topic-02',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: Quality and Operations',
      link: { type: 'doc', id: 'chapter-04/chapter-04' },
      items: [
        'chapter-04/topic-01',
        'chapter-04/topic-02',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5: The Future and the Team',
      link: { type: 'doc', id: 'chapter-05/chapter-05' },
      items: [
        'chapter-05/topic-01',
        'chapter-05/topic-02',
      ],
    },
  ],
};

export default sidebars;
