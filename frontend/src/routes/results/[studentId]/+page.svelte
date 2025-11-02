<script lang="ts">
import { onMount, onDestroy } from "svelte";
import { page } from '$app/state';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

let opacity = $state(1);
let resultText = $state("Prophesizing...");

const SPEED_MULTIPLIER = 1;
const DECAY_FACTOR = 0.97; // Gentle decay per frame
const SPEED_THRESHOLD = 0.3; // Minimum speed to count

let mouseX: number | undefined;
let mouseY: number | undefined;
let lastX: number | undefined;
let lastY: number | undefined;
let lastTime: DOMHighResTimeStamp;
let animationFrameId: number | undefined;

function animate() {
    if (mouseX === undefined || mouseY === undefined) {
        // The mouse hasn't entered the area yet
        animationFrameId = requestAnimationFrame(animate);
        return;
    }

    const now = performance.now();
    if (lastTime !== undefined && lastX !== undefined && lastY !== undefined) {
        // Calculate mouse speed since the last frame
        const dt = now - lastTime;
        const dx = mouseX - lastX;
        const dy = mouseY - lastY;
        const speed = Math.sqrt(dx * dx + dy * dy) / (dt || 1);

        // Increase opacity based on speed
        if (speed > SPEED_THRESHOLD) {
            opacity += speed * SPEED_MULTIPLIER / 100;
        }

        // Apply a gentle decay on every frame so the user must keep moving
        opacity *= DECAY_FACTOR;
    }

    // Update state for the next frame's calculation
    lastX = mouseX;
    lastY = mouseY;
    lastTime = now;

    if (opacity >= 1) {
        // Once fully visible, lock it in
        opacity = 1;
    } else {
        // Until fully visible, keep animating
        animationFrameId = requestAnimationFrame(animate);
    }
}

function onMouseMove(event: MouseEvent) {
    mouseX = event.clientX;
    mouseY = event.clientY;
}

onMount(() => {
    onDestroy(() => {
        if (animationFrameId !== undefined) {
            cancelAnimationFrame(animationFrameId);
        }
    });

    fetch(`${PUBLIC_BACKEND_URL}/roommate/${page.params.studentId}`)
        .then(response => response.json())
        .then(response => {
            opacity = 0;
            resultText = `Your roommate is\n ${response.match_name} (student ID: ${response.best_match})`

            animationFrameId = requestAnimationFrame(animate);
        })

});
</script>

<h1>Results</h1>
<p id="toptext">No better legacy than a friendship.</p>
<div id="main">
    <img
            onmousemove={onMouseMove}
            onmouseleave={() => {mouseX = undefined; mouseY = undefined;}}
            id="crystalBall"
            alt="Crystal ball"
            src="https://media.istockphoto.com/id/933666298/photo/hands-on-crystal-ball-and-cryptocurrency.jpg?s=612x612&w=0&k=20&c=rWJ_caa0AZCHYB09wkcLRghIYGZmGqfYe8D2l1JNZE8="
    >
    <pre id="result" style:opacity={opacity}>{resultText}</pre>
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
    text-align: center;
    font-family: "Momo Signature", cursive;
    font-size: 15px;
    margin: 5px;
}

#main {
  position: relative;
  text-align: center;
}

#crystalBall {
  width: 52%;
  height: 52%;
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
}
</style>