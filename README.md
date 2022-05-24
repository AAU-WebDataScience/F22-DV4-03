# F22-DV4-03
Repository for the project of group cs-22-dv-4-03

The goal of the project is to create a knowledge graph from the yelp dataset, using the rdf standard.
The yelp dataset is available at: https://www.yelp.com/dataset.

### How
The folder code_to_create_graphs contains Python code to create 5 graphs, corresponding to the .json files obtained from Yelp (follow above link). 
The rdflib package has been used to create N-Triples (.nt).

| Original (Yelp) | Outcome (Graph) | DB name                     |
| --------------- |:---------------:| ---------------------------:|
| Business.json   | biz.nt          |http://www.yelpkg.com/biz    |
| Review.json     | review.nt       |http://www.yelpkg.com/review |
| User.json       | user.nt         |http://www.yelpkg.com/user   |
| Tip.json        | tip.nt          |http://www.yelpkg.com/tip    |
| Checkin.json    | checkin.nt      |http://www.yelpkg.com/checkin|

### Who and Where
The project was developed by fourth semester students: 
<ul>
  <li>Marcus Muzhen Austin</li>
  <li>Storm King-Isager</li>
  <li>Flemming Steno Kjær</li>
  <li>Maja Pipaluk Ploumann</li>
  <li>Johnnie Pedersen</li>
</ul>

Under the supervision of:
<ul>
  <li> Matteo Lissandini https://people.cs.aau.dk/~matteo/ </li>
</ul>

During the spring of 2022.

### claaudia tutorial

https://git.its.aau.dk/CLAAUDIA/Compute_cloud_user_guides/src/branch/master/quick-start.md


### key

https://aaudk-my.sharepoint.com/:f:/g/personal/mausti20_student_aau_dk/EhgJLgDSifxPg73Qnso9y64BIf6IaFDdz_hFuNtMOiqX9w?e=OoP12N

### names of graphs
`http://www.yelpkg.com/tip`<br />
`http://www.yelpkg.com/review`<br />
`http://www.yelpkg.com/user`<br />
`http://www.yelpkg.com/biz`<br />
`http://www.yelpkg.com/checkin`
