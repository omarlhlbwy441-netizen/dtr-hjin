"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — GameArchitect Agent                    ║
║  وكيل تصميم وبناء الألعاب — HTML5 Canvas Games                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class GameArchitect:
    """وكيل متخصص في تصميم وبناء الألعاب"""

    GAME_TEMPLATES = {
        "platformer": {
            "name": "Platformer Adventure",
            "description": "لعبة منصات كلاسيكية مع قفز وجري",
            "engine": "html5",
            "difficulty": "medium",
            "assets": ["player", "platforms", "coins", "enemies", "background"]
        },
        "puzzle": {
            "name": "Puzzle Master",
            "description": "لعبة ألغاز منطقية",
            "engine": "html5",
            "difficulty": "easy",
            "assets": ["tiles", "background", "ui"]
        },
        "shooter": {
            "name": "Space Shooter",
            "description": "لعبة إطلاق نار فضائية",
            "engine": "html5",
            "difficulty": "hard",
            "assets": ["player", "enemies", "bullets", "powerups", "background"]
        },
        "racing": {
            "name": "Speed Racer",
            "description": "لعبة سباق سيارات",
            "engine": "html5",
            "difficulty": "medium",
            "assets": ["cars", "track", "obstacles", "background"]
        },
        "rpg": {
            "name": "RPG Quest",
            "description": "لعبة تقمص أدوار",
            "engine": "html5",
            "difficulty": "hard",
            "assets": ["hero", "npcs", "map", "items", "monsters"]
        }
    }

    def __init__(self):
        self.games_dir = Path("games")
        self.games_dir.mkdir(exist_ok=True)
        self.generated_games = []

    def list_templates(self) -> List[Dict]:
        return [{"id": k, **v} for k, v in self.GAME_TEMPLATES.items()]

    def generate_game(self, game_type: str, title: str, custom_config: Optional[Dict] = None) -> Dict[str, Any]:
        if game_type not in self.GAME_TEMPLATES:
            return {"status": "error", "message": f"Game type '{game_type}' not found"}

        template = self.GAME_TEMPLATES[game_type]
        game_id = str(uuid.uuid4())[:8]
        safe_title = title.replace(" ", "_").lower()
        game_dir = self.games_dir / f"{safe_title}_{game_id}"
        game_dir.mkdir(parents=True, exist_ok=True)

        config = {**template, **(custom_config or {})}

        files_generated = []

        # HTML
        html = self._generate_html(game_type, title, config)
        (game_dir / "index.html").write_text(html, encoding="utf-8")
        files_generated.append("index.html")

        # JS
        js = self._generate_js(game_type, config)
        (game_dir / "game.js").write_text(js, encoding="utf-8")
        files_generated.append("game.js")

        # CSS
        css = self._generate_css(config)
        (game_dir / "style.css").write_text(css, encoding="utf-8")
        files_generated.append("style.css")

        # Config
        cfg = json.dumps({
            "game_id": game_id, "title": title, "type": game_type,
            "created_at": datetime.utcnow().isoformat(),
            "config": config, "files": files_generated
        }, indent=2, ensure_ascii=False)
        (game_dir / "game.json").write_text(cfg, encoding="utf-8")
        files_generated.append("game.json")

        game_info = {
            "status": "success", "game_id": game_id, "title": title,
            "type": game_type, "directory": str(game_dir),
            "files": files_generated,
            "play_url": f"/games/{safe_title}_{game_id}/index.html",
            "created_at": datetime.utcnow().isoformat()
        }
        self.generated_games.append(game_info)
        return game_info

    def _generate_html(self, game_type, title, config):
        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Rafeeq Games</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="game-container">
<header class="game-header"><h1>🎮 {title}</h1>
<div class="game-stats"><span id="score">النقاط: 0</span><span id="level">المستوى: 1</span><span id="lives">❤️❤️❤️</span></div></header>
<canvas id="gameCanvas" width="800" height="600"></canvas>
<div class="game-controls">
<button id="startBtn" class="btn-primary">ابدأ اللعبة</button>
<button id="pauseBtn" class="btn-secondary" disabled>إيقاف مؤقت</button>
<button id="resetBtn" class="btn-secondary">إعادة</button></div>
<div class="instructions"><h3>🎯 طريقة اللعب:</h3><p>{config.get('description', 'استخدم الأسهم للتحرك')}</p></div></div>
<script src="game.js"></script></body></html>"""

    def _generate_js(self, game_type, config):
        engines = {
            "platformer": self._js_platformer,
            "shooter": self._js_shooter,
            "puzzle": self._js_puzzle,
            "racing": self._js_racing,
            "rpg": self._js_rpg
        }
        return engines.get(game_type, self._js_platformer)(config)

    def _js_platformer(self, config):
        return """const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let gameRunning=false,score=0,level=1,lives=3;
const player={x:50,y:400,w:40,h:40,vx:0,vy:0,speed:5,jump:-15,g:0.8,ground:false,color:'#0ea5e9'};
const platforms=[{x:0,y:550,w:800,h:50},{x:200,y:450,w:150,h:20},{x:450,y:350,w:150,h:20},{x:100,y:250,w:150,h:20},{x:600,y:200,w:150,h:20}];
const coins=[{x:250,y:410,r:10,c:false},{x:500,y:310,r:10,c:false},{x:150,y:210,r:10,c:false},{x:650,y:160,r:10,c:false}];
const enemies=[{x:300,y:510,w:30,h:30,s:2,d:1,color:'#ef4444'}];
const keys={};document.addEventListener('keydown',e=>keys[e.code]=true);document.addEventListener('keyup',e=>keys[e.code]=false);
function loop(){if(!gameRunning)return;update();draw();requestAnimationFrame(loop);}
function update(){
if(keys['ArrowRight']||keys['KeyD'])player.vx=player.speed;else if(keys['ArrowLeft']||keys['KeyA'])player.vx=-player.speed;else player.vx*=0.8;
if((keys['ArrowUp']||keys['Space']||keys['KeyW'])&&player.ground){player.vy=player.jump;player.ground=false;}
player.vy+=player.g;player.x+=player.vx;player.y+=player.vy;player.ground=false;
for(const p of platforms){if(player.x<p.x+p.w&&player.x+player.w>p.x&&player.y+player.h>p.y&&player.y+player.h<p.y+p.h+20){player.y=p.y-player.h;player.vy=0;player.ground=true;}}
if(player.x<0)player.x=0;if(player.x+player.w>canvas.width)player.x=canvas.width-player.w;
if(player.y>canvas.height){lives--;player.x=50;player.y=400;player.vy=0;if(lives<=0)gameOver();}
for(const c of coins){if(!c.c){const dx=player.x+player.w/2-c.x,dy=player.y+player.h/2-c.y;if(Math.sqrt(dx*dx+dy*dy)<c.r+player.w/2){c.c=true;score+=10;updateUI();}}}
for(const e of enemies){e.x+=e.s*e.d;if(e.x<=200||e.x>=500)e.d*=-1;
if(player.x<e.x+e.w&&player.x+player.w>e.x&&player.y<e.y+e.h&&player.y+player.h>e.y){lives--;player.x=50;player.y=400;updateUI();if(lives<=0)gameOver();}}
if(coins.every(c=>c.c)){level++;coins.forEach(c=>c.c=false);score+=50;updateUI();}}
function draw(){ctx.fillStyle='#0f172a';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#ffffff';for(let i=0;i<50;i++)ctx.fillRect((i*73)%canvas.width,(i*37)%canvas.height,2,2);
for(const p of platforms){ctx.fillStyle='#10b981';ctx.fillRect(p.x,p.y,p.w,p.h);ctx.strokeStyle='#ffffff';ctx.strokeRect(p.x,p.y,p.w,p.h);}
for(const c of coins){if(!c.c){ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,Math.PI*2);ctx.fillStyle='#fbbf24';ctx.fill();ctx.strokeStyle='#f59e0b';ctx.stroke();}}
for(const e of enemies){ctx.fillStyle=e.color;ctx.fillRect(e.x,e.y,e.w,e.h);ctx.fillStyle='#ffffff';ctx.fillRect(e.x+5,e.y+5,8,8);ctx.fillRect(e.x+17,e.y+5,8,8);}
ctx.fillStyle=player.color;ctx.fillRect(player.x,player.y,player.w,player.h);ctx.fillStyle='#ffffff';ctx.fillRect(player.x+8,player.y+8,8,8);ctx.fillRect(player.x+24,player.y+8,8,8);}
function updateUI(){document.getElementById('score').textContent='النقاط: '+score;document.getElementById('level').textContent='المستوى: '+level;document.getElementById('lives').textContent='❤️'.repeat(lives);}
function gameOver(){gameRunning=false;ctx.fillStyle='rgba(0,0,0,0.8)';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#ef4444';ctx.font='48px Arial';ctx.textAlign='center';ctx.fillText('انتهت اللعبة!',canvas.width/2,canvas.height/2);ctx.fillStyle='#ffffff';ctx.font='24px Arial';ctx.fillText('النقاط: '+score,canvas.width/2,canvas.height/2+50);document.getElementById('startBtn').textContent='إعادة اللعب';document.getElementById('startBtn').disabled=false;document.getElementById('pauseBtn').disabled=true;}
document.getElementById('startBtn').addEventListener('click',()=>{if(!gameRunning){gameRunning=true;score=0;level=1;lives=3;player.x=50;player.y=400;coins.forEach(c=>c.c=false);updateUI();document.getElementById('startBtn').textContent='جاري اللعب...';document.getElementById('startBtn').disabled=true;document.getElementById('pauseBtn').disabled=false;loop();}});
document.getElementById('pauseBtn').addEventListener('click',()=>{gameRunning=!gameRunning;document.getElementById('pauseBtn').textContent=gameRunning?'إيقاف مؤقت':'استئناف';if(gameRunning)loop();});
document.getElementById('resetBtn').addEventListener('click',()=>{gameRunning=false;score=0;level=1;lives=3;player.x=50;player.y=400;coins.forEach(c=>c.c=false);updateUI();draw();document.getElementById('startBtn').textContent='ابدأ اللعبة';document.getElementById('startBtn').disabled=false;document.getElementById('pauseBtn').disabled=true;});
draw();"""

    def _js_shooter(self, config):
        return """const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let gameRunning=false,score=0,level=1;
const player={x:400,y:500,w:50,h:50,speed:7,color:'#0ea5e9'};
const bullets=[],enemies=[],particles=[];
const keys={};document.addEventListener('keydown',e=>keys[e.code]=true);document.addEventListener('keyup',e=>keys[e.code]=false);
function spawnEnemy(){enemies.push({x:Math.random()*(canvas.width-40),y:-40,w:40,h:40,s:2+level*0.5,color:'#ef4444'});}
function createParticles(x,y,color){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-0.5)*8,vy:(Math.random()-0.5)*8,life:30,color});}
function loop(){if(!gameRunning)return;update();draw();requestAnimationFrame(loop);}
function update(){
if(keys['ArrowLeft']||keys['KeyA'])player.x-=player.speed;if(keys['ArrowRight']||keys['KeyD'])player.x+=player.speed;player.x=Math.max(0,Math.min(canvas.width-player.w,player.x));
if(keys['Space']){if(!player.lastShot||Date.now()-player.lastShot>200){bullets.push({x:player.x+player.w/2-3,y:player.y,w:6,h:15,s:10});player.lastShot=Date.now();}}
for(let i=bullets.length-1;i>=0;i--){bullets[i].y-=bullets[i].s;if(bullets[i].y<0)bullets.splice(i,1);}
if(Math.random()<0.02+level*0.005)spawnEnemy();
for(let i=enemies.length-1;i>=0;i--){enemies[i].y+=enemies[i].s;
for(let j=bullets.length-1;j>=0;j--){if(bullets[j].x<enemies[i].x+enemies[i].w&&bullets[j].x+bullets[j].w>enemies[i].x&&bullets[j].y<enemies[i].y+enemies[i].h&&bullets[j].y+bullets[j].h>enemies[i].y){createParticles(enemies[i].x+enemies[i].w/2,enemies[i].y+enemies[i].h/2,'#ef4444');enemies.splice(i,1);bullets.splice(j,1);score+=10;if(score%100===0)level++;updateUI();break;}}
if(enemies[i]&&enemies[i].y>canvas.height)enemies.splice(i,1);}
for(let i=particles.length-1;i>=0;i--){particles[i].x+=particles[i].vx;particles[i].y+=particles[i].vy;particles[i].life--;if(particles[i].life<=0)particles.splice(i,1);}}
function draw(){ctx.fillStyle='#0f172a';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#ffffff';for(let i=0;i<100;i++)ctx.fillRect((i*137+Date.now()*0.01)%canvas.width,(i*93)%canvas.height,1,1);
ctx.fillStyle=player.color;ctx.beginPath();ctx.moveTo(player.x+player.w/2,player.y);ctx.lineTo(player.x+player.w,player.y+player.h);ctx.lineTo(player.x,player.y+player.h);ctx.closePath();ctx.fill();
ctx.fillStyle='#fbbf24';for(const b of bullets)ctx.fillRect(b.x,b.y,b.w,b.h);
for(const e of enemies){ctx.fillStyle=e.color;ctx.fillRect(e.x,e.y,e.w,e.h);ctx.fillStyle='#ffffff';ctx.fillRect(e.x+8,e.y+10,8,8);ctx.fillRect(e.x+24,e.y+10,8,8);}
for(const p of particles){ctx.fillStyle=p.color;ctx.globalAlpha=p.life/30;ctx.fillRect(p.x,p.y,4,4);}ctx.globalAlpha=1;}
function updateUI(){document.getElementById('score').textContent='النقاط: '+score;document.getElementById('level').textContent='المستوى: '+level;}
document.getElementById('startBtn').addEventListener('click',()=>{if(!gameRunning){gameRunning=true;score=0;level=1;bullets.length=0;enemies.length=0;particles.length=0;updateUI();document.getElementById('startBtn').disabled=true;document.getElementById('pauseBtn').disabled=false;loop();}});
document.getElementById('pauseBtn').addEventListener('click',()=>{gameRunning=!gameRunning;document.getElementById('pauseBtn').textContent=gameRunning?'إيقاف مؤقت':'استئناف';if(gameRunning)loop();});
document.getElementById('resetBtn').addEventListener('click',()=>{gameRunning=false;score=0;level=1;bullets.length=0;enemies.length=0;particles.length=0;updateUI();draw();document.getElementById('startBtn').disabled=false;document.getElementById('startBtn').textContent='ابدأ اللعبة';document.getElementById('pauseBtn').disabled=true;});
draw();"""

    def _js_puzzle(self, config):
        return """const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let gameRunning=false,score=0,moves=0;
const gridSize=4,tileSize=100,gap=10;
let grid=[],emptyPos={x:3,y:3};
function initGrid(){grid=[];let numbers=Array.from({length:15},(_,i)=>i+1);numbers.push(0);
for(let i=numbers.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[numbers[i],numbers[j]]=[numbers[j],numbers[i]];}
for(let y=0;y<gridSize;y++){grid[y]=[];for(let x=0;x<gridSize;x++){grid[y][x]=numbers[y*gridSize+x];if(grid[y][x]===0)emptyPos={x,y};}}}
function moveTile(x,y){if(Math.abs(x-emptyPos.x)+Math.abs(y-emptyPos.y)!==1)return false;grid[emptyPos.y][emptyPos.x]=grid[y][x];grid[y][x]=0;emptyPos={x,y};moves++;
let won=true,expected=1;for(let y=0;y<gridSize;y++){for(let x=0;x<gridSize;x++){if(y===gridSize-1&&x===gridSize-1)continue;if(grid[y][x]!==expected){won=false;break;}expected++;}}
if(won){score=Math.max(1000-moves*10,100);document.getElementById('score').textContent='النقاط: '+score;ctx.fillStyle='rgba(0,0,0,0.8)';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#10b981';ctx.font='48px Arial';ctx.textAlign='center';ctx.fillText('🎉 فزت!',canvas.width/2,canvas.height/2);gameRunning=false;document.getElementById('startBtn').textContent='لعب مرة أخرى';document.getElementById('startBtn').disabled=false;}return true;}
function draw(){ctx.fillStyle='#0f172a';ctx.fillRect(0,0,canvas.width,canvas.height);
const offsetX=(canvas.width-(gridSize*tileSize+(gridSize-1)*gap))/2;
const offsetY=(canvas.height-(gridSize*tileSize+(gridSize-1)*gap))/2;
for(let y=0;y<gridSize;y++){for(let x=0;x<gridSize;x++){const num=grid[y][x];const px=offsetX+x*(tileSize+gap);const py=offsetY+y*(tileSize+gap);
if(num===0){ctx.fillStyle='#1e293b';ctx.fillRect(px,py,tileSize,tileSize);}else{ctx.fillStyle='#0ea5e9';ctx.fillRect(px,py,tileSize,tileSize);ctx.strokeStyle='#38bdf8';ctx.strokeRect(px,py,tileSize,tileSize);ctx.fillStyle='#ffffff';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(num.toString(),px+tileSize/2,py+tileSize/2);}}}}
canvas.addEventListener('click',e=>{if(!gameRunning)return;const rect=canvas.getBoundingClientRect();const mx=e.clientX-rect.left,my=e.clientY-rect.top;
const offsetX=(canvas.width-(gridSize*tileSize+(gridSize-1)*gap))/2;const offsetY=(canvas.height-(gridSize*tileSize+(gridSize-1)*gap))/2;
const x=Math.floor((mx-offsetX)/(tileSize+gap));const y=Math.floor((my-offsetY)/(tileSize+gap));
if(x>=0&&x<gridSize&&y>=0&&y<gridSize){if(moveTile(x,y))draw();}});
document.getElementById('startBtn').addEventListener('click',()=>{initGrid();gameRunning=true;moves=0;document.getElementById('score').textContent='النقاط: 0';document.getElementById('startBtn').disabled=true;draw();});
document.getElementById('resetBtn').addEventListener('click',()=>{gameRunning=false;initGrid();moves=0;document.getElementById('score').textContent='النقاط: 0';document.getElementById('startBtn').disabled=false;document.getElementById('startBtn').textContent='ابدأ اللعبة';draw();});
initGrid();draw();"""

    def _js_racing(self, config):
        return """const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let gameRunning=false,score=0,speed=5;
const car={x:375,y:500,w:50,h:80,color:'#0ea5e9'};
const obstacles=[],roadLines=[];
const keys={};document.addEventListener('keydown',e=>keys[e.code]=true);document.addEventListener('keyup',e=>keys[e.code]=false);
for(let i=0;i<6;i++)roadLines.push({x:395,y:i*120,w:10,h:60});
function spawnObstacle(){const lanes=[200,375,550];obstacles.push({x:lanes[Math.floor(Math.random()*lanes.length)],y:-100,w:50,h:80,color:'#ef4444'});}
function loop(){if(!gameRunning)return;update();draw();requestAnimationFrame(loop);}
function update(){
if(keys['ArrowLeft']||keys['KeyA'])car.x-=8;if(keys['ArrowRight']||keys['KeyD'])car.x+=8;car.x=Math.max(150,Math.min(600,car.x));
for(const line of roadLines){line.y+=speed;if(line.y>canvas.height)line.y=-60;}
if(Math.random()<0.015)spawnObstacle();
for(let i=obstacles.length-1;i>=0;i--){obstacles[i].y+=speed;
if(car.x<obstacles[i].x+obstacles[i].w&&car.x+car.w>obstacles[i].x&&car.y<obstacles[i].y+obstacles[i].h&&car.y+car.h>obstacles[i].y){gameOver();return;}
if(obstacles[i].y>canvas.height){obstacles.splice(i,1);score+=10;if(score%100===0)speed+=1;updateUI();}}}
function draw(){ctx.fillStyle='#1e293b';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#10b981';ctx.fillRect(0,0,130,canvas.height);ctx.fillRect(670,0,130,canvas.height);ctx.fillStyle='#ffffff';for(const line of roadLines)ctx.fillRect(line.x,line.y,line.w,line.h);
ctx.fillStyle=car.color;ctx.fillRect(car.x,car.y,car.w,car.h);ctx.fillStyle='#38bdf8';ctx.fillRect(car.x+5,car.y+10,car.w-10,20);ctx.fillStyle='#fbbf24';ctx.fillRect(car.x+10,car.y+60,10,10);ctx.fillRect(car.x+30,car.y+60,10,10);
for(const obs of obstacles){ctx.fillStyle=obs.color;ctx.fillRect(obs.x,obs.y,obs.w,obs.h);ctx.fillStyle='#ffffff';ctx.fillRect(obs.x+10,obs.y+10,8,8);ctx.fillRect(obs.x+32,obs.y+10,8,8);}}
function updateUI(){document.getElementById('score').textContent='النقاط: '+score;document.getElementById('level').textContent='السرعة: '+speed;}
function gameOver(){gameRunning=false;ctx.fillStyle='rgba(0,0,0,0.8)';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#ef4444';ctx.font='48px Arial';ctx.textAlign='center';ctx.fillText('💥 تصادم!',canvas.width/2,canvas.height/2);ctx.fillStyle='#ffffff';ctx.font='24px Arial';ctx.fillText('النقاط: '+score,canvas.width/2,canvas.height/2+50);document.getElementById('startBtn').textContent='إعادة المحاولة';document.getElementById('startBtn').disabled=false;document.getElementById('pauseBtn').disabled=true;}
document.getElementById('startBtn').addEventListener('click',()=>{if(!gameRunning){gameRunning=true;score=0;speed=5;obstacles.length=0;updateUI();document.getElementById('startBtn').disabled=true;document.getElementById('pauseBtn').disabled=false;loop();}});
document.getElementById('pauseBtn').addEventListener('click',()=>{gameRunning=!gameRunning;document.getElementById('pauseBtn').textContent=gameRunning?'إيقاف مؤقت':'استئناف';if(gameRunning)loop();});
document.getElementById('resetBtn').addEventListener('click',()=>{gameRunning=false;score=0;speed=5;obstacles.length=0;updateUI();draw();document.getElementById('startBtn').disabled=false;document.getElementById('startBtn').textContent='ابدأ اللعبة';document.getElementById('pauseBtn').disabled=true;});
draw();"""

    def _js_rpg(self, config):
        return """const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let gameRunning=false;
const tileSize=40,mapWidth=20,mapHeight=15;
const map=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]];
const hero={x:2,y:2,hp:100,maxHp:100,exp:0,level:1};
const monsters=[{x:10,y:5,hp:30,maxHp:30,damage:10},{x:15,y:8,hp:40,maxHp:40,damage:15},{x:8,y:12,hp:25,maxHp:25,damage:8}];
const items=[{x:5,y:3,type:'potion',value:20},{x:12,y:10,type:'sword',value:10},{x:18,y:13,type:'potion',value:20}];
document.addEventListener('keydown',e=>{if(!gameRunning)return;let newX=hero.x,newY=hero.y;
if(e.code==='ArrowUp'||e.code==='KeyW')newY--;if(e.code==='ArrowDown'||e.code==='KeyS')newY++;if(e.code==='ArrowLeft'||e.code==='KeyA')newX--;if(e.code==='ArrowRight'||e.code==='KeyD')newX++;
if(map[newY]&&map[newY][newX]===0){hero.x=newX;hero.y=newY;}
for(let i=items.length-1;i>=0;i--){if(items[i].x===hero.x&&items[i].y===hero.y){if(items[i].type==='potion')hero.hp=Math.min(hero.hp+items[i].value,hero.maxHp);else hero.damage=(hero.damage||10)+items[i].value;items.splice(i,1);}}
for(const m of monsters){if(m.x===hero.x&&m.y===hero.y){m.hp-=(hero.damage||10);hero.hp-=m.damage;if(m.hp<=0){hero.exp+=20;if(hero.exp>=hero.level*50){hero.level++;hero.maxHp+=20;hero.hp=hero.maxHp;hero.exp=0;}}if(hero.hp<=0){gameOver();return;}}}draw();updateUI();});
function draw(){ctx.fillStyle='#0f172a';ctx.fillRect(0,0,canvas.width,canvas.height);
for(let y=0;y<mapHeight;y++){for(let x=0;x<mapWidth;x++){const px=x*tileSize,py=y*tileSize;if(map[y][x]===1){ctx.fillStyle='#334155';ctx.fillRect(px,py,tileSize,tileSize);ctx.strokeStyle='#475569';ctx.strokeRect(px,py,tileSize,tileSize);}else{ctx.fillStyle='#1e293b';ctx.fillRect(px,py,tileSize,tileSize);}}}
for(const item of items){const px=item.x*tileSize+tileSize/2,py=item.y*tileSize+tileSize/2;ctx.fillStyle=item.type==='potion'?'#ef4444':'#fbbf24';ctx.beginPath();ctx.arc(px,py,10,0,Math.PI*2);ctx.fill();}
for(const m of monsters){if(m.hp>0){const px=m.x*tileSize,py=m.y*tileSize;ctx.fillStyle='#7c3aed';ctx.fillRect(px+5,py+5,tileSize-10,tileSize-10);ctx.fillStyle='#ef4444';ctx.fillRect(px+5,py-5,(tileSize-10)*(m.hp/m.maxHp),4);}}
const px=hero.x*tileSize,py=hero.y*tileSize;ctx.fillStyle='#0ea5e9';ctx.fillRect(px+5,py+5,tileSize-10,tileSize-10);ctx.fillStyle='#ffffff';ctx.fillRect(px+10,py+12,6,6);ctx.fillRect(px+24,py+12,6,6);}
function updateUI(){document.getElementById('score').textContent='HP: '+hero.hp+'/'+hero.maxHp;document.getElementById('level').textContent='المستوى: '+hero.level;document.getElementById('lives').textContent='XP: '+hero.exp;}
function gameOver(){gameRunning=false;ctx.fillStyle='rgba(0,0,0,0.8)';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#ef4444';ctx.font='48px Arial';ctx.textAlign='center';ctx.fillText('☠️ مات البطل!',canvas.width/2,canvas.height/2);ctx.fillStyle='#ffffff';ctx.font='24px Arial';ctx.fillText('المستوى: '+hero.level,canvas.width/2,canvas.height/2+50);document.getElementById('startBtn').textContent='إعادة المحاولة';document.getElementById('startBtn').disabled=false;}
document.getElementById('startBtn').addEventListener('click',()=>{gameRunning=true;hero.x=2;hero.y=2;hero.hp=100;hero.maxHp=100;hero.exp=0;hero.level=1;monsters[0].hp=30;monsters[1].hp=40;monsters[2].hp=25;items.length=0;items.push({x:5,y:3,type:'potion',value:20});items.push({x:12,y:10,type:'sword',value:10});items.push({x:18,y:13,type:'potion',value:20});updateUI();document.getElementById('startBtn').disabled=true;draw();});
document.getElementById('resetBtn').addEventListener('click',()=>{gameRunning=false;hero.x=2;hero.y=2;hero.hp=100;hero.maxHp=100;hero.exp=0;hero.level=1;monsters[0].hp=30;monsters[1].hp=40;monsters[2].hp=25;updateUI();document.getElementById('startBtn').disabled=false;document.getElementById('startBtn').textContent='ابدأ اللعبة';draw();});
updateUI();draw();"""

    def _generate_css(self, config):
        return """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);color:#e2e8f0;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.game-container{background:rgba(30,41,59,0.9);border-radius:16px;padding:24px;box-shadow:0 25px 50px -12px rgba(0,0,0,0.5);border:1px solid rgba(148,163,184,0.1);max-width:900px;width:100%}
.game-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid rgba(148,163,184,0.1)}
.game-header h1{font-size:1.8rem;background:linear-gradient(135deg,#0ea5e9,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.game-stats{display:flex;gap:20px;font-size:1rem;color:#94a3b8}
.game-stats span{background:rgba(15,23,42,0.6);padding:6px 12px;border-radius:8px;border:1px solid rgba(148,163,184,0.1)}
#gameCanvas{display:block;margin:0 auto 20px;border-radius:12px;border:2px solid rgba(148,163,184,0.2);background:#0f172a;max-width:100%}
.game-controls{display:flex;justify-content:center;gap:12px;margin-bottom:20px}
.btn-primary,.btn-secondary{padding:12px 24px;border:none;border-radius:10px;font-size:1rem;font-weight:600;cursor:pointer;transition:all 0.3s ease}
.btn-primary{background:linear-gradient(135deg,#0ea5e9,#8b5cf6);color:white}
.btn-primary:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 10px 20px -5px rgba(14,165,233,0.4)}
.btn-secondary{background:rgba(148,163,184,0.1);color:#e2e8f0;border:1px solid rgba(148,163,184,0.2)}
.btn-secondary:hover:not(:disabled){background:rgba(148,163,184,0.2)}
button:disabled{opacity:0.5;cursor:not-allowed}
.instructions{background:rgba(15,23,42,0.6);padding:16px;border-radius:10px;border:1px solid rgba(148,163,184,0.1)}
.instructions h3{color:#0ea5e9;margin-bottom:8px}
.instructions p{color:#94a3b8;line-height:1.6}"""

    def list_games(self):
        return self.generated_games


game_architect = GameArchitect()
def get_game_architect():
    return game_architect
