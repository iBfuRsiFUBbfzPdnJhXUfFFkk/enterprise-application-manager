/**
 * Multiple Select Search Box with Chips Component
 *
 * A reusable component that creates a searchable chip-based interface for <select multiple> elements.
 * Based on the working implementation from application_group_form.html
 *
 * Features:
 * - Search/filter functionality
 * - Selected items displayed as removable chips
 * - Dropdown with filtered results
 * - Maintains Django form compatibility by syncing with underlying select element
 * - Works exclusively with <select multiple> elements
 *
 * Usage:
 * 1. Include this script in your template
 * 2. Include the CSS file (multiple_select_search_box.css)
 * 3. Call initializeMultipleSelectSearchBox() with configuration object
 *
 * Example:
 * <script>
 *   initializeMultipleSelectSearchBox({
 *     selectId: 'id_applications',
 *     searchInputId: 'applications_search',
 *     chipsContainerId: 'applications_chips',
 *     dropdownId: 'applications_dropdown',
 *     placeholder: 'Search applications...',
 *     emptyMessage: 'No applications found'
 *   });
 * </script>
 *
 * HTML Structure Required:
 * <div class="searchable-select-container">
 *   <div class="selected-chips" id="[chipsContainerId]"></div>
 *   <input type="text"
 *          class="chip-search-input"
 *          id="[searchInputId]"
 *          placeholder="Search and select..."
 *          autocomplete="off">
 *   <div class="search-dropdown hidden" id="[dropdownId]"></div>
 * </div>
 * <div class="hidden">
 *   <select multiple id="[selectId]" name="...">
 *     <option value="1">Item 1</option>
 *     <option value="2">Item 2</option>
 *   </select>
 * </div>
 */

/**
 * Initialize a multiple select search box component
 * @param {Object} config - Configuration object
 * @param {string} config.selectId - ID of the native <select multiple> element
 * @param {string} config.searchInputId - ID of the search input element
 * @param {string} config.chipsContainerId - ID of the chips container element
 * @param {string} config.dropdownId - ID of the dropdown container element
 * @param {string} [config.placeholder='Search and select...'] - Placeholder text for search input
 * @param {string} [config.emptyMessage='No items found'] - Message shown when no items match search
 * @returns {Object|null} - Returns the component instance or null if initialization fails
 */
function initializeMultipleSelectSearchBox(config) {
    // Validate configuration
    if (!config || !config.selectId || !config.searchInputId || !config.chipsContainerId || !config.dropdownId) {
        console.error('MultipleSelectSearchBox: Missing required configuration parameters');
        return null;
    }

    // Get DOM elements
    const nativeSelect = document.getElementById(config.selectId);
    const searchInput = document.getElementById(config.searchInputId);
    const chipsContainer = document.getElementById(config.chipsContainerId);
    const dropdown = document.getElementById(config.dropdownId);

    // Validate that all elements exist
    if (!nativeSelect) {
        console.error(`MultipleSelectSearchBox: Select element with ID "${config.selectId}" not found`);
        return null;
    }
    if (!searchInput) {
        console.error(`MultipleSelectSearchBox: Search input with ID "${config.searchInputId}" not found`);
        return null;
    }
    if (!chipsContainer) {
        console.error(`MultipleSelectSearchBox: Chips container with ID "${config.chipsContainerId}" not found`);
        return null;
    }
    if (!dropdown) {
        console.error(`MultipleSelectSearchBox: Dropdown with ID "${config.dropdownId}" not found`);
        return null;
    }

    // Validate that the select element is a multi-select
    if (!nativeSelect.multiple) {
        console.error(`MultipleSelectSearchBox: Select element with ID "${config.selectId}" is not a multi-select`);
        return null;
    }

    // Set defaults
    const placeholder = config.placeholder || 'Search and select...';
    const emptyMessage = config.emptyMessage || 'No items found';

    // Set placeholder
    searchInput.placeholder = placeholder;

    // Get all available options from the native select
    const allOptions = Array.from(nativeSelect.options).map(option => ({
        value: option.value,
        text: option.text,
        selected: option.selected
    }));

    // Track selected items
    let selectedItems = allOptions.filter(opt => opt.selected);

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Render selected items as chips
     */
    function renderChips() {
        chipsContainer.innerHTML = '';
        selectedItems.forEach(item => {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.innerHTML = `
                <span>${escapeHtml(item.text)}</span>
                <span class="chip-remove" data-value="${item.value}">&times;</span>
            `;
            chipsContainer.appendChild(chip);
        });

        // Update native select to maintain form compatibility
        Array.from(nativeSelect.options).forEach(option => {
            option.selected = selectedItems.some(item => item.value === option.value);
        });
    }

    /**
     * Render dropdown with filtered items
     * @param {string} searchTerm - The search term to filter by
     */
    function renderDropdown(searchTerm) {
        // Filter available items (not already selected)
        const availableItems = allOptions.filter(opt =>
            !selectedItems.some(sel => sel.value === opt.value) &&
            opt.text.toLowerCase().includes(searchTerm.toLowerCase())
        );

        if (availableItems.length === 0) {
            dropdown.innerHTML = `<div class="dropdown-empty">${escapeHtml(emptyMessage)}</div>`;
        } else {
            dropdown.innerHTML = availableItems.map(item => `
                <div class="dropdown-item" data-value="${item.value}">
                    ${escapeHtml(item.text)}
                </div>
            `).join('');
        }

        dropdown.classList.remove('hidden');
    }

    /**
     * Hide the dropdown
     */
    function hideDropdown() {
        dropdown.classList.add('hidden');
    }

    // Search input event
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim();
        renderDropdown(searchTerm);
    });

    // Focus event - show dropdown
    searchInput.addEventListener('focus', function() {
        const searchTerm = this.value.trim();
        renderDropdown(searchTerm);
    });

    // Click outside to close dropdown
    const clickOutsideHandler = function(e) {
        if (!e.target.closest('.searchable-select-container')) {
            hideDropdown();
        }
    };
    document.addEventListener('click', clickOutsideHandler);

    // Event delegation for dropdown items
    dropdown.addEventListener('click', function(e) {
        const item = e.target.closest('.dropdown-item');
        if (item) {
            const value = item.dataset.value;
            const option = allOptions.find(opt => opt.value === value);
            if (option) {
                selectedItems.push(option);
                renderChips();
                searchInput.value = '';
                renderDropdown('');
                searchInput.focus();
            }
        }
    });

    // Event delegation for chip removal
    chipsContainer.addEventListener('click', function(e) {
        const removeBtn = e.target.closest('.chip-remove');
        if (removeBtn) {
            const value = removeBtn.dataset.value;
            selectedItems = selectedItems.filter(item => item.value !== value);
            renderChips();
            const searchTerm = searchInput.value.trim();
            renderDropdown(searchTerm);
        }
    });

    // Initialize - render chips for pre-selected items
    renderChips();

    // Return instance with public methods
    return {
        allOptions: allOptions,
        selectedItems: selectedItems,
        renderChips: renderChips,
        renderDropdown: renderDropdown,
        hideDropdown: hideDropdown,
        destroy: function() {
            // Clean up event listeners
            document.removeEventListener('click', clickOutsideHandler);
        }
    };
}

/**
 * Initialize multiple search boxes at once
 * @param {Array<Object>} configs - Array of configuration objects
 * @returns {Array<Object>} - Array of component instances
 */
function initializeMultipleSelectSearchBoxes(configs) {
    return configs.map(config => initializeMultipleSelectSearchBox(config)).filter(instance => instance !== null);
}