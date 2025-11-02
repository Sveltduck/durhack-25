<script lang="ts">
import {onMount} from "svelte";

// TODO: Loading state, fetch data from Python server before allowing reveal

let opacity = 0;

const SPEED_MULTIPLIER = 1;

let lastX = 0;
let lastY = 0;
let revealScore = 0;
let lastTime = Date.now();

let animationInterval: NodeJS.Timeout;

function onMouseMove(event: MouseEvent) {
    if (!animationInterval) return; // already fully revealed

    const now = Date.now();
    const dt = now - lastTime || 16; // fallback to ~60fps interval

    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;
    const speed = Math.sqrt(dx * dx + dy * dy) / dt;

    // Increase score while moving quickly
    if (speed > 0.3) {
        revealScore += speed * SPEED_MULTIPLIER;
    }

    // clamp
    revealScore = Math.min(Math.max(revealScore, 0), 100);

    lastX = event.clientX;
    lastY = event.clientY;
    lastTime = now;
}

onMount(() => {
    // Animation loop — fade in until fully revealed
    animationInterval = setInterval(() => {
        // gentle decay so user must keep moving to build score
        opacity = Math.min(revealScore / 100, 1);

        revealScore *= 0.97;
        if (revealScore < 0.01) revealScore = 0;

        // Once fully visible, lock it in
        if (opacity >= 1) {
            clearInterval(animationInterval);
        }
    }, 50);
});
</script>

<h1>Results</h1>
<p id="toptext">Leave a great Legacy</p>
<div id="main">
  <img onmousemove={onMouseMove} id="crystalBall" alt="Crystal ball" src="https://media.istockphoto.com/id/933666298/photo/hands-on-crystal-ball-and-cryptocurrency.jpg?s=612x612&w=0&k=20&c=rWJ_caa0AZCHYB09wkcLRghIYGZmGqfYe8D2l1JNZE8=">
  <p id="result" style:opacity={opacity}>This is your Roommate!</p>
</div>

<style>
@import url("https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&family=Momo+Signature&display=swap");

:global(body) {
  background-color: black;
}

h1{
  color: white;
  text-align: center;
  font-family: "Momo Signature", cursive;
  font-size: 50px;
  margin: 0;
}

#toptext {
    color: white;
    text-align:center;
    font-family: "Momo Signature", cursive;
    font-size:15px;
    margin:5px;
} 

#main {
  position: relative;
  text-align: center;
}

#crystalBall {
  width: 52%;
  height: 52%;
  display: block;
  margin: auto;
  cursor: pointer;
}

#result {
  color: black;
  font-size: 20px;
  font-weight: bold;
  position: absolute;
  font-family: "Momo Signature", cursive;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  opacity: 0;
  transition: opacity 0.3s ease;
}
</style>