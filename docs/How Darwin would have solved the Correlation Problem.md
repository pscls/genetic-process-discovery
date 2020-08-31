_A small introduction into the world of discovering unknown patterns and finding correlations by following the laws of nature - Darwinism: survival of the fittest._

In our daily life, we are surrounded by processes. Most of our everyday actions follow a certain pattern. For instance, everyone has a personal morning routine. Companies follow certain patterns as well. Those patterns are often described as so-called business process models. Those business process models can help to support the business with an IT-infrastructure. This helps companies to improve their processes, reduce planning overheads and increase their production.

![Process Meme](https://www.mememaker.net/api/bucket?path=static/img/memes/full/2019/Apr/18/18/process-meme-128238.png)

A company can run into problems though. If the defined process models and the actual patterns during the executed process mismatch, errors, and miscommunication emerge. The modeled behavior and actual behavior can diverge. Reasons can be workarounds that employees prefer or simply edge cases that could not be modeled.
Thankfully, there is a solution to this problem. It is called process mining. Process mining does what the name says. It 'mines' processes. In the deep caves of information storage, data can be cut out of the databases. This data holds all the information that was executed during a process in the form of transactions or so-called events. If we now can look at all the events that were read and written, we should be able to solve the puzzle of which events belong together and represent a former process execution.
However, this puzzle is not as easy as it sounds. It is called the correlation problem and has caused a lot of work for process miners to this day.
In the following, we want to address the correlation problem, give some insights into how it can be solved. And we will show how nature and Darwin can help with this problem.

<!--
Our world runs on and with processes, especially the IT-supported businesses. For every situation, we need to make a decision in terms of reaction to it. These reactions are often defined by a company's internal process for example. Others are not defined at all since they maybe never have been thought about before due to their small possibility of occurrence or it is simply a situation where we need to decide fast based on our experience and gut feeling. Nevertheless understanding the decision process and therefore the lived process is extremely important for companies to enable them to improve their structure regarding time and cost. Unfortunately, this is often not straightforward and requires work and a lot of effort to come up with an idea of how the reality looks like if even possible. Everybody knows the saying: Never change a running system. So instead of changing software and infrastructure (which usually cost more time and problems than planned) let's simply estimate the case identifiers if we are not able to extract them. 
-->

<!---
![Process Meme](https://media.makeameme.org/created/what-process-do.jpg)
![Process Meme](https://www.mememaker.net/api/bucket?path=static/img/memes/full/2019/Apr/18/18/process-meme-128238.png)
![Process Meme](https://images.squarespace-cdn.com/content/v1/5ba00ef485ede1fd4588b22d/1551469786947-NC49BVBL0QMHDQV5M7A9/ke17ZwdGBToddI8pDm48kBzTjOOxrLdK_5cUhOu5Bw5Zw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpxdTwfbQLUVN9QrwM_X1xLfYY8gDfcS05gR5XlJzlhnIexeEZJAvzBDG1BGvyy6dmE/process+meme.jpg?format=750w)
-->
### Blog Aim
I will explain the following three key areas:
1. Understanding the Correlation Problem
1. A brief introduction to the estimation process
1. How Nature can help us here

<!--
### A off-the-cuff introduction into Process Mining -->

### What is the Correlation Problem on a real-life example
Getting an idea of how a system is used and operated by employees is a good starting point of a company's business process improvement procedure since this data is required to improve software (or even automate it with bots - robotic process automation). Do get this data user interaction needs to be recorded in event logs - this procedure is called UBM (user behavior mining). In ERP (Enterprise-Resource-Planning) systems the business object (e.g. an invoice) gets used often as the case identifier which can often be extremely difficult or even impossible to come up with at the beginning during the tracking process. Having the right case identifier for an event is indispensable to continue with the process analysis. Companies often run on an old on-premise system (e.g. S4/Hana with SAP Gui) or use complex technologies like server-side frontend rendering (e.g. SAP Screen Personas). Those systems are not build to serve the needed data easily and thus updates or bigger adjustments would often be needed to reach the required result. Updating or completely changing a company's underlaying system for this purpose is probably 100% impossible and therefore we need to go a different way - read further if you want to know how.

### A brief introduction to the estimation process

Let us now get our hand dirty! Let us now assume that we could retrieve some events and also could retrieve their order from databases in our company. We now have a so-called unlabeled event log. It consists of ordered event labels. That is all the information we get. Now we try to estimate, what event to start with and what event is respectively the next. If our events types are named as 'A', 'B', 'C', ... then it could look like the following.

<img width="400" alt="image" src="https://user-images.githubusercontent.com/32839252/91727182-94fb9880-eba1-11ea-9331-d5c5c1316306.png">

Let us now assume that we somehow know how likely it is that one event follows any other event. This information can be displayed in a probability matrix often referred to as Markov chain. For our event types 'A', 'B', 'C', ..., a probability matrix could look like this:

<img width="300" alt="image" src="https://user-images.githubusercontent.com/32839252/91726758-0d158e80-eba1-11ea-8fd3-8be26ed7bbb5.png">

We can now apply some rules that describe, which event to assign to which trace. A new event is assigned to the trace, of which last event has the highest probability of being followed by this new event. If the new event never follows another event, a new trace is created (like for _A_ in our case). If it is never followed by any event, then the trace is finished.

![estimation](https://user-images.githubusercontent.com/32839252/91723071-7db9ac80-eb9b-11ea-9db5-37dfad7e6d36.gif)

Now we can extract our traces. But wait! Didn't we miss the point of creating our probability matrix? Well, the matrix can simply be generated by looking at our unlabeled event log and setting in relation how often the direct successorship of two event occurs with how often they occur at all. With that, we have an idea of how likely two events are to be successors.
Doing this only once leads to not so great results, but we can estimate a new matrix from the occurrences within the estimated traces. This gives an even better estimation on how likely two events succeed.
The steps of computing a new matrix and estimating traces is done iteratively until the traces won't change any more.

<img width="600" alt="image" src="https://user-images.githubusercontent.com/32839252/91737764-cd09d800-ebaf-11ea-9f46-acaf19d1a6da.png">

With that procedure, we are able to estimate traces and case IDs and generate our event log in the end.
<!--
2. Describe briefly the base algorithm and its idea/theory behind it
- Different Approaches exist, problem: restrictions, assumptions and moderate results
- The aim is to improve one of those approaches
- Idea: estimation based on direct successorship, iteratively improve estimations
- present approach:
- estimate a probability matrix
-- estimate Case IDs
- estimate Matrix again
- ...
- visualization
-->

### How Nature can help
<!-- 3. Describe genetic programing and the extension to it -->

Now we want to try to improve the approach from before. Help comes from mother nature. The genetic programming paradigm provides rules and techniques that aim to find a programmatic solution with concepts from evolution. As the first evolutionary theorist, Charles Darwin described one main factor of evolution as natural selection -- simply said the strongest individuals will slowly replace the weakest ones. We use the selection in our procedure as well. This is not done naturally as Darwin described, but with the use of a fitness function that gives us an indication of the fitness of an individual (probability matrix and the derived trace). Thus, instead of training only one model, we are working with multiple ones. After each generation we use the best ones for reproduction where we create the next generation offsprings to replace the weakest ones of the current generation. Another idea, which comes from looking and the nature, is the mutation where we randomly change features in offsprings, as it happens in reality as well, to increase the chance of an higher estimation accuracy.

The fitness function has to evaluate how good a matrix represents the actual process. But, as you might remember, we do not know anything about the actual process. That is why we need process mining in the first place. So, how can a function evaluate how well a matrix represents a process that we do not know?
The answer is quite simple. As the genetic approach is running on multiple matrices, we can evaluate a matrix against all the other matrices. And as all should represent the actual process well, a matrix should receive a high fitness score if it represents many other matrices good as well.
The fitness function compares a matrix against each of the other matrices and evaluates how fit it is in the average by taking the average consensus to all other available matrices. A matrix that is fitter in average will get a higher ranking and thus a high chance of survive the selection process in this generation. So in our case, the consensus of all models is an indicator for high fitness. Getting the similarity, percentual equivalence, between two matrices by using their estimated traces was already defined for us. What a luck! So we were able to reuse it and simply average the consensus between all pair of matrices. That is all we needed here.

is done by using the estimated traces from both and computing the 

Like in nature, only the fittest matrices are then reproduced. 
Again, in analogy to nature, matrices can also be mutated, which means small changes of values. This can lead to a worse, or in some cases to an even better matrix as a solution candidate.

<img width="600" alt="image" src="https://user-images.githubusercontent.com/32839252/91738111-4e616a80-ebb0-11ea-83f6-488d8a82cae4.png">

We implemented this approach and compared the results of the genetic extension to the original approach which makes the core of our approach as well. The fitness metric that was used compares the probability of traces of the estimation and the probability of traces of a process model that was used for evaluation. From this model, events were generated, for which we executed the correlation discovery. The results are then comparable to the actual process.

<img width="300" alt="base" src="https://github.com/pscls/genetic-process-discovery/blob/master/docs/images/base_evaluation.png">

<img width="295" alt="genetic" src="https://github.com/pscls/genetic-process-discovery/blob/master/docs/images/genetic_evaluation_1.jpg">

The results of the genetic approach are pretty similar to the original. But, if you look closely they seem to be slightly inferior.
Yet, there is no need to abandon the idea of genetic programming. Genetic algorithms are very sensible in regards to their hyperparameters. Small differences in the number or strength of mutations, for instance, can have a huge impact on the algorithms' performance. Often, it is quite difficult to find the best configuration. We did not find it yet, also because experiments that try to find a suiting configuration take very long. There is still some time and work needed to show better results.

Also, the genetic approach opens up a broad field of possible extensions. Over time, this makes it possible to overcome some of the made assumptions.
This allows us to handle multiple different recordings from the same process with different start points for example. Doing that increases the accuracy tremendously as it can be seen here.
<img width="300" alt="genetic_2" src="https://github.com/pscls/genetic-process-discovery/blob/master/docs/images/genetic_evaluation_2.jpg">

### Summary

The goal was to either improve the the accuracy of the base algorithm or soften the made assumptions - both by extending it with a genetic procedure. We did not achieve either of them, but provided a working extension that enable further research and already shows potential to be far better if tweaked and tuned correctly. While our accuracy is even slightly inferior we have paved the way for different possible points of improvements by being capable of running multiple models simultaneously. Overall we are quite confident that this approach has the potential to outperform the base algorithm and dispose some of its assumptions. 

You got interested in this topic? Then take a look at our [documentation](https://github.com/pscls/genetic-process-discovery/blob/master/docs/Genetic%20Correlation%20Discoveryfor%20Unlabeled%20Event%20Logs.pdf) or simply try it on your own with the provided code in this [repository](https://github.com/pscls/genetic-process-discovery) right now!

Written by _Pascal Schulze_ and _Anjo Seidel_


<!--

***

The goal is to open your research to a broader audience. Ask yourself
“How would I explain topic XY to my grandparents?”. For that, use
meaningful (real-world) examples and figures. If you include code, keep
it simple. 

Further, use a format of your choice, like a nice formatted Word
document, Markdown, or HTML page. The blog should not exceed 4 pages,
including figures.

But most important, do not copy your paper!

1.1 Show why process discovery, in general, can help you, example driven
- For a business without knowledge about the underlying processes, it can be helpfull to extract processes in order understand the process, for enhancements and for conformance checking.
- Example

1.2 Start with an example and show the problem in a practical way
- Usage information needed improve (and automate) enterprise software
- Record user interaction in logs → User Behavior Mining
- “ERP Systems use the Business objects as the case identifier” [1] 
- What if it is extremely difficult or even impossible to identify the Business objects?
- companies often have old running on-premise systems (SAP Gui) → difficult 
- frontend gets rendered on server (SAP Screen Personas) → extremely difficult or impossible
- Updates or bigger Adjustments would be needed to get desired result

2. Describe briefly the base algorithm and its idea/theory behind it
- Differen Approaches exist, problem: rescrictions, assumptions and moderate results
- Aim is to improve one of those approaches
- Idea: estimation based on direct successorship, iteratively improve estimations
- present approach:
- estimate a probability matrix
-- estimate Case IDs
- estimate Matrix again
- ...
- visualization

3. Describe genetic programing and the extension to it


-->
