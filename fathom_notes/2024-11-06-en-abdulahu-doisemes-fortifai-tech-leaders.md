---
title: 'DoisEmes + Fortifai: Tech leaders'
date: '2024-11-06T13:00:00.000000Z'
duration: 60m
participants:
- João
- En Abdulahu
source: https://fathom.video/calls/177446338
encoding: utf-8
scrapingdate: '2025-06-09T19:40:31.889241+00:00'
---

DoisEmes + Fortifai: Tech leaders - November 06
VIEW RECORDING - 57 mins (No highlights): https://fathom.video/share/BjcjEuYRCBkxP3ssxY-pCysiKZWnUMC6

---

0:04 - João Landeiro
  É, eu dividi as perguntas, tenho um papel com dois lados, perguntas mais técnico, técnico que ainda faz sentido para nós, não sei da arquitetura do sistema, qual é linguagem, não é sobre isso.  E outro lado, mais de co-founder, como eles apresentam, go-to-market, o que eles estão pensando, porque acho que isso pode nos ajudar a priorizar algumas coisas.  O when vai entrar. Tá. Hello, How are you?

0:44 - En Abdulahu (fortifai.co)
  Hello, guys. Good morning.

0:48 - João Landeiro
  Do you want to bring your AI note-taker as well, because we are making an AI note-taker party here? We could just maybe share the notes with us afterwards, that would be nice.

0:59 - En Abdulahu (fortifai.co)
  Yeah. We'll do it, let me.

1:02 - João Landeiro
  Hello.

1:03 - Ivan Ćelić
  Hello, Ivan. Hi, guys. Hello.

1:10 - En Abdulahu (fortifai.co)
  I think Abby is also trying to get in.

1:13 - João Landeiro
  Yeah, she's joining us, well. Hi, Abby. Hello, how are you?

1:24 - A L
  Good, good.

1:25 - João Landeiro
  Anya?

1:27 - A L
  I'm doing as well as I can with the last one, also. Oh, true, true that.

1:34 - João Landeiro
  We woke up to that here. So without further ado, I saw, I don't know, Abby, if you felt a bit weird about us just talking to Anne initially, we wanted to spare your agenda.  But since you can join, this is perfect.

1:56 - A L
  Yeah, no, it's good that I could join this line, also, too, on this. but also talking with Mustafa is hoping you could join, but I'm not sure if he's going to make it.  Okay, okay.

2:05 - João Landeiro
  So we've divided this conversation into segments. One of them is more about the technical aspects of Fortify. And when I say technical aspects, I think perhaps and even are thinking like way deeper than how far we are going to go.  But just we're mostly trying to understand limits to what can be done and what is faster to develop, what things are already made, components, that sort of thinking.  And the other side of the meeting is more around I'll call it like the go-to-market motions, like how do you, because we have this idea, we've been talking about this, so we are not a completely clean slate.  But how do you, which points of Fortify do you emphasize in a real conversation? and what kind of, we went through the benchmarks on Miro.  I have some notes here down here. And a lot of those mentioned specific things and there were a few that were more outliers that caught our attention.  So we might go into that. So, is this okay? we move? Yeah.

3:26 - En Abdulahu (fortifai.co)
  Of course.

3:27 - João Landeiro
  More technical aspects. From what you guys already have developed and have, I mean, everybody has complimented the speed of development.  So I guess you probably have a smart way of doing this that goes beyond just, you know, having a huge team.  So how are you in terms of like components and things that we can reuse and journeys we can slice and reposition?  How has this been for you? I'm not really good for now.

3:58 - Ivan Ćelić
  We don't have a, for the The design, we don't have a complete team and component setup, or at least not that I can see from the development side, from the design side, maybe there is.  I think the idea was to have something, but because of the pace of design and everything, we currently don't have it.  For example, I have no idea which three or four versions of buttons we have in the app. So I would like that be sorted in the next version and that type of stuff.  So we are using similar stuff all across the design right now, but it's not consistent. And I would say it's not done the usual way.

4:38 - A L
  I don't think everything was prioritized, But from what I understand, I think what we agreed with Rui and Pinar was that Kashin's going to another project now.  So she only has eight hours a week. And part of that eight hours a week, it's not necessarily developing flows, but to clean up these components and to clean up these little icons and everything so that they have it into a better wrap up.  I don't know how you spoke with Rui, but I think that was the plan.

5:05 - Ivan Ćelić
  Okay, okay, yeah. I'm not familiar with the plan there, but just as the current state, I see it. what I would prefer is to have a life normal and the usual way of doing it so that we have types of components that we can then also have it in our code.  In our code, to add this, in our code we have components. The previous version of the app we have a button setup.  We are using Manta in UI. This is just a library that gets us a bit of speed on some elements.  So it has buttons, selects and all of that. And we are styling that to fit the design. And that's been going okay for now.  Why do we have that? Well, we chose that like six or seven months ago before everything. So that's what we are rolling with right now.  So I would say that we can keep the current design language. I'm fine with that. a bit more consistency in the component than typography and all that usual stuff.  Could you just repeat the name?

6:08 - A L
  I'll write it.

6:11 - Ivan Ćelić
  There was another one that we bought two weeks ago. This is technical, this is component library that also comes with its own old style.  Then what Abby is mentioning is that SnowUI, I think, right, Abby, or something like that, that we are familiar with.

6:30 - A L
  those are two separate things, I would say.

6:33 - Ivan Ćelić
  I'm not sure if you understand what I'm trying to say here. Maintain your ICSS library.

6:41 - João Landeiro
  Like React, that sort of thing? Yeah.

6:45 - Ivan Ćelić
  mean, we take components and we get components from there and then we style them. We can style them. We don't have to style them.  That's the thing. So if they have, for example, autocomplete components, we take it and we style it and we get some early start on that because we don't to  code our own autocomplete logic because autocomplete has logic when you write text it pops up and all that stuff just There is I just want to say there is in the prototype file there's a page called local components that They are being used throughout the the tool.

7:19 - En Abdulahu (fortifai.co)
  Yes, so On terms of pin R and re cleaning up. This is already happening here. I would say Perfect.

7:29 - João Landeiro
  My point is because It's common that the figma takes one direction and development, you know Branches out and then we need to forcibly, you know, reconnect them.  So I saw that section, but Anyway, got it. I saw and as add the The hand up so That's what I wanted to mention.  That's okay. Oh more recently, so Uh, no, just reinforcing what I've said, uh, we talked to Rui and they're gonna they're not gonna  design system not at all, you know all the components but they are going to organize the treatment file and everything they have.  It's not going to be confusing on the treatment file now but they're going to clean up everything so we have a more specific direction to follow.  Okay, so on the, okay, Mentine got it, I received here on the Slack, thank you Ivan. And so we are using this Mentine.  Yeah, it's just a bonus fabric.

8:48 - Ivan Ćelić
  I don't think you need to worry about it because current design and everything they didn't look at this so I would say it's fine.  It will help us so if you need to see for, I don't know for example How we usually do it is designers can maybe take a look at how the components look and feel there and maybe slightly adjust them, but let's ignore that for now.  This is just so you know we are using that and that's fine, because design is not referencing that in any place.  let's let's not change things. Please let's let's continue. So SnowUI is like a big designer's library, and this library is more for us developers as a pre-built component that we can use and change.  That's different, just that we can stop it here for now. it, got it.

9:33 - João Landeiro
  And in terms of that, of these more functional aspects of it, less aesthetic ones, I understand, we can style them.  We have this toolbox of things that can be rearranged. Do we have any kind of list of components that are already done?  Because I assume that you're not using the entire Mantine thing and styling it all together. explain the question behind my question.  Maybe this is better. The point is, because of the speed imperative, if we know that some things are faster to develop, because you have done them before, they are more ready for production, we can try and adjust whatever flows we design to make use of what was already made.  This would, you know, get us some time. So this is what I'm thinking about. And because Figma and the development side, are separate entities, what I'm trying and the longer thing is actually translating the Figma to the development aspect.  If I can know what is ready on the development side, I can already think in terms of what flows can be faster to produce.  From component science, we don't have much.

10:49 - Ivan Ćelić
  We have lots of custom things, buttons and all that stuff was changed in lines, because usually we do the same way as you do it.  So we create components library, like the team and we style them and then we use them across the app, same way you do.  So we create the button with the four variants, same in Figma, and then we use it in places. That is not completed yet.  current element that we have in our code are all designs. The new design that we are applying is partial because we didn't have a team setup, so we didn't set it up.  I'm not sure maybe how to answer you the best, but the only components that we currently have in the new design are the ones that we are building the pages for, which will be policies flow for now.  Those are custom components, although some of them will appear. For example, NavBar is done, NavBar is done in the new example.  That's not something we have to think about anymore and top bar and that kind of stuff. Models, for example, we created models like yesterday or today and that's it.  That's all. Got it. Thank you very much.

12:00 - A L
  Because we are kind of, I know we haven't maintained from before, but we're really building it from scratch. Really, yeah, we kind of, we have one other product that's with another customer, a telenoir, but we've kind of, we started from scratch on all of this.  So it's really a month and a half old from when we talked to you. And then two weeks after we talked to you, we started building with the front-end designers.  everything is really new, I would say. It's like nothing truly set in stone. And it's, it's so, yeah. So that's just to let you know that, that like, yeah.  So you some flexibility there.

12:34 - João Landeiro
  Got it. Not far ahead with the new design implementation.

12:38 - Ivan Ćelić
  So, so if you have some, something that you want to update and it doesn't take much time, why not?  Okay, got it.

12:44 - João Landeiro
  So we're not to stack on that. Perfect. you. But policies flow is the thing that is the most ready.  So components that appear in the policies flow are, you know, yeah, easier to reuse.

12:55 - Ivan Ćelić
  Yes.

12:56 - João Landeiro
  And feel free, of course.

12:57 - Ivan Ćelić
  mean, when you will be building new pages, same as always. try to reuse things, doesn't have to be a specific thing but try to reuse everything as much as possible at least for the initial version and then later we can always expand things and add things and change things once we see how it behaves and how it reacts.  Perfect thank you thank you very much this helpful. So can you show us what's production ready perhaps so we get a feeling of production ready in what is production ready in the design or something you know in the development something we could perhaps take a look at even locally yes you can take a look at the policies do you have access to our test maybe and give you guys access to the test environment so you guys can log in and click around yourself and send the links and send the links it's like I think this gets lost after the call so thanks if I can click into it now but I don't know if you guys have a vlog yet Yes so regarding the production ready  The policies are not production-ready yet, so they are the first main feature that we are building, policies, trainings, and communication.  We have some pages currently with dummy data, like home, dashboard, and I think something else. So it's the screen?  Yeah, but regarding that, if you want, we can have a quick session, not while everyone is in here, and I can maybe show you around the app quickly.  I don't want to maybe waste everyone's time now. Basically, for production-ready, we don't have anything yet that's production-ready. We have something in production, but that's all design and being used by other companies, so I would say that's not relevant for this conversation.  Or if you want, I can also show you that, but that's all this time. because it will take like two seconds.

15:02 - A L
  It's not that much built, but just so that they have a picture of it.

15:05 - Ivan Ćelić
  It looks very similar to the Figma design.

15:08 - A L
  It's just one or two pages of that. So there hasn't been that much differentiation from there. So I'll be a log in.

15:18 - En Abdulahu (fortifai.co)
  There's also some that are in code review that are not here yet, which should be probably tomorrow.

15:31 - Ivan Ćelić
  Does it push even the policy view? No, there are some changes to fix, but it should be soon.

15:41 - En Abdulahu (fortifai.co)
  because I saw it yesterday on the front end guys.

15:53 - Ivan Ćelić
  Let me log in. I have to log in. Now it's asking me for password. I clicked the Microsoft sign-in and it's one's password, so it's...  I can't share this, but it was second. It's always the worst stuff that top-notch cards. Yes, always.

16:16 - João Landeiro
  Monday morning, first meeting of Let me know if you can see my screen. Yep, we do it.

16:22 - En Abdulahu (fortifai.co)
  Oh, good.

16:22 - Ivan Ćelić
  Yeah, great. This is dummy, but this is the layout that's built. And I think charts are styles, so we have chart styles, for example, implemented and these cards.  So this is built from the front-end side, but the back-end side is not yet built, because this page consists of a lot of different data.  So I think this will be one of the... Not last part, but after we build the features, then we will build this page, because this is like a data aggregation.  yeah, no point in building it without the initial data. And then this page is done. We still have the lag on the component.  Let's talk about it tomorrow morning on our daily and we can create a task and fix it, yeah. So compliance map page is done, I think, but that's the static page with the categories that design is done for that, it's implemented and here only a couple of links are not working for everything yet because not everything is implemented.  So here if you take a look at this compliance map, you can go back to the compliance map, please.  So we need to build all of these. currently we are working on the content area part, we are building policies and after that training and communication, they are all very similar and their design for that is ready and we are now well into policies building it.  The next one will be controls and then the stakeholder and blah blah all that other stuff so maybe you can open our policies.  now we are going to policy, this should be connected to the API. So this is... yeah so this is this is basically this is it so this is in code review when you click on this one the new model with the drawer with yeah with the actual policy text where you can then deploy it edit it and so on so yeah and then for the trainings it's slightly different and then communications is almost but it's literally copy-paste of this the smaller texts all the flows are the same only the content part so the policies will be a document the training will be a PDF if I'm not mistaken and then communication so everything else is the same the pages will feel the same so yeah that's that's the thing we are working on now and then once that is done once we have that flow for example completed also yeah and we have an employee view also in is it live  It is but I'm not sure if there will be any data because no one could release a poll deploy a policies that employee can see it You know, but yeah, and I'm not sure if you have employee account.  I do Yeah, you can try but basically Employee side of the views of you know, so the admin side of you.  We are also building at the same time Sorry Oh Sorry Verification code. Yeah, you can get it on your phone We should have this one set up through multiple people Yeah, probably okay never mind, but I can show it to them.  I can actually show it right now. I have it locally, but yeah, okay so Because I'm working on stuff.  So Basically here you will see this so same layout you can see that we are using same components. This is little bit spread out.  I'm on a big screen But we can also talk about the margins and stuff that's easily changeable. But you can see that this annual is different, policy training, submissions and homepage.  Homepage is also dummy data for now. But this one will be completely changed. is the old homepage. Yeah, this is the old one.  And the Figma.

20:20 - En Abdulahu (fortifai.co)
  Yeah, we have a new design in Figma.

20:22 - Ivan Ćelić
  And policies is now empty because I don't have any data here, but you saw how it looked like on the first click.  It will be the same rows and that's it basically. So lots of things are being built right now at the same time in parallel.  So hopefully soon we'll have some at least one feature like fully rounded and ready to show you. But this is like a big preview of everything.  Yeah, if you need, we can have a one on one session or one on with two or something with that one and two.  So to go a bit more details of each functionality. But yeah, this is like the summary where we are at currently.  So this is how it will look once finished.

21:00 - En Abdulahu (fortifai.co)
  the portal. You will have similar to the admin one, but it's just on their own tasks and then status of submissions and then make a submission.  This is the home page.

21:13 - Ivan Ćelić
  That might need to be updated because make a submission that's only for G.

21:17 - A L
  They'll probably be different like the submission to ES and GS. There might need to be a toggle or something or like this so we can change that later.

21:29 - João Landeiro
  Okay, thank you. Ivan, maybe that separate call could be interesting. I'll make the notes here, yeah.

21:38 - Ivan Ćelić
  Feel free to ping me whenever you need it. we can do it.

21:46 - João Landeiro
  Okay. So, when we present, when I say we, mean 425, when 425 presents, what's, no, the What's possible to do what do you rely right now?  Do you rely more on the presentation like PowerPoint sort of thing or do you rely more on? Interactive prototypes to show the vision of what's being built what do you use the most?

22:17 - A L
  think it depends on who the Audiences if it's somebody who knows the subject really well they they have it in their head and they understand what we're trying to But even even that like I find that having the prototypes and more helpful like I want to meet with called Mike Where she's a lawyer she kind of gets it But then when you actually visually see it they get it a lot more and they understand it So I think we did this also been surviving because we didn't have anything So if I've been having to talk around it and like and do that, but now that we have something It's a lot easier to get them to understand But I do think we need to clean that video up lot because it's like a three or five minute video that kind of goes Are not that exciting for some of the it's not used as a sales or just more to be the demo, but it's  that we have and ideally we have like what I'm really pushing for is that you know we have a big event coming up in two weeks that we have a flow that's actually working in our app that we can actually show them because it's starting to get embarrassing to be like oh here's a big time which is so better than what we had to you know two months ago we had nothing it was just an idea on my head now we have at least a big but now it's like okay we actually have a technology and we need to be to show up a workflow that we actually are developing so that's that's where we are and we are yeah so it's been but I think a lot of it we have been doing more warm I would say warm intros and so they when you have a warm intro warm connection you could do maybe more of the benefit of the doubt now we're going to be a cold outreach soon and then we need something a little bit more I would say set in that like you know something that's working that they can walk through and they can see what it is so that's the yeah I don't know if that answers your question but that's how bit it's been going and related to to that question or perhaps the question behind the question is

24:02 - João Landeiro
  Again, given the speed, the speed aspect, a lot of what we will be, you know, focusing on is figuring out where we can get the most impact, right, in the shortest amount of time.  And from that perspective, and a demo could have different approaches, right, we could have a broad, but relatively shallow demo, or we could have like a more of a deep demo into a specific journey.  From our past conversations, I have noted here that what we're aiming at right now is like the complete experience, right.  If, for instance, like for this two-week event, I assume that you want to show for the two-week event something working in the app, not just the Figma.

25:00 - A L
  But the specific thing of the app working, what's like the slice of things you want to show, Abby? I think it's the deployment of a policy, going from the science map to here's a policy, here's what a policy looks like.  I just dropped on the new text and put that new text, the policy I created, into there, deploy it, check it in employee portal.  Like one whole workflow, they really understand the process in which this works. tracking of the progress. Yeah, tracking the progress.  so just like one workflow down because then we can be like, look, this is how you do it, how simple it is to policy.  Just picture it with communication, with training, then people can actually understand that and visualize it. Romeo, I thought that was like a spin, like an octopus that just came out.

25:44 - En Abdulahu (fortifai.co)
  like, what's going on?

25:44 - A L
  I was also confused. It's just the tail and I was like, whoa, it's an octopus. But yeah, so that's what we hope.  But for you guys, I think I would like... we've done this really fast. I feel like we have a lot already for the engineering team to work with, whether it's policy procedures, trainings, control.  What we need from you guys is maybe a new look into what we're doing. Another thing I think is the trust, the integrity hub.  Part of it, we haven't looked at it, but I feel more and more that's gonna be important and that needs some creativity because that is where we kind of brag about what we do around there.  And I think we haven't given enough thought around that. But so like going into the workflows because I do feel that we went so fast, we might have missed something.  So to kind of think about that and we can catch it beforehand. And then there are some workflows such as the reporting and the auditing part, which I realized with reading the ISO ones that we also need to get started on because it's gonna be quite important actually to do the press audit is that we have the right documentation and audit trail.  So there are like rather than, I would say like, yeah. There's enough work outside of the development team is really moving forward on what the eggs did, because the rig developed so much.  But then we know that there's some missing parts within what the eggs have done. But also, there's just some part they haven't touched yet that we need to be able to create.

27:17 - En Abdulahu (fortifai.co)
  And I think we could also add a couple of elements to some of the things that we have created.  example, policies, we need to add some labels, because it's essential, for example, for ISO, that we label it as internal or external document.  And I think that can be done in the end, one of the final screens. So I think we need to just revise it a couple more times before we go live.  Yeah, so I think one of the questions for you guys is, what is easier or better for you?

27:48 - A L
  Is it better for like, I was talking to Mistoff about this too, because like I don't want to also, it's easier sometimes to kind of like, see where we went wrong after it's been developed.  I know it's like you're trying to get all the screens before. and exactly perfect before we start. I don't think that's possible in where we are and just the way that we work, but we have at least like 90, 95% of it, correct?  And I think in the process we're gonna find, in testing it with our 10 pilot customers, we're gonna get feedback.  Like it's a lot easier to test it with our pilots when they can actually see in the app and they actually try it and then we're gonna have that redraw a few things.  And for you guys to be part of those meetings, you can hear and see how they do it. So then, okay, we'll redraw some things so that Eva and then this team can put it into place.  So I think that's one aspect of it. So we're trying to get the development team out, but then the other aspect is with those missing pieces that we don't.  So I'd rather almost like build the missing ones like reporting, auditing, even like kind of the entrance page and settings, which we don't really have thought through along with the integrity hub.  If we can get those and then Eva and his team are building what's made with eggs and then we test those and then we update it as we see it in the next rounds in there.  So that's my thinking. But... Also, how you guys want to work to having seen everything.

29:06 - João Landeiro
  Thank you for this recap. I think it really helped me. what I've listed here is that there's kind of like three levels of things we could be working on right now.  the Brazilian team, let's say. So there's one aspect about fine tuning or improving or augmenting components, like what Anne mentioned, like we will need something about labels for documents.  It's like a very specific thing, very tactical thing. There's another level which is kind of what you've mentioned that you wanted a new look, is recheck some of the flows, which is more related to flows that are designed, with policies, training, communication.  And then there's the third level which is a little bit more ahead, which is the new stuff, right? So the integrity hub that there's like  An image of what it could look like, but I understand from what you're telling me that you would like to, you know Yeah, so the integrity have the report the auditing and the controls so this is like the new stuff that is Further ahead in the in the way we have the controls and risk assessment.

30:20 - A L
  That's that's what eggs is also going to do before they leave So what we're like where we're at zero is the recording board reporting and I realized more as I look at the ISO ISO there's We have to do a lot more reporting and like sign off by the board So that could be the reporting part and the audit part.  There's another box got audit So reporting reporting to management reporting to board and then auditing and then integrity have those are we haven't done anything?  Those four points we haven't done anything on which we're going to need to do And then take really have I think and maybe I might even need to be a strategic discussion on what do we want in that?  because that could that is That's the thing where customers used to kind of brag and that's also a place where  if they if we get it right and they want to use it to brag it's an automatic way where people know about us you know i mean because it's an link and they'll be like i'm using it and then people are like oh what is this we want it to so it's like kind of a critical sales and marketing tactic to also get right so in terms of strategy that can also help with our sales too to be able to like show it off so strategically i think that's an important one but then reporting and auditing and having everything drawn out would be good but i think um i think development team has enough to work with in terms of policies procedures trainings control and risk assessment over the next probably two months just to get those out so there is time i would say for you know the reporting and the other ones but i think but i think also during this period going back to question number one is that we will need to do a handover with our 10 pilots where we introduced you guys to the 10 pilots and they give feedback and in that feedback they might say like okay this flow doesn't work or i don't like this or i would like this  And then and then we might need to change things based on that. Yeah, that's good.

32:06 - Mau Medeiros (doisemes®)
  Thank you. Thank you so much.

32:07 - João Landeiro
  This was really illuminating Yeah, I think these are these are the these were the my most pressing questions We got to take a quick look at how it looks in terms of what's developed.  We got a some perspective on What kind of tooling and components are ready from the development side and we also understand that there's some nuance there And we got a clear Take on what's left to do, let's say On my side, I think I'd like to give us give this some some thought and get get back to you This independent of what was already discussed what was already discussed we we keep on doing  And for now I have no more questions.

33:02 - A L
  don't know if the rest of the Brazilian team has other questions No, I think we have just mentioned that you know going through everything was already developed and then in point Exactly what you like what you don't like, you know some comments and everything so that would help us to Understand how to work on it Sorry Like for me, I think it's more There's nothing that I don't really like from the design that there is one like when when the when the little boom enough person pops out I think it's that really bothers me But I think that like other than that like I don't really have any like design element So it's more like on your your design eye.  Is there anything that you know should change or something based off of that?

33:59 - Mau Medeiros (doisemes®)
  Otherwise I don't really

34:00 - A L
  have any strong opinion.

34:01 - Mau Medeiros (doisemes®)
  think it looks good.

34:02 - A L
  So like for me, I think it could be a little bit more fun, more poppy, like I think more on the integrity hub.  So I would say that like it could be good for my initial gut feeling would be for you guys to work on things that are not done yet, like reporting, auditing, integrity hub, because the more of that picture we can draw, the more that we can use it for sales, and the more that team will be ready to use.  And then there will be like a process of cleanup when we start going through the actual flows that are done with the customers and then know that we need to change it.

34:33 - Mau Medeiros (doisemes®)
  So I think that would be the best use of the time.

34:36 - A L
  And then also in order to understand, you know, the new parts, you need to understand the existing parts, right?  So going through the flows. So you see how it fits into the reporting. So ideally, I would like to be able to have a conversation with you guys next week where we like kind of discuss these four missing parts and say, you know, what would we like in it?  What does it look like? for you guys to like pick one of them and start like trying to wrap your heads around it.  Yeah, it's a little bit of a

35:00 - Mau Medeiros (doisemes®)
  you broad, when you you know, so just a new look. Yes. like an abstract, so it's good to us, because we have a very short of time to really grasp everything that should be done, so that's really good.  Yeah, I don't think we need a whole brand look.

35:18 - A L
  I think it's more, I'd like to look now, not that I'm not against, like, later on when we're working with you and, like, the product is more full than we really think about the whole brand look.  I know you guys have experience with that, but to find it on website, that's fine, but I think first we need to kind of develop most of the tool, like the missing parts of the tool that eggs can get to.  So I think that's what we need to build out first, and then kind of revise it based off of the development.  And we have just, we have just staffed up on development, and that's only recent. So that's why we're going to be able to go faster on the development, so it's also good timing for you guys to work on the reporting aspect of that.

35:56 - Mau Medeiros (doisemes®)
  So hopefully with this back, but we will go faster and then catch up too.

36:00 - A L
  the two-year part so that we can get that part developed. QuickR2.

36:06 - Mau Medeiros (doisemes®)
  Yeah, no problem. Thank you. That's good. I would have to produce this meeting. think all of the questions were very answered.  But I would have a very quick presentation. If you can present to us as the same way you presented to our new customers.  Just to run through for that, as you are selling to us.

36:36 - A L
  Yeah, we haven't really gotten ourselves processed, I would say, right. But I usually say that we're an end-to-end continuous ESG management tool that we use that enables you to be compliant without sustainability or compliance officers within eight to 12 weeks.  So we're very fast. And I often give an example of the difference between. sustainability reporting pool which is like once a year that you go in and spend all your money pushing it into a once a year tool and then you forget about it for six months and then you go in again and pull everything into a data so it becomes like a really expensive process on the company and very time-consuming and manual whereas if you use our product every day you do it and then you're not going to have this you're going to have the same result with less time and less money and then so I kind of always say like it's like if you're equivalent of financial reporting like you you put out an annual report once a year but every day you have control of your finances so it's the same thing for sustainability not just reporting once a year but every day you have control of what you're doing around sustainability so that's kind of how I sell it um so yeah that's been the kind of the main difference uh there I also like to say that we're creating a digital compliance or sustainability officer that anyone we turn anyone into a digital compliance officer regardless of their background

38:00 - En Abdulahu (fortifai.co)
  You can just follow everything in our tool and you'll be compliant whether you have knowledge on the matter or not everything is set up for you and you don't need to know anything you just follow the steps and we designed the software by experts so that our customers don't have to be experts.

38:18 - A L
  Yeah, and I think and like if you think about that we haven't really built that as well as we had hoped into the tool I think we went kind of fast.  That was a comment from one of our customers that way that doesn't know that much because it could be like a little bit more eyes you know with a circle with an eye on it that gives you a little bit more contact.

38:34 - Ivan Ćelić
  Information about it.

38:35 - A L
  Like information about this being like why are you doing this what does this actually mean I think we've kind of built it quickly so we're kind of missing that aspect of like that learning that teaching you that enabling you because I think the way that we built it quite quickly it's it's for people who kind of know what they're doing already but then maybe we would have to stand on the side and guide them you know for the ones who don't but eventually we would need to build into the tools and said that.  That would be some interesting that from you guys when you go through the tool if you notice anything like what is going on Just think this is run information button would be helpful to me because Ideally, we would want anyone to to understand what to do through the tool regardless if I have a designer Yeah, like I think yeah That's that's true because I think like if we we've been so fast It's like alright, let's get this out.  But like if you go anti bribery policy or discrimination policy, like what is that? Why do you have it?  Like, you know, why is it important, right? Like there's a there's a few aspects of that where I Realize when I was adding and it's creating communication that you just sent to the organization to kind of explain why we're doing this and all of that We haven't really built that into the tool, you know, like what does controls even mean?  And I don't like there should be an eye being like this is what a control is and some people don't know what controls are But we haven't done that pain of act yet because I think even with our pilots we're gonna be working so closely with them Hope you like press this button and then you  or at least say it, but eventually want to be a product-mode growth company that we need to be able to have that.

40:07 - Mau Medeiros (doisemes®)
  Yeah, for me for the, you know, the interface that we have right now, it has a completely new user or something like that.  I don't know anything about, you know, ASG, for example. I think what we have is pretty clear in terms of what we should do, in terms of the whole architecture.  I think it's very clear in terms of user interface, everything where everything is actually, and then have the main actors, so step-by-step what should be done.  Of course, know, this is going to pop up in many other windows, course. You know, in general terms, I would say that that's okay.  It seems to me, but we don't know that. You know, although our final goal is to become very... simple and less practical, it's still a very kind of form, you know, it's just checking, checking, checking.  I think one point where you're going to have something more like in terms of being more fun as I've already said, and not only it's just very bureaucratic, you know.  I'm thinking about, you know, our news that, you know, I don't have many, you know, much time to do that.  I'll go to the tool to be very fast and quick and very straight to the point. Maybe lots of readers will defend where I am, but this is something for the future for you to develop.  It's working for me.

41:53 - A L
  Yeah, and I think one of the things like policies procedures, I'm just like brainstorming as we talk about the timing because right now the team is working on policies.  these procedures training and it's probably going to take them November to do it, at least like including the training and completion part right.  So that part is like I feel like we shouldn't touch that too much but there is like control and assessment and like the next step that they're going to build or maybe they're going to start building some of them now that you can look at and see like okay how would you optimize them out because I agree with you I'm a little confused that it's like check check check check check check check like it's like it is a lot of forms a lot of different things and is there that we can make it more entertaining or that I'm not sure but it could be a good time to look at it I don't know if I control this too late so maybe it's around risk management and third party management those two for you guys to look at those and how to make those more entertaining I'm not sure before going into the next part but there is there is a lag right so there is a policy of training in cases too late if you're like those already you know the train has moved on this but there's other ones that the train hasn't moved on I think control is maybe  train has moved on to but I think maybe risk assessment at third party the train hasn't moved on those yet so there's a chance to change it as we did and those I would say risk assessment and risk assessment third party management those we spent probably the least amount of time on those are like one meeting we should have spent the most yeah like yeah that we should actually spending more time on so those could be actually ones that we start with and like kind of rethink the logic rethink the strategy around that and spend a little bit more time we have some good starting points from eggs now but we really maybe spent one or two meetings on those and those are probably more difficult ones maybe that could be a good place to start and like discuss and then and then see how it's in do you guys have any time tomorrow or Friday to book a meeting where we could go through one of them in more detail yeah I'm pretty flexible tomorrow I'm not that flexible tomorrow nor Friday

44:02 - João Landeiro
  We can figure this out, I can't. Tomorrow and Friday I cannot. I could also do it on Monday.

44:14 - A L
  Next week maybe like Romeo or Mal, I it's good for child to be there, so I think it could be good for Romeo and Mal for us to explain it, like if they either record it and explain it to you or you guys can look through it yourself together and try to click through it and see if you can figure it out yourself and like you know write some questions and then we can discuss it on Monday.  Mike does the, I would say just this assessment makes sense to you, does the third party part make sense to you because those are actually complex and we spent at least a amount of time on it.  So it could be good to just look at it on Thursday Friday and then we need on Monday to discuss it in more detail to be kind of an option.  Yeah it works for us.

44:56 - Mau Medeiros (doisemes®)
  I'm saying all of that because I'm, my role here is from a consumer perspective and that's what I mentioned, what I see from the, what we're talking about right now because marketing sales approach, we are saying that everything is going to be fun or everything is going to be easy.  So and then when people come to the platform, they might think it's easy, so that's something for the future to have it on the back of our mind in terms of the user experience.  Yeah, you guys know much more about, you know, us, but we are playing this role all the time.

45:43 - A L
  And I think that that's good. I think we're playing that role, like the usability of it, because technically you guys are our target, like you're not a subject matter expert so you find it difficult and you find it boring.  That's a good indication that everybody else is going to feel that way too. Like, you know, so I think we have more of a vested interest being like, oh, that doesn't work, then we still want to do it, but I think we're actually going to go for these customers.  Like we've seen, like, customer, think, and we saw that one, that GDPR tool where, like, the customer bought it and just never used it because he didn't know how to use it.  It was so difficult and that we don't want to become that because then people aren't going to really keep using our tool.  And that is one of our key goals is how to keep people using our tool because that's where compliance tool often go wrong, but they get so complex, people don't use it.  And then eventually, after not using it for a while, just touch on their prescription. So we want to engage them into using it.  And that's the same thing with, like, portal. I feel like we can make it more engaging, like, oh, you submitted a request, thanks for saving the earth.  You know, like something like fun about it, like that, like that engages them or motivates them to want to continue doing it, like a little bit of a learning aspect of it or a little bit of that thing so that it's not so boring.  So I think you guys can bring in some creativity to what we have. Absolutely.

46:54 - En Abdulahu (fortifai.co)
  One thing we forgot to think about in our tool is I use a similar tool for security.

47:00 - Mau Medeiros (doisemes®)
  It's called Sprinto and what I've noticed that I forgot to mention is that every day they send me an email of what my status is Every single day sometimes there's a lot for me to do sometimes I ignore it But the more I ignore it the more tasks they just keep bulking up I think that's something we should think like some kind of email Status email because that one is what keeps me going back to the tool If they didn't sign me that I'll probably forget who to ever go in there Yeah I'm thinking spirit on and I believe that you know in the future in terms of when you case them and learning process I'll say, you know a kind of approach is more like micro learning So using the tic-toc type, you know video to explain things very fast Yeah No I think that's actually like we actually did that in our first tool first iteration a year ago.

47:59 - A L
  We had like syphilis It's like an AI tool and we tried to do like learning and video clips. I'm kind of being like, why are we doing this?  What is third-party management instead of like an eye popping up? We would have a small video clip still open for that.  Maybe making even more fun like the Tik Tok or something like that. Absolutely. think that's a good idea. I forgot this in this round, but there was a period where we felt like, and this might be with like third-party investment.  The ones that we're going into now to have some context via video. Like, why do we do risk management?  What is, you know, that could be good and do it like kind of in a fun way. Totally open.  I think it's a good idea. Yeah.

48:35 - Mau Medeiros (doisemes®)
  I think I just based on the AI tool using the rig of AI right here. Instead of, you know, as I mentioned about heavy emails or messages or notifications, what the platform does like using AI to make a short video about the internet.  This is one thing. If they have a to-do list with a very fragmented part of the videos, one minute change, or is it a Mao-igu, you have to do this, and I'm reminding you to do that.  So it's a very, strong video. So I'm just thinking about how we can incorporate this in the future for this type of experience that should be easy and very fluid and everything.  So yeah, I'm thinking ahead.

49:31 - A L
  Sounds good. I think that's good.

49:34 - En Abdulahu (fortifai.co)
  Yeah.

49:34 - A L
  So I think maybe we should set up some time on Monday afternoon to go over a risk assessment or third party, one of the two.  I think it could be good for maybe Romeo this week just to go through like each of the sigma to see if we really understand it and the flow or maybe shall too.  And then especially around third party and this management before we leave on Monday because then you can have any questions that you have.  I just like them. on it. I don't know. Anne has Pinar finished all of those ones, but I know she was working on it.  then, I don't know where the status Is that a risk assessment or? Yeah, risk assessment and third party.

50:13 - En Abdulahu (fortifai.co)
  No. And she sent a status email, a status update on Monday in Slack that she will work on them later this week as she started a new project.  Yeah, so there might not be actually that much for you guys to look at.

50:30 - A L
  we're on third party.

50:33 - En Abdulahu (fortifai.co)
  There's some, I would say it's not a little, but the risk management, yeah, not so much.

50:40 - A L
  So maybe we must start with third party management then and look at third party management and then we can develop that more.  And then hopefully by the time we understand third party, then she'll have risk management further because that finishes the order with what we're doing anyway.  Do you guys have any time on? I don't know where you are and yeah and yeah we're all in the same time zone okay that's great okay so yeah this is the best this is the best window for us I think yeah well well do I have a meeting at one or two okay I just have my time difference here I'm yeah let's do 3 p.m then 3 p.m Monday that would be okay right to pop up through the meeting very nice and just wrapping up

53:07 - Mau Medeiros (doisemes®)
  I'll send an invite for this.

53:09 - João Landeiro
  All right.

53:12 - Mau Medeiros (doisemes®)
  Just to wrap up here, we are going to talk about everything that we've seen today and then make a plan.  Of course, we have a meeting on Monday to go through everything in more detail. But we are also going to do the next steps for the team at least the next weeks to be very productive.  that's something I'm going to go back to you as much as possible. another request that I have is like, even though it's not finished or it's not well done and everything.  So I would like you to choose to send to us your keynote presentation as a selling tool, if you have it, or anything you use for selling.  that we have. Yeah, that's fine.

54:09 - A L
  I think for it, like it would be ideal, like if we did, because like the way that we are working with eggs was like we were almost able to do a flow every two weeks, but I think with third party management, because it's already half done, it's just like more expanding on it that we can spend like next week, like if we meet on Monday, then we'll meet, I don't know if we have time next week, like to put some hours in, so then on Friday we can get farther ahead, and then the same thing with like risk management, you know, do it the following Monday, it's already half done, so by two weeks we kind of have more of a flow on those two, and then that could also go into like the integrity hub.  think it's a, I think those, at least for planning, those are good like first ones to start with, and then by then you'll get a hang of it, you'll have a better understanding of what it's going to take for the other parts of it too.  for branding, for visual guidance, or anything which is enough for you. We do have a visual guide from our web designer, but it's more on our website, not necessarily around our tool because she made it before our tool was made.  So we don't have one. I think that's something that should probably come out of this project. It's like, once you understand the tool and all of the different things, how are we going to update our website to match our tool and our messaging to match the tool.  You know, and I think we have to have more pictures of our tool on the website. So I think it's all underway, versus to get a tool that we can kind of use and show and start selling and then building a brand around that.  I think it's okay for my side to have anything.

55:44 - Mau Medeiros (doisemes®)
  No, it's good.

55:45 - João Landeiro
  good. I'll send the notes and a recap of what we've discussed. Perfect. Thank you very much.

55:54 - A L
  Feel free to just ping us if there's anything, guys, any questions or like any access.

56:00 - En Abdulahu (fortifai.co)
  And just one more thing, sorry.

56:03 - Mau Medeiros (doisemes®)
  Could you send us again for me and the patient for the check? it's just like, I don't know, we couldn't get that.  So if you send us... Which one? slide? The slide, please. Okay, sure.

56:20 - En Abdulahu (fortifai.co)
  Yeah. I know you got it.

56:23 - A L
  Yeah.

56:24 - En Abdulahu (fortifai.co)
  You've been talking on slide.

56:28 - João Landeiro
  That's it.

56:28 - A L
  Thank you very much.

56:30 - Mau Medeiros (doisemes®)
  Thank you. Bye-bye. Bye-bye.