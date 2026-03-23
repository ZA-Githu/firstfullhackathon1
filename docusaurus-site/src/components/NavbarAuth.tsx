import React from 'react';
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from '@clerk/clerk-react';
import styles from './NavbarAuth.module.css';

/**
 * Error boundary so the navbar doesn't crash when ClerkProvider is absent
 * (i.e. no valid publishable key is set in .env.local).
 */
class ClerkErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): { hasError: boolean } {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) return null;
    return this.props.children;
  }
}

function AuthButtons(): JSX.Element {
  return (
    <div className={styles.authWrapper}>
      <SignedOut>
        <div className={styles.authButtons}>
          <SignInButton mode="modal">
            <button className={styles.signInBtn}>Sign In</button>
          </SignInButton>
          <SignUpButton mode="modal">
            <button className={styles.signUpBtn}>Get Started</button>
          </SignUpButton>
        </div>
      </SignedOut>
      <SignedIn>
        <div className={styles.userRow}>
          <UserButton afterSignOutUrl="/" />
        </div>
      </SignedIn>
    </div>
  );
}

export default function NavbarAuth(): JSX.Element {
  return (
    <ClerkErrorBoundary>
      <AuthButtons />
    </ClerkErrorBoundary>
  );
}
