const videoElement = document.getElementById("video");
const startButton = document.getElementById("startButton");
const gestureDisplay = document.getElementById("gestureDisplay");
let socket = null;

startButton.onclick = async () => {
  // Initialize socket connection
  socket = io();

  // Start streaming video
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = stream;

    // Send frames to backend at regular intervals
    setInterval(() => {
      sendFrameToBackend();
    }, 1000); // Adjust the interval as needed
  } catch (err) {
    console.error("Error accessing camera:", err);
  }
};

// Function to send frame to backend
function sendFrameToBackend() {
  // Create a canvas element and draw the video frame on it
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  // Convert the canvas to base64 data URL
  const frameData = canvas.toDataURL("image/jpeg");

  // Send the frame data to the backend
  socket.emit("frame_data", frameData);
}

// Socket event listener for receiving detected gestures
socket.on("gesture_detected", (gesture) => {
  // Update gesture display
  gestureDisplay.textContent = "Detected Gesture: " + gesture;

  // Perform action based on detected gesture
  switch (gesture) {
    case "up":
      // Perform volume up action
      alert("Volume Up gesture detected!");
      break;
    case "down":
      // Perform volume down action
      alert("Volume Down gesture detected!");
      break;
    case "left":
      // Perform previous action
      alert("Previous gesture detected!");
      break;
    case "right":
      // Perform next action
      alert("Next gesture detected!");
      break;
    default:
      // Do nothing
      break;
  }
});
