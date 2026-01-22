---
title: Middlewares
---

When you're building a Telegram bot, you often end up repeating the same setup, checks, or clean‑up code across many handlers. Middleware helps you avoid that. It lets you plug in common logic around your handlers, so your main code stays clean, focused, and easier to maintain.

Here’s how middleware works in *telegram‑bot*, and how you can use it in your own projects.

---

############### “What is Middleware?” (in simple terms)

Think of middleware like a security guard + reporter + helper that stands in three places along the path of each update:

1. **Before anything happens**
2. **Right before your handler runs**
3. **After your handler finished**

You can attach code to each of those moments to do things like check if someone is allowed, modify the data, log what’s going on, or clean up afterward.

---

############### The Three Hook Points & Why They’re Useful

Here are the three hooks (*points you can attach middleware*) in *telegram‑bot*, and what they let you do:

| Hook           | When it runs                                                                          | What you can use it for                                                                                                                                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **preHandle**  | As soon as the update arrives, **before** the library picks which handler should run  | ✔ Filter out irrelevant updates (spam, malformed, etc.) <br>✔ Global checks: is user banned? Is the message coming from a channel you support? <br>✔ Logging: “Hey, got this update” <br>✔ Setup shared context (e.g. user data you’ll need later)                                              |
| **preInvoke**  | After deciding *which* handler should run, but just before calling it                 | ✔ Handler‑specific conditions (maybe some handlers require special permissions) <br>✔ Enriching the update for that handler (e.g. parse arguments) <br>✔ Starting timers / metrics for how long the handler takes <br>✔ If something is missing, you might cancel here (don’t call the handler) |
| **postInvoke** | After the handler is done (whether success or failure), just before returning control | ✔ Log what happened: success / error, time taken <br>✔ Clean up resources opened in preInvoke <br>✔ If the handler threw an error, handle it here (send fallback message, etc.) <br>✔ Maybe modify the result before sending reply or finishing                                                 |

---

############### Real‑Life Example

Here’s a short imaginary example showing how middleware could help:

Suppose you have a bot that responds to commands, but only certain users are allowed to run some commands, and you also want to measure how long each command takes, plus log every command usage.

You might set up middleware like this:

* In **preHandle**: reject the update if the user is banned (don’t bother doing anything else).
* In **preInvoke**: check if the user has permission for *this specific handler*. If not, send “You’re not allowed”. Also start a timer.
* In **postInvoke**: stop the timer, record how long the handler took. If there was an exception, send an error message and log stack trace.

This keeps your handler code very simple: “Here’s what I’m supposed to do when everything is good”.

---

############### Some Tips & Best Practices

* Only do what needs to happen at *each* stage: don’t overload `preHandle` or `postInvoke` with everything. It helps keep things predictable.

* Order matters! If you have multiple middleware, the order in which `preHandle` and `preInvoke` run has a big effect. Make sure more general checks happen first, more specific ones later.

* Clean up after yourself — if you open resources or timers in `preInvoke`, do the matching cleanup in `postInvoke`, even if something went wrong.

* Use middleware for things that are “shared logic” — auth, logging, metrics, filtering. For code that’s specific to one handler, usually keep it in the handler.

* Make sure errors are handled gracefully in middleware. If a middleware throws, downstream code or the bot runtime should still behave in a controlled way, not crash.
