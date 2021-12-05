import {submitImage} from "./websocket.js";

const videoContainer = document.createElement("video");
videoContainer.autoplay = true;

const takePictureButton = document.querySelector(".take-picture");

const COUNTER_LENGTH = 3;
const FLASH_LENGTH = 0.2;
let counterStartTime = null;

const canvas = document.querySelector("canvas");
canvas.width = parseInt(canvas.style.width);
canvas.height = parseInt(canvas.style.height);
let ctx = canvas.getContext("2d");

if (navigator.mediaDevices?.getUserMedia)
    navigator.mediaDevices.getUserMedia({
        video: {
            width: 500,
            height: 793,
            colorTemperature: 7000,
            focusMode: "manual",
            focusDistance: 0,
            resizeMode: "cropAndScale",
            facingMode: "environment",
            torch: true,
        },
    })
        .then(stream => {
            videoContainer.srcObject = stream;
        })
        .catch(err => alert(`Error: ${err}`));

videoContainer.addEventListener("playing", () => {
    canvas.width = videoContainer.videoWidth;
    canvas.height = videoContainer.videoHeight;
    ctx = canvas.getContext("2d");

    requestAnimationFrame(draw);

});

function draw() {
    ctx.drawImage(videoContainer, 0, 0);
    if (counterStartTime !== null) {
        const diff = (Date.now() - counterStartTime) / 1000;
        const timeLeft = COUNTER_LENGTH - diff;
        if (timeLeft > 0) {
            const fractSecond = timeLeft % 1;
            const opacity = 1 - (1 - fractSecond) ** 5;
            const size = Math.round(canvas.width / 2);
            ctx.font = `${size}px Righteous`;
            ctx.fillStyle = `rgba(0, 165, 250, ${opacity})`;
            const text = Math.ceil(timeLeft) + "";
            const width = ctx.measureText(text).width;
            ctx.fillText(text, (canvas.width - width) / 2, (canvas.height + size / 2) / 2);
        } else if (timeLeft > -FLASH_LENGTH) {
            const opacity = ((timeLeft + FLASH_LENGTH) / FLASH_LENGTH) ** 0.3;
            ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        } else {
            counterStartTime = null;
            const offscreenCanvas = document.createElement("canvas");
            offscreenCanvas.width = canvas.width;
            offscreenCanvas.height = canvas.height;
            const offscreenCtx = offscreenCanvas.getContext("2d");
            offscreenCtx.drawImage(videoContainer, 0, 0);
            submitImage(offscreenCanvas.toDataURL());
        }
    }
    requestAnimationFrame(draw);
}

takePictureButton.addEventListener("click", () => {
    counterStartTime = Date.now();
});
