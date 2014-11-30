var college_list = {"All Souls": "all-souls.png",
                    "Balliol": "balliol.png",
                    "Blackfriars": "blackfriars.png",
                    "Brasenose": "brasenose.png",
                    "Campion Hall": "campion-hall.png",
                    "Christ Church": "christ-church.png",
                    "Coprus Christi": "coprus-christi.png",
                    "Exeter": "exeter.png",
                    "Green Templeton": "green-templeton.png",
                    "Harris Manchester": "harris-manchester.png",
                    "Hertford": "hertford.png",
                    "Jesus": "jesus.png",
                    "Keble": "keble.png",
                    "Kellog": "kellogg.png",
                    "Lady Margaret": "lady-margaret-hall.png",
                    "Linacre": "linacre.png",
                    "Lincoln": "lincoln.png",
                    "Magdalen": "magdalen.png",
                    "Mansfield": "mansfield.png",
                    "Merton": "merton.png",
                    "New": "new.png",
                    "Nuffield": "nuffield.png",
                    "Oriel": "oriel.png",
                    "Pembroke": "pembroke.png",
                    "Queens": "queens.png",
                    "Regent Park": "regents-park.png",
                    "St Annes": "st-annes.png",
                    "St Anthonys": "st-antonys.png",
                    "St Benets": "st-benets-hall.png",
                    "St Catherines": "st-catherines.png",
                    "St Cross": "st-cross.png",
                    "St Edmund Hall": "st-edmund-hall.png",
                    "St Hildas": "st-hildas.png",
                    "St Hughs": "st-hughs.png",
                    "St Johns": "st-johns.png",
                    "St Peters": "st-peters.png",
                    "St Stephens": "st-stephens-house.png",
                    "Somerville": "somerville.png",
                    "Trinity": "trinity.png",
                    "University": "university.png",
                    "Wadham": "wadham.png",
                    "Wolfson":"wolfson.png",
                    "Worcester": "worcester.png",
                    "Wycliffe": "wycliffe-hall.png"}
var width = 960,
    height = 600;

var force = d3.layout.force()
    .charge(-250)
    .linkDistance(70)
    .size([width, height]);

var svg = d3.select("#network").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/static/oxhack/network.json", function(error, graph) {
  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();     

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .attr("stroke-width", function(d) {return (1+Math.sqrt(d.freq))+"px";})
        
  link.append("title")
      .attr("class", "link-title")
      .text(function(d) { return "No. of interactions: "+d.freq; });
      
  var node = svg.selectAll(".node")
      .data(graph.nodes)
    .enter().append("g")
      .attr("class", "node")
      .call(force.drag);
      
     node.append("image")
        .attr("xlink:href", function(d) {return "http://oxhunt.me/static/oxhack/images/college-crests/"+college_list[d.college];})
        .attr("x", -8)
        .attr("y", -8)
        .attr("width", 20)
        .attr("height", 20);

  node.append("title")
      .attr("class", "node-title")
      .text(function(d) { return "College: "+d.college; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
});