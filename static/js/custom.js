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
    const dropdownLinks = document.querySelectorAll('.dropdown a[data-toggle="collapse"]');
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



    // Theme Toggle Logic
    const applyTheme = (theme) => {
        document.body.classList.toggle('dark-theme-variables', theme === "dark");
        localStorage.setItem("theme", theme);

        const togglers = document.querySelectorAll('.theme-toggler, .theme-toggler-2');
        togglers.forEach(toggler => {
            toggler.querySelector('span:nth-child(1)').classList.toggle('active', theme === "light");
            toggler.querySelector('span:nth-child(2)').classList.toggle('active', theme === "dark");
        });

        const themeSelector = document.querySelector('#themeSelection');
        if (themeSelector) themeSelector.value = theme;
    };

    const savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);

    const themeTogglers = document.querySelectorAll('.theme-toggler, .theme-toggler-2');
    themeTogglers.forEach(toggler => {
        toggler.addEventListener('click', () => {
            const isDark = document.body.classList.contains('dark-theme-variables');
            applyTheme(isDark ? "light" : "dark");
        });
    });


    const themeSelector = document.querySelector('#themeSelection');
    if (themeSelector) {
        themeSelector.addEventListener('change', (event) => {
            applyTheme(event.target.value);
        });
    }

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

//Manual Override

function openEditModal(employeeId) {
    const employeeData = {
        101: 'Bilal',
        102: 'Shiraz',
        103: 'Abrar',
        104: 'Shariq',
        105: 'Abdul Saboor',
        // Add more employees here
    };

    const employeeName = employeeData[employeeId] || 'Unknown Employee';

    document.getElementById('employeeName').value = employeeName;
    const modal = new bootstrap.Modal(document.getElementById('editModal'));
    modal.show();
}

function saveOverride() {
    const employeeName = document.getElementById('employeeName').value;
    const overrideStatus = document.getElementById('overrideStatus').value;
    const reason = document.getElementById('reason').value;

    if (!reason.trim()) {
        alert('Please provide a reason for the override.');
        return;
    }

    const logEntry = `${employeeName} - Status changed to "${overrideStatus}" by HR at ${new Date().toLocaleTimeString()}, ${new Date().toLocaleDateString()} (Reason: ${reason})`;
    const logList = document.getElementById('auditLogList');
    const listItem = document.createElement('li');
    listItem.textContent = logEntry;
    logList.appendChild(listItem);

    alert('Override changes saved successfully!');
    const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
    modal.hide();
}
