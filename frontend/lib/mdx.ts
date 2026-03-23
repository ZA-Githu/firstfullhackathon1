import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { Chapter, Topic } from "@/types";

/** Directory containing all MDX chapter files */
const CHAPTERS_DIR = path.join(process.cwd(), "content", "chapters");

/**
 * Reads a single MDX file and returns frontmatter + raw content string.
 * @param filename - e.g. "chapter-01-topic-01.mdx"
 */
function readMdxFile(filename: string): {
  data: Record<string, unknown>;
  content: string;
} {
  const filePath = path.join(CHAPTERS_DIR, filename);
  const raw = fs.readFileSync(filePath, "utf8");
  const { data, content } = matter(raw);
  return { data, content };
}

/**
 * Returns all 10 topics sorted by chapterNumber, then topicNumber.
 * Each topic includes the raw MDX content string.
 */
export async function getAllTopics(): Promise<Topic[]> {
  const filenames = fs
    .readdirSync(CHAPTERS_DIR)
    .filter((f) => f.endsWith(".mdx"))
    .sort();

  const topics: Topic[] = filenames.map((filename) => {
    const { data, content } = readMdxFile(filename);

    const chapterNumber = Number(data.chapterNumber);
    const topicNumber = Number(data.topicNumber);

    return {
      chapterNumber,
      topicNumber,
      title: String(data.title ?? ""),
      description: String(data.description ?? ""),
      slug: String(data.slug ?? ""),
      content: content.trim(),
      // Anchor ID format: ch{C}-t{T}
      anchorId: `ch${chapterNumber}-t${topicNumber}`,
    };
  });

  // Sort by chapterNumber ASC, then topicNumber ASC
  return topics.sort((a, b) =>
    a.chapterNumber !== b.chapterNumber
      ? a.chapterNumber - b.chapterNumber
      : a.topicNumber - b.topicNumber
  );
}

/**
 * Returns all 5 chapters, each with their 2 topics, sorted by chapterNumber.
 */
export async function getAllChapters(): Promise<Chapter[]> {
  const topics = await getAllTopics();

  // Group topics by chapterNumber
  const chapterMap = new Map<number, Topic[]>();
  for (const topic of topics) {
    const existing = chapterMap.get(topic.chapterNumber) ?? [];
    chapterMap.set(topic.chapterNumber, [...existing, topic]);
  }

  const chapters: Chapter[] = [];
  for (const [chapterNumber, chapterTopics] of chapterMap) {
    // Derive chapter metadata from the first topic's data
    // (chapter title comes from the chapter title field if present, else we generate it)
    const firstTopic = chapterTopics[0];

    // Read chapter-level metadata: we store a chapterTitle in each MDX file
    // For now, use a mapping based on chapterNumber
    const chapterTitles: Record<number, string> = {
      1: "The AI-Native Paradigm",
      2: "Designing with AI",
      3: "Building AI-Native Systems",
      4: "Shipping and Scaling",
      5: "The Future of AI-Native Development",
    };

    const chapterDescriptions: Record<number, string> = {
      1: "Understand what makes a software system truly AI-native and how it differs from traditional development.",
      2: "Learn spec-driven workflows and prompt engineering techniques that define AI-native teams.",
      3: "Explore architecture patterns, data pipelines, and model integration strategies.",
      4: "Master testing, monitoring, and observability for AI-native systems in production.",
      5: "Discover emerging tools and how to build the teams that will shape the future.",
    };

    chapters.push({
      chapterNumber,
      title: chapterTitles[chapterNumber] ?? `Chapter ${chapterNumber}`,
      description:
        chapterDescriptions[chapterNumber] ??
        firstTopic.description,
      slug: `chapter-0${chapterNumber}`,
      topics: chapterTopics,
    });
  }

  return chapters.sort((a, b) => a.chapterNumber - b.chapterNumber);
}

/**
 * Returns the raw MDX source string for a single topic by slug.
 * Returns null if the file does not exist.
 */
export async function getTopicContent(slug: string): Promise<string | null> {
  const filename = `${slug}.mdx`;
  const filePath = path.join(CHAPTERS_DIR, filename);

  if (!fs.existsSync(filePath)) {
    return null;
  }

  const { content } = readMdxFile(filename);
  return content.trim() || null;
}
