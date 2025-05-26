/**
 * AdminLTE JS - Basic Version
 * Lightweight JS file for basic AdminLTE functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar on mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('sidebar-open');
        });
    }

    // Dropdown menus
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            parent.classList.toggle('open');
        });
    });

    // Collapsible sidebar menu items
    const treeviewMenus = document.querySelectorAll('.treeview > a');
    treeviewMenus.forEach(function(menu) {
        menu.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            parent.classList.toggle('active');
            
            // Close other open menus (uncomment if needed)
            /*
            const siblings = Array.from(parent.parentElement.children).filter(function(item) {
                return item !== parent && item.classList.contains('treeview');
            });
            siblings.forEach(function(sibling) {
                sibling.classList.remove('active');
            });
            */
        });
    });

    // Box widgets
    const boxTools = document.querySelectorAll('.box-tools [data-widget="collapse"]');
    boxTools.forEach(function(tool) {
        tool.addEventListener('click', function(e) {
            e.preventDefault();
            const box = this.closest('.box');
            box.classList.toggle('collapsed-box');
            
            const icon = this.querySelector('i.fa');
            if (icon) {
                if (box.classList.contains('collapsed-box')) {
                    icon.classList.remove('fa-minus');
                    icon.classList.add('fa-plus');
                } else {
                    icon.classList.remove('fa-plus');
                    icon.classList.add('fa-minus');
                }
            }
        });
    });

    // Remove box
    const removeBoxButtons = document.querySelectorAll('.box-tools [data-widget="remove"]');
    removeBoxButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const box = this.closest('.box');
            box.remove();
        });
    });

    // Expandable search (optional)
    const searchExpand = document.querySelector('.navbar-nav .search-btn');
    if (searchExpand) {
        searchExpand.addEventListener('click', function(e) {
            e.preventDefault();
            const searchForm = document.querySelector('.navbar-nav .search-form');
            searchForm.classList.toggle('active');
        });
    }

    // Tooltip initialization (if you want to add your own implementation)
    const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltips.forEach(function(tooltip) {
        tooltip.addEventListener('mouseenter', function() {
            // Simple tooltip implementation
            const title = this.getAttribute('title') || this.getAttribute('data-original-title');
            if (!title) return;
            
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip';
            tooltipEl.textContent = title;
            document.body.appendChild(tooltipEl);
            
            const rect = this.getBoundingClientRect();
            tooltipEl.style.top = (rect.top - tooltipEl.offsetHeight - 5) + 'px';
            tooltipEl.style.left = (rect.left + rect.width / 2 - tooltipEl.offsetWidth / 2) + 'px';
            tooltipEl.style.opacity = '1';
            
            this.addEventListener('mouseleave', function() {
                tooltipEl.remove();
            }, { once: true });
        });
    });

    // Sidebar menu active link
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-menu a');
    sidebarLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentPath || currentPath.startsWith(href)) {
            link.closest('li').classList.add('active');
            // If it's in a treeview, also activate parent
            const treeview = link.closest('.treeview');
            if (treeview) {
                treeview.classList.add('active');
            }
        }
    });
});

// Push menu (sidebar toggle for all devices)
function toggleSidebar() {
    document.body.classList.toggle('sidebar-collapse');
}

// Control sidebar toggle (right sidebar)
function toggleControlSidebar() {
    document.body.classList.toggle('control-sidebar-open');
}

// Box widget functions
function collapseBox(element) {
    const box = element.closest('.box');
    box.classList.toggle('collapsed-box');
    
    const icon = element.querySelector('i.fa');
    if (icon) {
        if (box.classList.contains('collapsed-box')) {
            icon.classList.remove('fa-minus');
            icon.classList.add('fa-plus');
        } else {
            icon.classList.remove('fa-plus');
            icon.classList.add('fa-minus');
        }
    }
}

function removeBox(element) {
    const box = element.closest('.box');
    box.remove();
} 