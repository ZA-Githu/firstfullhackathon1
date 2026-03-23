import React from 'react';
import { ClerkProvider } from '@clerk/clerk-react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatBot from '@site/src/components/ChatBot';

/**
 * Root theme component — wraps every Docusaurus page.
 * Provides ClerkProvider for auth + injects the AI chatbot widget.
 *
 * Add your Clerk Publishable Key to docusaurus-site/.env.local:
 *   REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxx
 */
export default function Root({ children }: { children: React.ReactNode }): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const clerkKey = siteConfig.customFields?.clerkPublishableKey as string | undefined;

  // Only wrap with ClerkProvider when a real key is configured
  const hasValidKey = clerkKey && clerkKey.startsWith('pk_') && clerkKey !== 'pk_test_placeholder';

  if (hasValidKey) {
    return (
      <ClerkProvider publishableKey={clerkKey}>
        {children}
        <ChatBot />
      </ClerkProvider>
    );
  }

  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}
