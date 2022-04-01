# OoT-Graph-Model
A project to craft a game graph for Ocarina of Time.

The constructed graph is supposed to act as a basis for algorithmic
speedrun modeling and routing approaches.

The verbose-ocarina-parser sub-project takes a text dump of OoT scenes from mzxrules' Verbose Ocarina tool
and translates all actor, spawn and transition actor data to CSV files.

The oot-graph-builder sub-project then takes these CSV files to produce a game graph model.
All actors inside one room are aggregated to one complete sub-graph and then connected through the transition actors.
Scene transitions are only implemented exemplary and manually yet.
Save, Death, Song and Blue Warps are added.
Model is only concerned with Glitchless runs for now.

## References for the interested

Concepts are mainly based on this paper: https://arxiv.org/abs/2106.01182

### A paper on algorithmical Mega Man speedrun optimization

Manuel Lafond. “The Complexity of Speedrunning Video Games.” In: 9th
International Conference on Fun with Algorithms (FUN 2018). Ed. by Hiro
Ito et al. Vol. 100. Leibniz International Proceedings in Informatics (LIPIcs).
Dagstuhl, Germany: Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik,
2018, 27:1–27:19. doi: [10.4230/LIPIcs.FUN.2018.27](https://doi.org/10.4230/LIPIcs.FUN.2018.27).

### A very cool guide on algorithmically optimizing Morrowind all factions

Artjoms Iškovs. Travelling Murderer Problem: Planning a Morrowind All-Faction
Speedrun with Simulated Annealing. Apr. 18, 2018. url: https://www.kimonote.com/@mildbyte/travelling-murderer-problem-planning-a-morrowind-all-faction-speedrun-with-simulated-annealing-part-1-41079/

### An also very cool guide to optimize TrackMania through an evolutional algorithms

JstAnothrVirtuoso, director. Finding the Optimum Nadeo Cut... With Science!! May 28, 2019. url: https://www.youtube.com/watch?v=1ZsAjvO9E1g






[The speedroute project by hzck](https://github.com/hzck/speedroute) as well as [this project by gdaaronson](https://github.com/gdaaronson/Thesis) have been good inspirations as well.

