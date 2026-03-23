"use client";

import { useState } from "react";
import { saveWaitlistEntry } from "@/lib/localStorage";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

type FormState = "idle" | "saving" | "success" | "success_with_warning";

interface FieldErrors {
  name?: string;
  email?: string;
}

export function WaitlistForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [state, setState] = useState<FormState>("idle");

  function validate(): FieldErrors {
    const errs: FieldErrors = {};
    if (!name.trim()) errs.name = "Name is required.";
    if (!email.trim()) {
      errs.email = "Email is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = "Please enter a valid email address.";
    }
    return errs;
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    setErrors({});
    setState("saving");

    const result = saveWaitlistEntry({ name: name.trim(), email: email.trim(), message: message.trim() || undefined });

    if (result.success) {
      setState("success");
    } else {
      setState("success_with_warning");
    }
  }

  if (state === "success" || state === "success_with_warning") {
    return (
      <div className="rounded-2xl border border-white/20 bg-white/5 backdrop-blur-sm p-8 text-center space-y-4">
        <div className="text-5xl">🎉</div>
        <h2 className="text-2xl font-heading font-bold gradient-text">
          You&apos;re on the list!
        </h2>
        <p className="text-muted-foreground">
          Thanks for joining. We&apos;ll be in touch when the book is ready.
        </p>
        {state === "success_with_warning" && (
          <div className="rounded-lg border border-amber-500/40 bg-amber-500/10 p-3 text-sm text-amber-700 dark:text-amber-300">
            Your entry may not have been saved because your browser has storage
            restrictions enabled. Try disabling private browsing mode.
          </div>
        )}
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-6">
      {/* Name */}
      <div className="space-y-1.5">
        <Label htmlFor="name">
          Name <span aria-hidden="true" className="text-red-500">*</span>
        </Label>
        <Input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          aria-required="true"
          aria-describedby={errors.name ? "name-error" : undefined}
          aria-invalid={!!errors.name}
          placeholder="Your name"
          className="bg-white/5 border-white/20 focus:border-primary-500"
        />
        {errors.name && (
          <p id="name-error" role="alert" className="text-sm text-red-500">
            {errors.name}
          </p>
        )}
      </div>

      {/* Email */}
      <div className="space-y-1.5">
        <Label htmlFor="email">
          Email <span aria-hidden="true" className="text-red-500">*</span>
        </Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-required="true"
          aria-describedby={errors.email ? "email-error" : undefined}
          aria-invalid={!!errors.email}
          placeholder="you@example.com"
          className="bg-white/5 border-white/20 focus:border-primary-500"
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-sm text-red-500">
            {errors.email}
          </p>
        )}
      </div>

      {/* Message */}
      <div className="space-y-1.5">
        <Label htmlFor="message">Message (optional)</Label>
        <Textarea
          id="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="What are you most excited to learn?"
          rows={4}
          className="bg-white/5 border-white/20 focus:border-primary-500 resize-none"
        />
      </div>

      <Button
        type="submit"
        disabled={state === "saving"}
        className="w-full bg-gradient-button hover:opacity-90 text-white font-semibold py-3 rounded-xl transition-opacity"
      >
        {state === "saving" ? "Saving…" : "Join the Waitlist →"}
      </Button>
    </form>
  );
}
