var pointList=new Array();
function Point(tX,tY,tVx,tVy,tR){
  this.x=tX;
  this.y=tY;
  this.vx=tVx;
  this.vy=tVy;
  this.r=tR;
}

function setup(){
  createCanvas(window.screen.width,window.innerHeight);
  frameRate(24);
  for(var i=0;i<80;i++){
    pointList.push(new Point(random(width),random(height),random(-1,1),random(-1,1),random(5,10)));
  }
}

function draw(){
  background(255);
  noStroke();
  fill(200,200,200);
  ellipse(mouseX,mouseY,5,5);
  for(var i=0;i<pointList.length;i++){
    ellipse(pointList[i].x,pointList[i].y,pointList[i].r,pointList[i].r);
    pointList[i].x+=pointList[i].vx;
    pointList[i].y+=pointList[i].vy;
    if(pointList[i].x>width) pointList[i].x=0;
    if(pointList[i].x<0) pointList[i].x=width;
    if(pointList[i].y>height) pointList[i].y=0;
    if(pointList[i].y<0) pointList[i].y=height;
    for(var j=0;j<pointList.length;j++){
      if(i!=j){
        var d=dist(pointList[i].x,pointList[i].y,pointList[j].x,pointList[j].y);
        if(d<100){
          var sColor=map(d,0,100,0,255);
          stroke(sColor);
          line(pointList[i].x,pointList[i].y,pointList[j].x,pointList[j].y);
          noStroke();
        }
      }
    }
    var d=dist(pointList[i].x,pointList[i].y,mouseX,mouseY);
    if(d<100){
      var sColor=map(d,0,100,0,255);
      stroke(sColor);
      line(pointList[i].x,pointList[i].y,mouseX,mouseY);
      noStroke();
    }
  }
}
