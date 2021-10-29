const States = {
    VACCINE_CERTIFICATE: Symbol("VACCINE_CERTIFICATE"),
    PERSONAL_ID: Symbol("PERSONAL_ID"),
    WAITING: Symbol("WAITING"),
}

const socket = new WebSocket(`ws://` + location.hostname + ":9999");

socket.addEventListener("open", () => {

});

socket.addEventListener("close", () => {
    alert("Socket closed, please reload the page");
});

let state = States.VACCINE_CERTIFICATE;

export function submitImage(image) {
    socket.send(image);
    const instruction = document.querySelector(".instruction");
    const button = document.querySelector(".take-picture");
    const canvas = document.querySelector("canvas");
    switch (state) {
        case States.VACCINE_CERTIFICATE:
            state = States.PERSONAL_ID;
            instruction.innerText = "Készíts egy képet a személyi igazolványodról!";
            break;
        case States.PERSONAL_ID:
            state = States.WAITING;
            instruction.innerText = "Várakozás";
            canvas.style.display = "none";
            button.style.display = "none";
            break;
    }
}

export function sendMessage(msg) {
    socket.send(msg);
}

socket.addEventListener("message", (e) => {
    if (state === States.WAITING) {
        const instruction = document.querySelector(".instruction");
        const button = document.querySelector(".take-picture");
        const canvas = document.querySelector("canvas");
        instruction.innerText = e.data === "SUCCESS" ? "Sikeres azonosítás" : "Sikertelen azonosítás";
        instruction.style.color = e.data === "SUCCESS" ? "green" : "red";
        setTimeout(() => {
            instruction.innerText = "Készíts egy képet a védettségi igazolványodról!"
            instruction.style.color = "black";
            button.style.display = "block";
            canvas.style.display = "block";
            state = States.VACCINE_CERTIFICATE;
        }, 3000);
    }
});