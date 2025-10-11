/**
 * Google Maps Places Autocomplete Integration
 *
 * This script enables Google Maps Places Autocomplete on address forms.
 * It automatically populates address, city, state, postal code, county, and coordinates
 * when a user selects a place from the autocomplete dropdown.
 *
 * Updated to use the modern PlaceAutocompleteElement API (2025)
 *
 * Usage:
 * 1. Include this script after the Google Maps API script
 * 2. Call initializeAddressAutocomplete() with field IDs
 *
 * Example:
 * <script>
 *   initializeAddressAutocomplete({
 *     addressField: 'id_location_address',
 *     cityField: 'id_location_city',
 *     stateField: 'id_location_state_code',
 *     postalCodeField: 'id_location_postal_code',
 *     countyField: 'id_location_county',
 *     latitudeField: 'id_location_latitude',
 *     longitudeField: 'id_location_longitude'
 *   });
 * </script>
 */

let autocompleteInstance = null;

/**
 * Initialize Google Maps Places Autocomplete on an address field
 * Uses the modern PlaceAutocompleteElement or falls back to classic Autocomplete
 * @param {Object} config - Configuration object with field IDs
 * @param {string} config.searchContainerId - ID of the container where the search input will be placed
 * @param {string} config.addressField - ID of the address input field (will be populated, not replaced)
 * @param {string} [config.cityField] - ID of the city input field
 * @param {string} [config.stateField] - ID of the state input field
 * @param {string} [config.postalCodeField] - ID of the postal code input field
 * @param {string} [config.countyField] - ID of the county input field
 * @param {string} [config.latitudeField] - ID of the latitude input field
 * @param {string} [config.longitudeField] - ID of the longitude input field
 */
async function initializeAddressAutocomplete(config) {
    // Wait for Google Maps API to be available
    if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
        console.warn('Google Maps API not loaded. Autocomplete will not be available.');
        return;
    }

    const searchContainer = document.getElementById(config.searchContainerId);
    if (!searchContainer) {
        console.error(`Search container with ID "${config.searchContainerId}" not found`);
        return;
    }

    const addressInput = document.getElementById(config.addressField);
    if (!addressInput) {
        console.error(`Address field with ID "${config.addressField}" not found`);
        return;
    }

    try {
        // Use the classic Autocomplete widget since PlaceAutocompleteElement events don't work
        // Create a search input element
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'block w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-200';
        searchInput.placeholder = 'Start typing an address...';
        searchInput.id = 'google_maps_search_input';

        // Clear container and add search input
        searchContainer.innerHTML = '';
        searchContainer.appendChild(searchInput);

        // Create Autocomplete instance
        const autocomplete = new google.maps.places.Autocomplete(searchInput, {
            types: ['address'],
            componentRestrictions: { country: 'us' },
            fields: ['address_components', 'geometry', 'formatted_address', 'name']
        });

        // Listen for place selection
        autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();

            if (!place.geometry || !place.geometry.location) {
                console.warn('No geometry found for place');
                return;
            }

            // Clear all location fields first
            clearAddressFields(config);

            // Populate the address field (Address Line 1)
            const streetNumber = getAddressComponent(place.address_components, 'street_number');
            const route = getAddressComponent(place.address_components, 'route');
            const addressLine = `${streetNumber} ${route}`.trim() || place.formatted_address?.split(',')[0] || '';
            addressInput.value = addressLine;

            // Populate city
            if (config.cityField) {
                const city = getAddressComponent(place.address_components, 'locality') ||
                            getAddressComponent(place.address_components, 'sublocality_level_1');
                const cityField = document.getElementById(config.cityField);
                if (cityField && city) {
                    cityField.value = city;
                }
            }

            // Populate state
            if (config.stateField) {
                const state = getAddressComponent(place.address_components, 'administrative_area_level_1', 'short_name');
                const stateField = document.getElementById(config.stateField);
                if (stateField && state) {
                    stateField.value = state;
                }
            }

            // Populate postal code
            if (config.postalCodeField) {
                const postalCode = getAddressComponent(place.address_components, 'postal_code');
                const postalCodeField = document.getElementById(config.postalCodeField);
                if (postalCodeField && postalCode) {
                    postalCodeField.value = postalCode;
                }
            }

            // Populate county
            if (config.countyField) {
                const county = getAddressComponent(place.address_components, 'administrative_area_level_2');
                const countyField = document.getElementById(config.countyField);
                if (countyField && county) {
                    countyField.value = county;
                }
            }

            // Populate coordinates
            if (place.geometry && place.geometry.location) {
                if (config.latitudeField) {
                    const latField = document.getElementById(config.latitudeField);
                    if (latField) {
                        const lat = place.geometry.location.lat();
                        latField.value = lat.toFixed(7);
                    }
                }
                if (config.longitudeField) {
                    const lngField = document.getElementById(config.longitudeField);
                    if (lngField) {
                        const lng = place.geometry.location.lng();
                        lngField.value = lng.toFixed(7);
                    }
                }
            }

            // Trigger change events on all populated fields
            triggerChangeEvents(config);
        });

    } catch (error) {
        // Fall back on error
        console.error('Error with Autocomplete:', error);
        initializeFallbackInput(config, searchContainer);
    }
}

/**
 * Helper function to extract address component by type
 */
function getAddressComponent(addressComponents, type, nameType = 'long_name') {
    if (!addressComponents || !Array.isArray(addressComponents)) return '';

    for (const component of addressComponents) {
        if (component.types && component.types.includes(type)) {
            return component[nameType] || component.longText || component.shortText || '';
        }
    }
    return '';
}

/**
 * Fallback for when PlaceAutocompleteElement is not available
 * Creates a simple text input with instructions
 */
function initializeFallbackInput(config, searchContainer) {
    // Display a message in the search container
    searchContainer.innerHTML = '<p class="text-sm text-gray-500">Google Maps autocomplete is not available in your browser. Please enter your address manually in the fields below.</p>';

    console.warn('PlaceAutocompleteElement not available. Manual address entry required.');
}


/**
 * Clear all address fields
 * @param {Object} config - Configuration object with field IDs
 */
function clearAddressFields(config) {
    const fieldIds = [
        config.cityField,
        config.stateField,
        config.postalCodeField,
        config.countyField,
        config.latitudeField,
        config.longitudeField
    ];

    fieldIds.forEach(fieldId => {
        if (fieldId) {
            const field = document.getElementById(fieldId);
            if (field) field.value = '';
        }
    });
}

/**
 * Trigger change events on all populated fields
 * @param {Object} config - Configuration object with field IDs
 */
function triggerChangeEvents(config) {
    const fieldIds = [
        config.addressField,
        config.cityField,
        config.stateField,
        config.postalCodeField,
        config.countyField,
        config.latitudeField,
        config.longitudeField
    ];

    fieldIds.forEach(fieldId => {
        if (fieldId) {
            const field = document.getElementById(fieldId);
            if (field) {
                field.dispatchEvent(new Event('change', { bubbles: true }));
                field.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
}
