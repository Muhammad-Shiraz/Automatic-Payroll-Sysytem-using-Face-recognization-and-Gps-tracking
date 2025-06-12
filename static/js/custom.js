document.addEventListener("DOMContentLoaded", () => {
    // Sidebar Toggle Functionality
    const sidebarToggle = document.querySelector('#sidebarCollapse');
    const sidebar = document.querySelector('#sidebar');
    const content = document.querySelector('#content');
    const overlay = document.querySelector('.body-overlay');
    const moreButtons = document.querySelectorAll('.more-button, .body-overlay');
    const icon = sidebarToggle.querySelector('.material-icons');


    // Initialize Sidebar State Based on Screen Size
    // const initializeSidebar = () => {
    //     const isLargeScreen = window.innerWidth >= 992;
    //     // sidebar.classList.toggle('active', isLargeScreen);
    //     // content.classList.toggle('active', isLargeScreen);
    //     // icon.textContent = isLargeScreen ? 'arrow_forward_ios' : 'arrow_back_ios';
    // };

    // initializeSidebar(); // On Page Load
    // window.addEventListener('resize', initializeSidebar); // On Window Resize

    // Toggle Sidebar on Button Click
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            const isLargeScreen = window.innerWidth >= 992;
            if (isLargeScreen) {
                sidebar.classList.toggle('active');
                content.classList.toggle('active');
                icon.textContent = sidebar.classList.contains('active') ? 'arrow_forward_ios' : 'arrow_back_ios';
            } else {
                sidebar.classList.toggle('show-nav');
                overlay.classList.toggle('show-nav');
            }
        });
    }

    // Additional Toggle for Small Screens
    moreButtons.forEach(button => {
        button.addEventListener('click', () => {
            sidebar.classList.toggle('show-nav');
            overlay.classList.toggle('show-nav');
        });
    });

    document.addEventListener("DOMContentLoaded", () => {
        const sidebar = document.querySelector('#sidebar');
        const overlay = document.querySelector('.body-overlay');
        const dropdownMenus = document.querySelectorAll('.dropdown-menu'); // Adjust this selector to match your submenu structure.

        // Function to close the sidebar and submenus
        const closeMenus = () => {
            sidebar.classList.remove('show-nav');
            overlay.classList.remove('show-nav');
            dropdownMenus.forEach(menu => {
                menu.classList.remove('show'); // Assuming 'show' class toggles the submenu visibility
            });
        };

    });


    // Close Other Submenus When One is Opened
    const dropdownLinks = document.querySelectorAll('.dropdown a[data-bs-toggle="collapse"]');
    dropdownLinks.forEach(link => {
        link.addEventListener('click', function () {
            const currentMenu = this.getAttribute("href");
            const collapses = document.querySelectorAll('.collapse');
            collapses.forEach(collapse => {
                if (collapse.id !== currentMenu.replace('#', '')) {
                    const bsCollapse = new bootstrap.Collapse(collapse, { toggle: false });
                    bsCollapse.hide();
                }
            });
        });
    });



    // // Theme Toggle Logic
    // const applyTheme = (theme) => {
    //     document.body.classList.toggle('dark-theme-variables', theme === "dark");
    //     localStorage.setItem("theme", theme);

    //     const togglers = document.querySelectorAll('.theme-toggler, .theme-toggler-2');
    //     togglers.forEach(toggler => {
    //         toggler.querySelector('span:nth-child(1)').classList.toggle('active', theme === "light");
    //         toggler.querySelector('span:nth-child(2)').classList.toggle('active', theme === "dark");
    //     });

    //     const themeSelector = document.querySelector('#themeSelection');
    //     if (themeSelector) themeSelector.value = theme;
    // };

    // const savedTheme = localStorage.getItem("theme") || "light";
    // applyTheme(savedTheme);

    // const themeTogglers = document.querySelectorAll('.theme-toggler, .theme-toggler-2');
    // themeTogglers.forEach(toggler => {
    //     toggler.addEventListener('click', () => {
    //         const isDark = document.body.classList.contains('dark-theme-variables');
    //         applyTheme(isDark ? "light" : "dark");
    //     });
    // });


    // const themeSelector = document.querySelector('#themeSelection');
    // if (themeSelector) {
    //     themeSelector.addEventListener('change', (event) => {
    //         applyTheme(event.target.value);
    //     });
    // }

    // Logout Functionality
    const logoutButtons = document.querySelectorAll('a[href="#logout"]');
    const confirmLogoutButton = document.querySelector('#confirmLogout');
    const logoutModalElement = document.querySelector('#logoutModal');

    if (logoutModalElement && confirmLogoutButton) {
        const logoutModal = new bootstrap.Modal(logoutModalElement);

        logoutButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                logoutModal.show();
            });
        });

        confirmLogoutButton.addEventListener('click', () => {
            console.log("User confirmed logout.");
            window.location.href = "index.html";
        });
    }







});













// Real-Time Attendance
// Dynamic Table Filtering
$(document).ready(function () {
    $("#searchInput, #departmentFilter, #statusFilter").on("input change", function () {
        let searchValue = $("#searchInput").val().toLowerCase();
        let departmentValue = $("#departmentFilter").val().toLowerCase();
        let statusValue = $("#statusFilter").val().toLowerCase();

        $("#attendanceTable tr").filter(function () {
            let nameOrId = $(this).text().toLowerCase();
            let department = $(this).find("td:nth-child(3)").text().trim().toLowerCase();
            let status = $(this).find("td:nth-child(6)").text().trim().toLowerCase();

            $(this).toggle(
                nameOrId.includes(searchValue) &&
                (departmentValue === "" || department === departmentValue) &&
                (statusValue === "" || status === statusValue)
            );
        });
    });
});



// toast

// custom.js

document.addEventListener('DOMContentLoaded', function () {
    // Find the script tag with messages JSON
    const messagesScript = document.getElementById('django-messages-data');
    if (!messagesScript) return; // No messages data found

    // Parse JSON messages
    let messages = [];
    try {
        messages = JSON.parse(messagesScript.textContent);
    } catch (e) {
        console.error('Error parsing messages JSON:', e);
    }

    if (messages.length === 0) return; // No messages to show

    // Create toast container
    const container = document.createElement('div');
    container.classList.add('toast-container');
    document.body.appendChild(container);

    messages.forEach(text => {
        const toast = document.createElement('div');
        toast.classList.add('toast');

        // You can customize icons here
        const iconHtml = '✔️';

        toast.innerHTML = `
      <span class="icon">${iconHtml}</span>
      <span class="message">${text}</span>
      <span class="progress-bar"></span>
    `;

        container.appendChild(toast);

        // Animate and remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.5s forwards';
            toast.addEventListener('animationend', () => toast.remove());

            if (!container.hasChildNodes()) {
                container.remove();
            }
        }, 5000);
    });
});






document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById('themeToggle');
    const sunIcon = themeToggle.querySelector('.sun-icon');
    const moonIcon = themeToggle.querySelector('.moon-icon');
    const body = document.body;

    // Load saved theme from localStorage or default to light
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-theme-variables');
        sunIcon.classList.remove('active');
        moonIcon.classList.add('active');
    } else {
        body.classList.remove('dark-theme-variables');
        sunIcon.classList.add('active');
        moonIcon.classList.remove('active');
    }

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme-variables');
        const isDark = body.classList.contains('dark-theme-variables');

        if (isDark) {
            sunIcon.classList.remove('active');
            moonIcon.classList.add('active');
            localStorage.setItem('theme', 'dark');
        } else {
            sunIcon.classList.add('active');
            moonIcon.classList.remove('active');
            localStorage.setItem('theme', 'light');
        }
    });
});




// // Initial icon setup
// lucide.createIcons();

// function toggleTheme() {
//     const body = document.body;
//     const sunIcon = document.querySelector('.sun-icon');
//     const moonIcon = document.querySelector('.moon-icon');

//     // Toggle dark mode
//     body.classList.toggle('dark-mode');

//     // Toggle icon states
//     if (body.classList.contains('dark-mode')) {
//         sunIcon.classList.remove('active');
//         moonIcon.classList.add('active');

//         // Optional: Fill moon when in dark mode
//         moonIcon.style.fill = 'white';
//         moonIcon.style.stroke = 'white';
//     } else {
//         sunIcon.classList.add('active');
//         moonIcon.classList.remove('active');

//         // Unfill moon in light mode
//         moonIcon.style.fill = 'none';
//         moonIcon.style.stroke = 'currentColor';
//     }
// }
