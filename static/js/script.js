

// document.addEventListener("DOMContentLoaded", function () {
//     const ctx = document.getElementById("leaveChart");

//     if (ctx) {  // Ensure the canvas element is available
//         new Chart(ctx, {
//             type: "doughnut",
//             data: {
//                 labels: ["Casual Leave", "Sick Leave", "On Duty", "Loss Of Pay", "Work Home"],
//                 datasets: [
//                     {
//                         label: "Leave Balance",
//                         data: [2, 10, 6, 12, 8], // Adjusted realistic data
//                         backgroundColor: ["#32c8cd", "#f78c6b", "#7851a9", "#c21b4e", "#ff1493"],
//                         borderWidth: 0,
//                     },
//                 ],
//             },
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 plugins: {
//                     legend: {
//                         position: "bottom",
//                         labels: {
//                             color: "black",
//                         },
//                     },
//                 },
//             },
//         });
//     } else {
//         console.error("Canvas element not found!");
//     }
// });




function toggleSidebar() {
    var sidebar = document.getElementById("menuSidebar");
    var contentWrapper = document.getElementById("contentWrapper");
    var overlay = document.getElementById("overlay");

    if (sidebar.classList.contains("visible")) {
        sidebar.classList.remove("visible");
        contentWrapper.classList.remove("blur");
        overlay.style.display = "none"; // Hide overlay
    } else {
        sidebar.classList.add("visible");
        contentWrapper.classList.add("blur");
        overlay.style.display = "block"; // Show overlay
    }
}

// Close sidebar when clicking on overlay
document.getElementById("overlay").addEventListener("click", function () {
    toggleSidebar();
});

// Close sidebar when screen resizes to large screens
window.addEventListener("resize", function () {
    var sidebar = document.getElementById("menuSidebar");
    var contentWrapper = document.getElementById("contentWrapper");
    var overlay = document.getElementById("overlay");

    if (window.innerWidth > 992) { // If screen width is more than 992px
        sidebar.classList.remove("visible");
        contentWrapper.classList.remove("blur");
        overlay.style.display = "none"; // Hide overlay
    }
});

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    document.querySelector(".navbar").classList.toggle("dark-mode");
    document.querySelector("#dataTable").classList.toggle("table-dark");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
}

// Apply dark mode if previously enabled
if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark-mode");
    document.querySelector(".navbar").classList.add("dark-mode");
    document.querySelector("#dataTable").classList.add("table-dark");
}