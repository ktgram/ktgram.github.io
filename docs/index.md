---
title: Index
---

# Intro
Let's get an idea of how the library handles updates in general:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/442cc5f1-0256-425a-9f25-185fdd49fe0a" alt="Handling process diagram" />
</p>

After receiving an update, the library performs three main steps, as we can see.

# Processing

Processing is to repackage the received update into the appropriate subclass of [`ProcessedUpdate`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.types.internal/-processed-update/index.html) depending on the payload being carried.

This step is needed to make it easier to operate the update and to extend the processing capabilities.

# Handling

Next comes the main step, here we get to the handling itself.

## Global RateLimiter

If there is a user in the update, we check for exceeding the global rate limiter.

## Parse text

Next, depending on the payload, we take a particular update component containing text and parse it according to the configuration.

More detailed you can see in [update parsing article](/Update-parsing).

## Find Activity

Next, according to the processing priority:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/6178c410-9b9e-4045-9f03-4791b3f49894" alt="Handling priority diagram" />
</p>

We are looking for a correspondence between the parsed data and the activities we are operating on.
As we can see on the priority diagram, `Commands` always come first.

I.e. if the text load in the update corresponds to any command, further search for `Inputs`, `Common` and of course execution of the `Unprocessed` action will not be performed.

The only thing is that if there is a `UpdateHandlers` will be triggered in parallel regardless.

### Commands

Let's take a closer look at the commands and their processing.

As you may have noticed, although the annotation for processing commands is called [`CommandHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-command-handler/index.html), it is more versatile than the classic concept in Telegram Bots.

#### Scopes

This is because it has a wider range of processing possibilities, i.e. the target function can be defined not only depending on the text match, but also on the type of a suitable update, this is the concept of scopes.

Accordingly, each command can have different handlers for a different list of scopes, or vice versa, one command for several.

Below you can see how mapping by text payload and scope is done:

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/c870027e-750e-4bb8-a2ed-45ad93a55875" alt="Command scope diagram" />
</p>

### Inputs

Next, if the text payload does not match any command the input points are searched.

The concept is very similar to input waiting in commandline applications, you put in the bot context for a particular user a point that will handle his next input, it doesn't matter what it contains, the main thing is that the next update has a `User` to be able to relate it to the set input waiting point.

Below you can see an example of processing an update when there is no match on `Commands`.

<p align="center">
  <img src="https://github.com/vendelieu/telegram-bot/assets/3987067/925d3e05-0985-43d5-8d6f-b3f2786ff212" alt="Priority example diagram" />
</p>

### Commons

If the handler finds no `commands` or `inputs`, it checks the text load against `common` handlers.

We advise to use it without abuse, since it checks doing iteration over all entries.

### Unprocessed

And the final step, if the handler doesn't find any matching activity ([`UpdateHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-update-handler/index.html) works completely in parallel and don't count as usual activity), then the [`UnprocessedHandler`](https://vendelieu.github.io/telegram-bot/telegram-bot/eu.vendeli.tgbot.annotations/-unprocessed-handler/index.html) comes into play, if it is set, it will handle this case, it may be useful to warn the user that something has gone wrong.

More detailed read in [Handlers article](/Handlers).

## Activity RateLimiter

After finding an activity, it also checks the user's rate limits on it, according to the parameters specified in the activity parameters.

# Activity

Activity refers to the different types of handlers the telegram bot library can handle, including Commands, Inputs, Regexes, and the Unprocessed handler.

# Invocation

The final processing step is the invocation of the found activity.

More details can be found in the [invocation article](/Activity-invocation).

# See also

* [Update parsing](/Update-parsing)
* [Activity invocation](/Activity-invocation)
* [Handlers](/Handlers)
* [Bot configuration](/Bot-configuration)
* [Web starters (Spring, Ktor)](/Web-starters-(Spring-and-Ktor))