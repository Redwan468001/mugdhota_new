
// Script for Manu
// Function to initializw an overview navigation menu
function initializeOverviewNav(navSelector, sectionSelector) {
    const navLinks = document.querySelectorAll(`${navSelector} a`);
    const sections = document.querySelectorAll(sectionSelector);

    // Function to show the active section
    function setActiveSection(activeId) {
        sections.forEach((section) => {
            if (section.id === activeId) {
                section.classList.add("active_ov");
            } else {
                section.classList.remove("active_ov");
            }
        }); 
    }

    // Add click listeners to navigation links
    navLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const targetId = link.getAttribute("href").substring(1);
            setActiveSection(targetId);
        });
    });

    // Show the first section by default
    if (sections.length > 0) {
        setActiveSection(sections[0].id);
    }
    
    // Add active class to link
    navLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            // Remove the 'active' class from all links
            navLinks.forEach((nav) => nav.classList.remove("active_nav"));
            // Add the 'active' class to the clicked link
            link.classList.add("active_nav");
        });
    });

}

// Initialize multiple navigation menus
initializeOverviewNav(".overview_nav_1", ".content1 .msmcs_section");
initializeOverviewNav(".overview_nav_2", ".content2 .msmcs_section");
// initializeOverviewNav(".content_nav_1", ".m_content1 .msmcs_section");

// End Script for Manu


// Script for Overview content
function initializeContentNav(cntNavSelector, cntSelector) {
    const cntNavLinks = document.querySelectorAll(`${cntNavSelector} a`);
    const cntSections = document.querySelectorAll(cntSelector);

    // Function to show the active section
    function setActiveSection(activeId) {
        cntSections.forEach((cntsection) => {
            if (cntsection.id === activeId) {
                cntsection.classList.add("active_ov");
            } else {
                cntsection.classList.remove("active_ov")
            }
        });
    }

    // Add Click lintener to navigation links
    cntNavLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const targetId = link.getAttribute("href").substring(1);
            setActiveSection(targetId)
        });
    });

    // Show the first item by default
    if (cntSections.length > 0){
        setActiveSection(cntSections[0].id)
    }

    // All class to nav after click
    cntNavLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            // Remove the 'active' class from all links
            cntNavLinks.forEach((nav) => nav.classList.remove("active_cnt_nav"));
            // Add the 'active' class to the clicked link
            link.classList.add("active_cnt_nav")
        });
    });
}

initializeContentNav(".content_nav_1", ".m_content1 .msmcs_section");

// End Script for Overview content


